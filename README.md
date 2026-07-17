# PCB SALUS V3

PCB de control para el robot Ackermann SALUS. Esta revision se inspira en la
arquitectura de `Hoja-Base`, pero usa un ESP32-S3 y se mantiene como un diseno
independiente.

## Abrir el proyecto

En KiCad 10, abre `PCB_SALUS_v3.kicad_pro`. El esquema raiz contiene tres
hojas jerarquicas activas: `ESP32`, `SENSORES` y `ALIMENTACION`.

La PCB esta sincronizada de forma parcial y aun no tiene placement ni ruteo
final. No debe enviarse a fabricar hasta completar la revision electrica,
placement, ruteo, DRC y pruebas de banco.

## Arquitectura actual

- `U8`: ESP32-S3-WROOM-1-N8R2 como controlador de tiempo real e I/O.
- `U9`: buck AP63203WU-7 que convierte `5V_SYS` a `+3.3V`.
- Dos receptaculos USB-C: `J3` para UART0 mediante CP2102N y `J16` para el USB
  nativo del ESP32-S3.
- BMI088, I2C externo, puente BTS7960, salidas de reles, sensores Hall,
  finales de carrera, acelerador, RF PPM, UART1 y dos headers de servo.
- Entrada manual de 5 V por `J5` y entrada manual de 7 V por `J19`.

## Documentacion

- [Contexto del proyecto](docs/00_CONTEXTO_PROYECTO.md)
- [Estructura del esquematico y librerias](docs/01_ESTRUCTURA_ESQUEMATICO_Y_LIBRERIAS.md)
- [Validacion y pruebas](docs/02_VALIDACION_Y_PRUEBAS.md)
- [Revision BOM y huellas JLCPCB](docs/03_REVISION_BOM_JLCPCB.md)
- [Puente H BTS7960](docs/04_PUENTE_H_BTS7960.md)
- [Mapa de submodulos y pinout](docs/05_MAPA_DE_SUBMODULOS_Y_PINOUT.md)
- [Revision V3](docs/06_REVISION_V3_2026-07-15.md)
