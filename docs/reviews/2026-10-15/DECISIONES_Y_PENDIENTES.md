# Decisiones y pendientes — 15/10/2026

Este registro incorpora las decisiones del operador posteriores a la revisión. Las decisiones de arquitectura no implican modificaciones ya realizadas al circuito. Base de revisión: `5d39f71`. Actualización posterior: D9 marcado DNP en esquema/PCB y excluido de BOM/CPL; entrega `fabricacion/actual/JLCPCB_2026-10-15_SALUS_v3_D9_DNP/`.

## Decisiones adoptadas

- Conservar el regulador lineal de 3.3 V. Se priorizan presupuesto y sencillez; no se añadirá un buck en la PCB. La decisión no sustituye la validación térmica y de dropout.
- Los 5 V y 7 V provienen de bucks externos desde la batería de 48 V. La selección y dimensionamiento de esos bucks queda fuera de esta revisión por indicación del operador.
- La carga de 3.3 V corresponde a componentes internos. Estimación preliminar de consumo normal: 150–250 mA; picos orientativos de 400–450 mA. Son estimaciones, no mediciones ni máximos garantizados. Ver informe térmico para escenarios de 250–300 mA sostenidos y sensibilidad a carga/temperatura.
- USB servirá para comunicación bidireccional con la Jetson, programación y depuración. La alimentación normal de la PCB vendrá del buck; no se desea alimentación desde VBUS ni retorno de potencia hacia la Jetson.
- Se adopta USB Serial/JTAG como modo inicial previsto del ESP32-S3. Permite puerto serie y JTAG simultáneos; flashear reinicia/interrumpe la aplicación. La implementación del protocolo del robot por USB está pendiente.
- No añadir detección de VBUS, por decisión explícita del operador. GPIO auxiliares permanecen disponibles. USB OTG/TinyUSB con alimentación propia requeriría revisar nuevamente la detección; no se declara cubierto ese caso ni la función USB host.
- La modificación propuesta es eliminar la ruta de potencia de D9 (no sustituir el diodo por un puente), conservando D7, D+/D−, GND, resistencias CC y protección USB. **Aplicado como DNP en esquema y PCB; excluido de BOM/CPL de la nueva entrega**. Sin buck y tras desconectar D9, USB no alimentará la lógica ni permitirá programarla sin alimentación externa.
- Conservar BOOT/RESET accesibles para recuperación. No deshabilitar mediante eFuses las funciones necesarias de programación/depuración. El bloqueo de potencia no es aislamiento galvánico: USB comparte GND.
- Módulo previsto: ESP32-S3-WROOM-1-N8R2. J22 expone GPIO3/45/46 (strapping, uso condicionado por arranque) y GPIO47/48 (sin esa restricción en N8R2). No tratar todos los pines de J22 como intercambiables ni tolerantes a 5 V.
- Receptor RC: FlySky FS-iA6B. Su amplitud PPM sigue pendiente de medición; alimentación y amplitud lógica no son equivalentes.
- Acelerador: el controlador alcanza la aceleración máxima con la señal actual de 3.3 V; no se exige salida de 5 V ni ganancia adicional por ese motivo. El firmware clásico limita el duty y mantiene un mínimo distinto de cero. Validar el comportamiento del nuevo filtro y buffer sin cambiar esa calibración por inferencia.

## Estado del firmware

`/home/leosole/Desktop/SALUS/ESP32_SALUS` es el firmware clásico: PlatformIO `esp32dev`, comunicación del robot por UART. No es todavía el firmware operativo del nuevo S3.

`/home/leosole/Desktop/SALUS/salus-esp32s3-fw` es un esqueleto ESP-IDF. Su `sdkconfig` local habilita USB Serial/JTAG como consola secundaria, pero esa elección no está fijada en `sdkconfig.defaults`. Falta portar comportamiento, mapa de pines, protocolo, seguridad y verificar el binario real. Una consola secundaria no acredita comunicación bidireccional del protocolo del robot.

## Pendientes para cerrar el diseño y validar la primera placa

1. D9 DNP aplicado y BOM/CPL comprobados (63 SMD, D7 incluido). Verificar ausencia física de D9 al recibir el montaje. Definir alimentación externa durante programación y verificar encendido/apagado de Jetson y PCB en ambos órdenes.
2. Fijar la configuración USB Serial/JTAG del firmware S3, implementar comandos/telemetría, y probar comunicación, flasheo, JTAG y recuperación BOOT/RESET desde la Jetson. Revisar comportamiento al desconectar USB y apagar cada equipo; no se garantiza fuga cero por retirar D9.
3. Medir corriente media/picos, entrada real de U1 después de D7, estabilidad/ripple de 3.3 V y temperatura interna/U1 con carga representativa. El informe térmico contiene escenarios, no una temperatura máxima garantizada del robot.
4. Validar acelerador filtrado: margen del LM358 con tensión mínima/temperatura, rango y carga de entrada del controlador, respuesta y estado seguro al arrancar/resetear/perder alimentación.
5. Cerrar interfaces: amplitud PPM del FS-iA6B y divisor; niveles de Hall; módulos de relé y protección de bobinas; pull-ups I2C; uso exclusivo o habilitación de UART J4 compartida con RS485; umbral PWM y corriente/cableado de servos.
6. Cerrar fabricación/mecánica: disponibilidad o sustitución de U6 ULN2003BDR; dibujo exacto de pulsadores y USB; especificación de conectores; desplazamiento de 0.5 mm de H2; rieles/fiduciales y montaje.
7. Después de cambios de diseño, repetir ERC/DRC/paridad y generar un paquete nuevo BOM/CPL/Gerbers. El paquete D9_DNP incorpora esa exclusión de montaje; otros pendientes de diseño y validación siguen abiertos. Realizar pruebas de banco, integridad USB/ESD y ruido proporcionales a la instalación, sin movimiento no autorizado.

## Referencias

- [Revisión completa](REVISION_COMPLETA.md), con hallazgos y evidencia de los archivos actuales.
- [Revisión térmica](thermal/REVISION_TERMICA_3V3.md).
- [USB Serial/JTAG de Espressif](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/usb-serial-jtag-console.html).
- [TinyUSB y detección de VBUS en dispositivos autoalimentados](https://docs.espressif.com/projects/esp-idf/en/v5.4.2/esp32s3/api-reference/peripherals/usb_device.html#self-powered-device).
- [Datasheet del módulo y pines de arranque](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf).
