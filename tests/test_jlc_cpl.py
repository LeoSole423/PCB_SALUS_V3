import importlib.util
import json
import csv
import math
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location("jlc_cpl", Path(__file__).parents[1] / "tools" / "jlc_cpl.py")
jlc_cpl = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(jlc_cpl)


class TransformTests(unittest.TestCase):
    def test_normalize_angle(self):
        self.assertEqual(jlc_cpl.normalize_angle(-90), 270)
        self.assertEqual(jlc_cpl.normalize_angle(720), 0)

    def test_top_local_offset_rotates_counter_clockwise(self):
        x, y = jlc_cpl.rotate_local((1, 0), 90)
        self.assertAlmostEqual(x, 0, places=6)
        self.assertAlmostEqual(y, 1, places=6)

    def test_bottom_local_offset_uses_mirrored_transform(self):
        x, y = jlc_cpl.rotate_local((1, 0), 30, bottom=True)
        self.assertAlmostEqual(x, 0.8660254, places=6)
        self.assertAlmostEqual(y, 0.5, places=6)


class ConfigTests(unittest.TestCase):
    def config(self):
        return {"schema_version": 1, "rules": [
            {"id": "family", "match": {"footprint_regex": "SOIC"}, "origin": "anchor", "position_offset_local_mm": [0, 0]},
            {"id": "exact", "match": {"reference": "U1"}, "origin": "pad_center", "position_offset_local_mm": [0, 0]}
        ]}

    def test_reference_precedes_regex(self):
        rule, tier, error = jlc_cpl.find_rule(self.config(), "U1", "", "Package_SO:SOIC-8")
        self.assertEqual((rule["id"], tier, error), ("exact", "reference", None))

    def test_ambiguous_rule_is_rejected(self):
        config = self.config(); config["rules"].append({"id": "also-exact", "match": {"reference": "U1"}, "origin": "anchor", "position_offset_local_mm": [0, 0]})
        rule, tier, error = jlc_cpl.find_rule(config, "U1", "", "Package_SO:SOIC-8")
        self.assertIsNone(rule); self.assertEqual(tier, "reference"); self.assertIn("ambiguous", error)

    def test_invalid_rule_is_rejected(self):
        with self.assertRaises(ValueError):
            jlc_cpl.validate_config({"schema_version": 1, "rules": [{"match": {"reference": "U1", "lcsc": "C1"}}]})

    def test_confirmed_rule_metadata_is_valid(self):
        config = {"schema_version": 1, "rules": [{"id": "confirmed", "match": {"reference": "U1"}, "origin": "anchor", "position_offset_local_mm": [0, 0], "requires_confirmation": False, "confirmed_on": "2026-08-12"}]}
        jlc_cpl.validate_config(config)


class CsvTests(unittest.TestCase):
    def test_bom_designator_parser_detects_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            bom = Path(directory) / "bom.csv"
            bom.write_text("Comment,Designator,Footprint,LCSC Part #\nX,U1,U,C1\nX,U1,U,C1\n", encoding="utf-8")
            refs, duplicates = jlc_cpl.load_bom_designators(bom)
            self.assertEqual(refs, {"U1"}); self.assertEqual(duplicates, ["U1"])

    def test_close_centroids_are_rejected(self):
        rows = [
            {"Designator": "C1", "Mid X": "10mm", "Mid Y": "20mm"},
            {"Designator": "C2", "Mid X": "10.1mm", "Mid Y": "20mm"}
        ]
        self.assertEqual(jlc_cpl.close_designator_pairs(rows, 0.2), ["C1 / C2: 0.100000 mm"])


@unittest.skipIf(jlc_cpl.pcbnew is None, "KiCad pcbnew is unavailable")
class SalusGoldenTests(unittest.TestCase):
    ROOT = Path(__file__).parents[1]

    def setUp(self):
        self.config = jlc_cpl.read_json(self.ROOT / "config/jlcpcb-cpl.json")
        self.bom = self.ROOT / "fabricacion/JLCPCB_2026-08-12_SALUS_v3/PCB_SALUS_v3-JLC-BOM.csv"
        self.expected = self.ROOT / "production/pcb_test_positions.csv"
        self.board = jlc_cpl.pcbnew.LoadBoard(str(self.ROOT / "PCB_SALUS_v3.kicad_pcb"))

    def test_golden_matches_toolkit_except_confirmed_calibrations(self):
        wanted, duplicates = jlc_cpl.load_bom_designators(self.bom)
        lcsc = jlc_cpl.get_lcsc_by_ref(self.bom)
        footprints = {x.GetReference(): x for x in self.board.GetFootprints() if not (x.GetAttributes() & jlc_cpl.pcbnew.FP_EXCLUDE_FROM_POS_FILES) and not x.IsDNP()}
        actual = {ref: jlc_cpl.make_row(footprints[ref], self.config, lcsc[ref]) for ref in wanted}
        with self.expected.open(newline="", encoding="utf-8-sig") as handle:
            baseline = {x["Designator"]: x for x in csv.DictReader(handle)}
        self.assertEqual(len(wanted), 63)
        self.assertEqual(duplicates, [])
        self.assertEqual(set(actual), set(baseline))
        changed = set()
        for ref, row in actual.items():
            values = (jlc_cpl.parse_number(row["cpl"]["Mid X"]), jlc_cpl.parse_number(row["cpl"]["Mid Y"]), float(row["cpl"]["Rotation"]))
            expected = (float(baseline[ref]["Mid X"]), float(baseline[ref]["Mid Y"]), float(baseline[ref]["Rotation"]))
            if any(not math.isclose(left, right, abs_tol=1e-6) for left, right in zip(values, expected)):
                changed.add(ref)
        self.assertEqual(changed, {"U1", "U4", "U8", "J16"})

    def test_off_center_footprints_have_confirmed_explicit_rules(self):
        lcsc = jlc_cpl.get_lcsc_by_ref(self.bom)
        fps = {x.GetReference(): x for x in self.board.GetFootprints()}
        for ref in ("U1", "U8", "J16"):
            row = jlc_cpl.make_row(fps[ref], self.config, lcsc[ref])
            self.assertEqual(row["status"], "ready")
            self.assertEqual(row["rule_precedence"], "reference")
            self.assertGreater(max(x for x in row["center_differences_mm"].values() if x is not None), 0.2)


if __name__ == "__main__":
    unittest.main()
