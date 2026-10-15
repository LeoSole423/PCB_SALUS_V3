# PCB SALUS V3

PCB de control para el robot Ackermann SALUS. Esta revision se inspira en la
arquitectura de `Hoja-Base`, pero usa un ESP32-S3 y se mantiene como un diseno
independiente.

## Abrir el proyecto

En KiCad 10, abre `PCB_SALUS_v3.kicad_pro`. El esquema raiz contiene tres
hojas jerarquicas activas: `ESP32`, `SENSORES` y `ALIMENTACION`.

El diseño actual corresponde a `fabricacion/actual/JLCPCB_2026-10-15_SALUS_v3_D9_DNP/`.
Incluye cuatro agujeros M3 NPTH, contorno redondeado y R4 de 120 ohm montada
como terminacion RS-485. El sufijo R4 identifica esa resistencia. Las fuentes
en `origen/` coinciden con los archivos de trabajo al registrar este paquete.

Los informes archivados del 20 de agosto registran cero conexiones sin rutear
y cero errores DRC/ERC, con avisos e ignorados documentados. Esto no sustituye
la validacion electrica ni las pruebas de banco. Antes de pedir, seguir
`README-pedido.txt` y revisar el montaje en el visor JLCPCB.

`JLCPCB_2026-08-20_SALUS_v3/` conserva la exportacion anterior del mismo dia,
sin R4 montada; los paquetes de julio y del 12 de agosto son historicos.

## Organización

- [Mapa del repositorio](docs/09_ORGANIZACION_REPOSITORIO.md).
- [Índice de fabricación](fabricacion/README.md): entrega actual, históricas y cotizaciones.
- [Archivo histórico](archivo/README.md): respaldos, v2 y exportaciones antiguas.
- `referencias/jlcpcb/`: plantillas XLSX del proveedor.

## Arquitectura actual

- `U8`: ESP32-S3-WROOM-1-N8R2.
- `U1`: LDO AMS1117CD-3.3; J5 alimenta `5V_SYS` mediante D7; D9 se conserva como DNP y USB J16 no alimenta la lógica.
- `JP1` cerrado alimenta `+3.3V` desde el LDO; `JP2` abierto permite una
  fuente alternativa por J20 con selección de puentes apropiada.
- J16 es USB nativo; J1 es debug UART0, J3/J21 son RS-485 mediante U2.
- BMI088, I2C, interfaz BTS7960, siete salidas de relé, Hall, finales,
  acelerador y PPM. Receptor RC previsto: FlySky FS-iA6B.
- J19 recibe 7 V externos para J17/J18; no hay conversión de potencia de tracción.

La [revisión completa del 15/10/2026](docs/reviews/2026-10-15/REVISION_COMPLETA.md)
registra los límites actuales: no hay aprobación incondicional para fabricar
ni integrar. Resolver especialmente el rango del LM358, alimentación e interfaces.
La documentación histórica que menciona U9 buck o U3 CP2102N describe etapas anteriores.

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

## Decisiones de integración

El [registro del 15/10/2026](docs/reviews/2026-10-15/DECISIONES_Y_PENDIENTES.md) distingue decisiones y cambios pendientes: conservar el lineal de 3.3 V, USB Serial/JTAG para la Jetson y no añadir detección VBUS. D9 ya está marcado DNP en esquema y PCB y excluido del montaje de la entrega actual. Sus pads/pistas permanecen; no montar ni puentear D9.
