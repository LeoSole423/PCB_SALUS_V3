# Organización del repositorio

Actualizada el 15/10/2026. El proyecto editable permanece en la raíz para
conservar las referencias de hojas, bibliotecas y modelos 3D.

| Ruta | Contenido |
|---|---|
| `PCB_SALUS_v3.kicad_pro`, `.kicad_pcb`, `.kicad_sch`, `.kicad_dru` | Proyecto, placa, esquema raíz y reglas activos. |
| `ESP32.kicad_sch`, `SENSORES.kicad_sch`, `ALIMENTACION.kicad_sch` | Hojas activas. |
| `Libs/`, `fp-lib-table`, `sym-lib-table` | Bibliotecas y modelos, conservando rutas originales. |
| `fabricacion/actual/` | Última entrega conservada. Ver índice de fabricación. |
| `fabricacion/historico/` | Entregas sustituidas. |
| `fabricacion/cotizaciones/` | Cotizaciones y variantes anteriores. |
| `archivo/` | Fragmentos v2, hoja vacía, respaldo y exportación toolkit antigua. |
| `referencias/jlcpcb/` | Ejemplos XLSX del proveedor. |
| `bom/` | BOM de seguimiento activa. |
| `config/`, `tools/`, `tests/` | Perfiles, generador CPL y pruebas. |
| `docs/`, `datasheets/`, `spice/` | Documentación, datasheets y simulaciones. |
| `analysis/` | Caché local de análisis; su manifiesto histórico no acredita el diseño actual. |

`fabrication-toolkit-options.json` permanece en la raíz por compatibilidad con
el plugin. Su nombre de exportación `pcb_test` es histórico: cualquier nueva
exportación debe generarse en una carpeta nueva y claramente identificada.
`.history/`, archivos de sesión y cachés siguen excluidos de Git.

La reorganización conserva los diseños y archivos de fabricación. Solo se
actualizaron rutas operativas en documentación/pruebas y se hicieron portables
los manifiestos SHA-256. Los informes y copias históricas no se reescribieron.
