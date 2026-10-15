# PCB SALUS V3

PCB de control para el robot Ackermann SALUS. Esta revision se inspira en la
arquitectura de `Hoja-Base`, pero usa un ESP32-S3 y se mantiene como un diseno
independiente.

## Abrir el proyecto

En KiCad 10, abre `PCB_SALUS_v3.kicad_pro`. El esquema raiz contiene tres
hojas jerarquicas activas: `ESP32`, `SENSORES` y `ALIMENTACION`.

El diseño actual corresponde a `fabricacion/JLCPCB_2026-08-20_SALUS_v3_R4/`.
Incluye cuatro agujeros M3 NPTH, contorno redondeado y R4 de 120 ohm montada
como terminacion RS-485. El sufijo R4 identifica esa resistencia. Las fuentes
en `origen/` coinciden con los archivos de trabajo al registrar este paquete.

Los informes archivados del 20 de agosto registran cero conexiones sin rutear
y cero errores DRC/ERC, con avisos e ignorados documentados. Esto no sustituye
la validacion electrica ni las pruebas de banco. Antes de pedir, seguir
`README-pedido.txt` y revisar el montaje en el visor JLCPCB.

`JLCPCB_2026-08-20_SALUS_v3/` conserva la exportacion anterior del mismo dia,
sin R4 montada; los paquetes de julio y del 12 de agosto son historicos.

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
- [Generacion CPL auditable KiCad → JLCPCB](docs/07_CPL_AUDITABLE_KICAD_JLCPCB.md)
- [Validacion del filtro PWM del acelerador](docs/08_VALIDACION_FILTRO_ACELERADOR_PWM.md)

## CPL para JLCPCB

Para toda exportación futura de montaje usar exclusivamente
`tools/jlc_cpl.py` y el perfil versionado `config/jlcpcb-cpl.json`. La guía
incluye el flujo reproducible para agentes, auditoría de centroides y
calibración desde el visor de JLCPCB. No editar rotaciones o posiciones
directamente en un CSV.
