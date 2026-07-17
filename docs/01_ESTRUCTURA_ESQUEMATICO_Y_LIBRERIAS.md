# Estructura del esquematico y librerias

## Hojas activas

| Hoja | Responsabilidad |
|---|---|
| `ESP32.kicad_sch` | ESP32-S3, USB-C UART0, USB-C nativo, CP2102N y autoprogramacion. |
| `SENSORES.kicad_sch` | IMU, sensores, BTS7960, reles, servo y conectores de campo. |
| `ALIMENTACION.kicad_sch` | Entrada 5 V, buck AP63203WU-7, entrada 7 V y rieles globales. |

El archivo raiz `PCB_SALUS_v3.kicad_sch` solo organiza las hojas. Las senales
de aplicacion se intercambian por etiquetas globales y los rieles usan simbolos
de potencia. Antes de crear una hoja nueva, definir su alimentacion, interfaz
y conector asociado.

## Bibliotecas del proyecto

`sym-lib-table` y `fp-lib-table` hacen que el proyecto use bibliotecas locales
de `Libs/` ademas de las bibliotecas estandar de KiCad.

```text
PCB_SALUS_v3/
  Libs/
    Symb/Simbolos.kicad_sym
    Footprints/Footprints.pretty/
    3D/
```

Usar una huella local solo cuando la huella estandar no coincida con el dibujo
mecanico del MPN. Para cada pieza SMD, verificar simbolo, pinout, pad 1,
encapsulado, MPN, fabricante y `LCSC PN`. Los headers THT llevan una huella
estandar de KiCad pero se anotan como `Compra manual` y se excluyen de PCBA.

## Actualizar la PCB

Despues de guardar cambios en las hojas, abrir el editor PCB y usar
`Herramientas -> Actualizar PCB desde el esquematico` (F8). Revisar la lista de
cambios antes de aceptar; no mover ni borrar componentes que ya hayan sido
colocados sin revisar el impacto. Esta accion no reemplaza el DRC.

## Modelos 3D

Los modelos de `Libs/3D/` son utiles para comprobar interferencias mecanicas,
pero no validan pinout, pad mapping ni compatibilidad con JLCPCB.
