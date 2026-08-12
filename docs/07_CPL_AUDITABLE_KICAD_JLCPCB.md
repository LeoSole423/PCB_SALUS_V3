# CPL auditable: KiCad → JLCPCB

`tools/jlc_cpl.py` es el único procedimiento admitido para crear un CPL nuevo.
No se editan coordenadas ni rotaciones directamente en un CSV: toda excepción
queda en `config/jlcpcb-cpl.json`, con motivo y fuente.

## Contrato JLCPCB

El archivo final contiene exactamente `Designator,Mid X,Mid Y,Layer,Rotation`.
Las coordenadas llevan `mm`, la capa es `Top` o `Bottom` y la rotación está en
`[0,360)`. JLCPCB interpreta `Mid X/Mid Y` como el centroide de colocación y
la rotación positiva en sentido antihorario. La herramienta parte del origen
auxiliar de KiCad; el perfil especifica el signo de los ejes, por lo que nunca
debe invertirse Y en una hoja de cálculo.

## Centros y reglas

KiCad puede tener tres centros diferentes:

- `anchor`: origen de la huella, que es el origen del exportador de KiCad.
- `pad_center`: centro de la envolvente de pads; útil para hallar anclas
  excéntricas, pero no es automáticamente el centro de montaje.
- `body_center`: estimación a partir de geometría de huella/courtyard.

Si cualquiera difiere más de 0,20 mm, el informe exige una regla explícita o
marca el componente `needs_review`. Esto sucede, por ejemplo, en U1, U8 y
J16. La imagen 3D de JLCPCB no es por sí sola una prueba de que el centro
matemático sea erróneo.

Las reglas tienen precedencia: referencia, LCSC, huella exacta, regex de
familia y base KiCad. Cada una admite `rotation_offset_deg`,
`position_offset_local_mm`, `origin`, `reason`, `source` y `confirmed_on`.
El offset se rota junto con la huella. Dos reglas coincidentes del mismo nivel
son un error: un agente debe resolverlas, no elegir arbitrariamente.

## Flujo para agentes y CI

```bash
/usr/bin/python3 tools/jlc_cpl.py generate PCB_SALUS_v3.kicad_pcb \
  --config config/jlcpcb-cpl.json \
  --bom fabricacion/JLCPCB_2026-08-12_SALUS_v3/PCB_SALUS_v3-JLC-BOM.csv \
  --output /tmp/salus-cpl.csv --raw-output /tmp/salus-cpl-raw.csv \
  --report /tmp/cpl-audit.json --review-output /tmp/cpl-review.csv \
  --overlay /tmp/cpl-overlay.svg

/usr/bin/python3 tools/jlc_cpl.py validate PCB_SALUS_v3.kicad_pcb \
  --config config/jlcpcb-cpl.json --bom fabricacion/JLCPCB_2026-08-12_SALUS_v3/PCB_SALUS_v3-JLC-BOM.csv \
  --cpl /tmp/salus-cpl.csv --report /tmp/cpl-validation.json

/usr/bin/python3 tools/jlc_cpl.py diff /tmp/salus-cpl-raw.csv /tmp/salus-cpl.csv \
  --output /tmp/cpl-diff.json
```

`generate` retorna 0 solo si la lista es completa y ningún elemento exige
revisión; 2 representa un resultado generado pero no liberable; 3 representa
un error de entrada/configuración. Sus informes JSON son la fuente de verdad
para otro agente.

## Calibración desde el visor JLCPCB

Después de cargar Gerbers, BOM y CPL, registrar solo observaciones inequívocas:

```json
{
  "observations": [{
    "reference": "U2",
    "origin": "anchor",
    "rotation_offset_deg": 90,
    "position_offset_local_mm": [0, 0],
    "reason": "Pin 1 del componente JLC coincide con pin 1 de la huella",
    "source": "JLCPCB viewer, captura enlazada",
    "confirmed_on": "2026-08-12"
  }]
}
```

Proponer la modificación sin tocar nada:

```bash
/usr/bin/python3 tools/jlc_cpl.py calibrate config/jlcpcb-cpl.json \
  --observations observaciones.json --output /tmp/reglas-propuestas.json --dry-run
```

Tras revisión humana, ejecutar de nuevo con `--apply`, regenerar, comparar y
volver a inspeccionar. Solo entonces se actualiza el paquete de fabricación y
su checksum. Gerbers y BOM no cambian por una corrección exclusiva del CPL.

La aceptación exige cuerpos sobre pads y pin 1/polaridad correctos para todos
los componentes asimétricos, no solo una previsualización global aparentemente
alineada.
