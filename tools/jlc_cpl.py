#!/usr/bin/env python3
"""Generate an auditable JLCPCB Component Placement List from a KiCad PCB.

The program deliberately keeps manufacturer-specific corrections outside the
PCB.  It is suitable for CI and agents: every final CPL row is explained in a
JSON audit report and uncertain placements return a non-zero status.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

try:
    import pcbnew  # type: ignore
except ImportError:  # allows pure transformation tests without KiCad
    pcbnew = None


HEADERS = ["Designator", "Mid X", "Mid Y", "Layer", "Rotation"]
SCHEMA_VERSION = 1


def normalize_angle(value: float) -> float:
    """Return an angle in [0, 360)."""
    result = value % 360.0
    return 0.0 if math.isclose(result, 360.0) else result


def rotate_local(offset: tuple[float, float], angle_deg: float, bottom: bool = False) -> tuple[float, float]:
    """Rotate a local XY correction into the output coordinate system."""
    x, y = offset
    radians = math.radians(angle_deg)
    cos_a, sin_a = math.cos(radians), math.sin(radians)
    if bottom:
        return (x * cos_a + y * sin_a, x * sin_a - y * cos_a)
    return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)


def mm(value: int) -> float:
    return pcbnew.ToMM(value)  # type: ignore[union-attr]


def point_mm(point: Any) -> list[float]:
    return [round(mm(point.x), 6), round(mm(point.y), 6)]


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def parse_number(value: str) -> float:
    return float(value.strip().removesuffix("mm"))


def load_bom_designators(path: Path) -> tuple[set[str], list[str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "Designator" not in reader.fieldnames:
            raise ValueError("BOM must contain a Designator column")
        result: list[str] = []
        for row in reader:
            result.extend(x.strip() for x in row["Designator"].split(",") if x.strip())
    duplicates = sorted(ref for ref, count in Counter(result).items() if count > 1)
    return set(result), duplicates


def get_lcsc_by_ref(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return {
            ref.strip(): row.get("LCSC Part #", "").strip()
            for row in reader
            for ref in row["Designator"].split(",")
            if ref.strip()
        }


def validate_config(config: dict[str, Any]) -> None:
    if config.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"Unsupported config schema_version: {config.get('schema_version')!r}")
    for index, rule in enumerate(config.get("rules", [])):
        match = rule.get("match", {})
        keys = [key for key in ("reference", "lcsc", "footprint", "footprint_regex") if key in match]
        if len(keys) != 1:
            raise ValueError(f"rule {index} must have exactly one match key")
        if "footprint_regex" in match:
            re.compile(match["footprint_regex"])
        if rule.get("origin", "anchor") not in ("anchor", "pad_center", "body_center"):
            raise ValueError(f"rule {index} has invalid origin")
        offset = rule.get("position_offset_local_mm", [0, 0])
        if not (isinstance(offset, list) and len(offset) == 2 and all(isinstance(n, (int, float)) for n in offset)):
            raise ValueError(f"rule {index} position_offset_local_mm must be [x, y]")


def footprint_name(footprint: Any) -> str:
    fpid = footprint.GetFPID()
    return str(fpid.GetUniStringLibId())


def pad_center(footprint: Any) -> Any | None:
    pads = list(footprint.Pads())
    if not pads:
        return None
    bbox = pads[0].GetBoundingBox()
    for pad in pads[1:]:
        bbox.Merge(pad.GetBoundingBox())
    return bbox.GetCenter()


def body_center(footprint: Any) -> Any | None:
    # KiCad includes graphic/courtyard geometry in this box.  It is an estimate,
    # intentionally recorded as such rather than mistaken for machine truth.
    bbox = footprint.GetBoundingBox(False, False)
    return bbox.GetCenter() if bbox.GetWidth() and bbox.GetHeight() else None


def distance(a: list[float] | None, b: list[float] | None) -> float | None:
    if a is None or b is None:
        return None
    return round(math.hypot(a[0] - b[0], a[1] - b[1]), 6)


def matching_rules(rules: list[dict[str, Any]], ref: str, lcsc: str, fp: str) -> tuple[list[dict[str, Any]], str]:
    tiers = (("reference", ref), ("lcsc", lcsc), ("footprint", fp), ("footprint_regex", fp))
    for key, value in tiers:
        found = []
        for rule in rules:
            match = rule.get("match", {})
            if key == "footprint_regex" and key in match and re.search(match[key], value):
                found.append(rule)
            elif key in match and match[key] == value:
                found.append(rule)
        if found:
            return found, key
    return [], "base"


def find_rule(config: dict[str, Any], ref: str, lcsc: str, fp: str) -> tuple[dict[str, Any] | None, str, str | None]:
    found, tier = matching_rules(config.get("rules", []), ref, lcsc, fp)
    if len(found) > 1:
        return None, tier, f"ambiguous {tier} rules: " + ", ".join(x.get("id", "<unnamed>") for x in found)
    return (found[0] if found else None), tier, None


def field_value(footprint: Any, name: str) -> str:
    try:
        field = footprint.GetFieldByName(name)
        return field.GetText().strip() if field else ""
    except AttributeError:
        return ""


def make_row(footprint: Any, config: dict[str, Any], lcsc: str) -> dict[str, Any]:
    ref, fp = footprint.GetReference(), footprint_name(footprint)
    anchor = point_mm(footprint.GetPosition())
    pad = point_mm(pad_center(footprint)) if pad_center(footprint) else None
    body = point_mm(body_center(footprint)) if body_center(footprint) else None
    rule, tier, error = find_rule(config, ref, lcsc, fp)
    selected_origin = (rule or {}).get("origin", config.get("defaults", {}).get("origin", "anchor"))
    centers = {"anchor": anchor, "pad_center": pad, "body_center": body}
    selected = centers.get(selected_origin)
    status: list[str] = []
    if error:
        status.append(error)
    if selected is None:
        selected = anchor
        status.append(f"{selected_origin} unavailable; used anchor")
    threshold = float(config.get("review", {}).get("center_difference_mm", 0.2))
    max_difference = max((x for x in (distance(anchor, pad), distance(anchor, body), distance(pad, body)) if x is not None), default=0.0)
    explicit = tier in ("reference", "lcsc", "footprint")
    required_refs = set(config.get("review", {}).get("require_confirmation_references", []))
    confirmed = bool((rule or {}).get("confirmed_on")) and (rule or {}).get("requires_confirmation") is False
    asymmetric = (ref in required_refs or bool((rule or {}).get("requires_confirmation", False))) and not confirmed
    if max_difference > threshold and not explicit:
        status.append(f"center difference {max_difference:.3f} mm needs explicit rule")
    if asymmetric:
        status.append("requires JLC viewer confirmation")
    raw_angle = footprint.GetOrientation().AsDegrees()
    angle = raw_angle
    layer = "Bottom" if footprint.GetLayer() == pcbnew.B_Cu else "Top"
    if layer == "Bottom":
        angle = 180.0 - angle
    offset = tuple((rule or {}).get("position_offset_local_mm", [0.0, 0.0]))
    # Offset lives in the footprint's local KiCad coordinates.  For Bottom,
    # JLC's output angle is mirrored later, but the local vector must still be
    # transformed using KiCad's original footprint angle.
    local = rotate_local(offset, raw_angle, layer == "Bottom")
    aux = footprint.GetBoard().GetDesignSettings().GetAuxOrigin()
    signs = config.get("coordinates", {"x_sign": 1, "y_sign": -1})
    x = (selected[0] - mm(aux.x)) * float(signs.get("x_sign", 1)) + local[0]
    y = (selected[1] - mm(aux.y)) * float(signs.get("y_sign", -1)) + local[1]
    rotation = normalize_angle(angle + float((rule or {}).get("rotation_offset_deg", 0.0)))
    return {
        "designator": ref, "footprint": fp, "lcsc": lcsc, "layer": layer,
        "centers_mm": {"anchor": anchor, "pad_center": pad, "body_center": body},
        "center_differences_mm": {"anchor_pad": distance(anchor, pad), "anchor_body": distance(anchor, body), "pad_body": distance(pad, body)},
        "selected_origin": selected_origin, "selected_center_mm": selected,
        "raw_rotation_deg": normalize_angle(raw_angle),
        "rotation_offset_deg": float((rule or {}).get("rotation_offset_deg", 0.0)),
        "position_offset_local_mm": list(offset), "position_offset_output_mm": [round(local[0], 6), round(local[1], 6)],
        "rule_id": (rule or {}).get("id", "base"), "rule_precedence": tier,
        "status": "needs_review" if status else "ready", "reasons": status,
        "cpl": {"Designator": ref, "Mid X": f"{x:.6f}mm", "Mid Y": f"{y:.6f}mm", "Layer": layer, "Rotation": f"{rotation:.3f}"},
        "raw_cpl": {"Designator": ref, "Mid X": f"{((anchor[0] - mm(aux.x)) * float(signs.get('x_sign', 1))):.6f}mm", "Mid Y": f"{((anchor[1] - mm(aux.y)) * float(signs.get('y_sign', -1))):.6f}mm", "Layer": layer, "Rotation": f"{normalize_angle(angle):.3f}"},
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def write_review(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = ["Designator", "Footprint", "LCSC", "Selected origin", "Rule", "Status", "Reasons", "Anchor mm", "Pad center mm", "Body center mm", "CPL X", "CPL Y", "Rotation"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n"); writer.writeheader()
        for row in rows:
            c = row["cpl"]; centers = row["centers_mm"]
            writer.writerow({"Designator": row["designator"], "Footprint": row["footprint"], "LCSC": row["lcsc"], "Selected origin": row["selected_origin"], "Rule": row["rule_id"], "Status": row["status"], "Reasons": "; ".join(row["reasons"]), "Anchor mm": centers["anchor"], "Pad center mm": centers["pad_center"], "Body center mm": centers["body_center"], "CPL X": c["Mid X"], "CPL Y": c["Mid Y"], "Rotation": c["Rotation"]})


def write_svg(path: Path, rows: list[dict[str, Any]]) -> None:
    pts = [p for row in rows for p in (row["centers_mm"]["anchor"], row["centers_mm"]["pad_center"], row["centers_mm"]["body_center"]) if p]
    lo_x, hi_x = min(x[0] for x in pts) - 5, max(x[0] for x in pts) + 5
    lo_y, hi_y = min(x[1] for x in pts) - 5, max(x[1] for x in pts) + 5
    width, height = hi_x - lo_x, hi_y - lo_y
    elements = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{lo_x} {lo_y} {width} {height}"><style>text{{font:1.2px sans-serif}}.a{{fill:#06c}}.p{{fill:#e80}}.b{{fill:#777}}.f{{fill:#d20}}</style><rect x="{lo_x}" y="{lo_y}" width="{width}" height="{height}" fill="white"/>']
    for row in rows:
        centers = row["centers_mm"]
        for key, cls in (("anchor", "a"), ("pad_center", "p"), ("body_center", "b")):
            if centers[key]: elements.append(f'<circle class="{cls}" cx="{centers[key][0]}" cy="{centers[key][1]}" r="0.35"/>')
        c = row["cpl"]; x, y = parse_number(c["Mid X"]), -parse_number(c["Mid Y"])
        color = "f" if row["status"] != "ready" else "a"
        elements.append(f'<path class="{color}" d="M{x-0.6},{y}h1.2M{x},{y-0.6}v1.2"/><text x="{x+0.6}" y="{y-0.6}">{row["designator"]}</text>')
    elements.append('<text x="5" y="5">blue=anchor, orange=pad center, gray=body center, cross=CPL</text></svg>')
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text("\n".join(elements), encoding="utf-8")


def close_designator_pairs(rows: list[dict[str, str]], minimum_mm: float) -> list[str]:
    """Return pairs whose CPL centroids violate JLCPCB's minimum spacing."""
    points = [(row["Designator"], parse_number(row["Mid X"]), parse_number(row["Mid Y"])) for row in rows]
    return [f"{a} / {b}: {math.hypot(ax - bx, ay - by):.6f} mm" for index, (a, ax, ay) in enumerate(points) for b, bx, by in points[index + 1:] if math.hypot(ax - bx, ay - by) < minimum_mm]


def generate(args: argparse.Namespace) -> int:
    if pcbnew is None: raise RuntimeError("pcbnew is required; run with KiCad Python")
    config, board_path, bom_path = read_json(Path(args.config)), Path(args.board), Path(args.bom)
    validate_config(config); wanted, duplicate_bom = load_bom_designators(bom_path); lcsc = get_lcsc_by_ref(bom_path)
    board = pcbnew.LoadBoard(str(board_path)); candidates = {f.GetReference(): f for f in board.GetFootprints() if not (f.GetAttributes() & pcbnew.FP_EXCLUDE_FROM_POS_FILES) and not f.IsDNP()}
    rows = [make_row(candidates[ref], config, lcsc.get(ref, "")) for ref in sorted(wanted & set(candidates))]
    missing_board, excluded = sorted(wanted - set(candidates)), sorted(set(candidates) - wanted)
    audit = {"schema_version": SCHEMA_VERSION, "board": str(board_path), "bom": str(bom_path), "coordinate_transform": config.get("coordinates"), "summary": {"bom_designators": len(wanted), "cpl_designators": len(rows), "missing_from_board": missing_board, "excluded_from_bom": excluded, "duplicate_bom_designators": duplicate_bom, "needs_review": [x["designator"] for x in rows if x["status"] != "ready"]}, "components": rows}
    write_csv(Path(args.output), [x["cpl"] for x in rows]); write_csv(Path(args.raw_output), [x["raw_cpl"] for x in rows]); write_json(Path(args.report), audit); write_review(Path(args.review_output), rows); write_svg(Path(args.overlay), rows)
    print(f"CPL: {len(rows)} rows; needs_review={len(audit['summary']['needs_review'])}; missing={len(missing_board)}")
    return 2 if missing_board or duplicate_bom or audit["summary"]["needs_review"] else 0


def validate(args: argparse.Namespace) -> int:
    config = read_json(Path(args.config)); validate_config(config)
    wanted, duplicates = load_bom_designators(Path(args.bom))
    with Path(args.cpl).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle); rows = list(reader); headers = reader.fieldnames
    errors: list[str] = []
    if headers != HEADERS: errors.append(f"headers must be {HEADERS}")
    refs = [x.get("Designator", "") for x in rows]
    if set(refs) != wanted: errors.append("BOM/CPL designator mismatch")
    if len(refs) != len(set(refs)): errors.append("duplicate CPL designators")
    if pcbnew is not None:
        board = pcbnew.LoadBoard(str(args.board))
        placeable = {f.GetReference() for f in board.GetFootprints() if not (f.GetAttributes() & pcbnew.FP_EXCLUDE_FROM_POS_FILES) and not f.IsDNP()}
        if set(refs) - placeable:
            errors.append("CPL includes footprints excluded from current board position data")
        if wanted - placeable:
            errors.append("BOM includes footprints absent from current board position data")
    for row in rows:
        try:
            if row["Layer"] not in ("Top", "Bottom"): raise ValueError("invalid layer")
            for key in ("Mid X", "Mid Y", "Rotation"): math.isfinite(parse_number(row[key]))
        except Exception as exc: errors.append(f"{row.get('Designator','?')}: {exc}")
    if not errors:
        minimum = float(config.get("review", {}).get("min_component_spacing_mm", 0.2))
        errors.extend("centroid spacing below %.3f mm: %s" % (minimum, pair) for pair in close_designator_pairs(rows, minimum))
    report = {"valid": not errors, "errors": errors, "bom_designators": len(wanted), "cpl_designators": len(rows), "duplicate_bom_designators": duplicates}
    write_json(Path(args.report), report); print(f"Validation: {'PASS' if not errors else 'FAIL'}; errors={len(errors)}")
    return 0 if not errors else 2


def diff(args: argparse.Namespace) -> int:
    def load(path: Path) -> dict[str, dict[str, str]]:
        with path.open(newline="", encoding="utf-8-sig") as h: return {r["Designator"]: r for r in csv.DictReader(h)}
    raw, final = load(Path(args.raw_cpl)), load(Path(args.final_cpl)); result = []
    for ref in sorted(set(raw) | set(final)):
        if ref not in raw or ref not in final: result.append({"designator": ref, "status": "missing", "raw": raw.get(ref), "final": final.get(ref)}); continue
        delta = {key: round(parse_number(final[ref][key]) - parse_number(raw[ref][key]), 6) for key in ("Mid X", "Mid Y", "Rotation")}
        delta["Rotation"] = ((delta["Rotation"] + 180) % 360) - 180
        result.append({"designator": ref, "status": "changed" if any(delta.values()) else "unchanged", "delta": delta, "raw": raw[ref], "final": final[ref]})
    write_json(Path(args.output), {"raw": str(args.raw_cpl), "final": str(args.final_cpl), "components": result}); print(f"Diff: {sum(x['status']=='changed' for x in result)} changed / {len(result)}")
    return 0


def calibrate(args: argparse.Namespace) -> int:
    config, observations = read_json(Path(args.config)), read_json(Path(args.observations)); validate_config(config)
    proposed = []
    for observation in observations.get("observations", []):
        ref = observation["reference"]
        proposed.append({"id": f"calibration-{ref.lower()}-{date.today().isoformat()}", "match": {"reference": ref}, "origin": observation.get("origin", "anchor"), "rotation_offset_deg": observation.get("rotation_offset_deg", 0), "position_offset_local_mm": observation.get("position_offset_local_mm", [0, 0]), "requires_confirmation": False, "reason": observation["reason"], "source": observation.get("source", "JLCPCB viewer"), "confirmed_on": observation.get("confirmed_on", date.today().isoformat())})
    document = {"dry_run": not args.apply, "schema_version": SCHEMA_VERSION, "proposed_rules": proposed}
    if args.apply and args.dry_run:
        raise ValueError("--apply and --dry-run cannot be used together")
    if args.apply:
        calibrated_refs = {x["match"]["reference"] for x in proposed}
        # A calibration deliberately supersedes an older per-reference rule;
        # leaving both would make the config ambiguous and fail generation.
        retained = [rule for rule in config.get("rules", []) if rule.get("match", {}).get("reference") not in calibrated_refs]
        config["rules"] = proposed + retained
        write_json(Path(args.config), config)
    if args.output: write_json(Path(args.output), document)
    print(f"Calibration: {len(proposed)} proposed rules; {'applied' if args.apply else 'dry-run'}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("generate"); p.add_argument("board"); p.add_argument("--config", required=True); p.add_argument("--bom", required=True); p.add_argument("--output", required=True); p.add_argument("--report", required=True); p.add_argument("--raw-output", required=True); p.add_argument("--review-output", required=True); p.add_argument("--overlay", required=True); p.set_defaults(func=generate)
    p = sub.add_parser("validate"); p.add_argument("board"); p.add_argument("--config", required=True); p.add_argument("--bom", required=True); p.add_argument("--cpl", required=True); p.add_argument("--report", required=True); p.set_defaults(func=validate)
    p = sub.add_parser("diff"); p.add_argument("raw_cpl"); p.add_argument("final_cpl"); p.add_argument("--output", required=True); p.set_defaults(func=diff)
    p = sub.add_parser("calibrate"); p.add_argument("config"); p.add_argument("--observations", required=True); p.add_argument("--output"); p.add_argument("--apply", action="store_true"); p.add_argument("--dry-run", action="store_true", help="Explicitly keep the config unchanged (the default)"); p.set_defaults(func=calibrate)
    args = parser.parse_args()
    try: return args.func(args)
    except (ValueError, RuntimeError, KeyError) as exc: print(f"ERROR: {exc}", file=sys.stderr); return 3


if __name__ == "__main__":
    raise SystemExit(main())
