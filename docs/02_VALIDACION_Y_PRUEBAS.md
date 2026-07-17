# Validacion y pruebas

## Estado de V3

La V3 cambio el ESP32 clasico y el LDO TLV757 por ESP32-S3 y buck AP63203WU-7.
Por ello, los resultados SPICE historicos de V2 sobre TLV757, OR por diodos y
ESP32-WROOM-32E no son evidencia de funcionamiento de V3 y no deben usarse
para aprobar esta revision.

| Bloque | Estado | Evidencia disponible | Pendiente |
|---|---|---|---|
| Jerarquia KiCad | Revisado | El esquema raiz exporta BOM y netlist con tres hojas. | ERC/DRC final tras ruteo. |
| Buck 5 V a 3.3 V | Revisado en esquema | U9 AP63203WU-7, L2 4.7 uH, C28 10 uF, C30/C31 22 uF y C22/C23 100 nF estan presentes. | Validar layout, arranque, ripple, temperatura y carga real. |
| USB-C UART0 | Revisado en esquema | J3, D2, CP2102N y Q3/Q4 estan presentes. | Enumeracion, carga de firmware y autoprogramacion en banco. |
| USB-C nativo | Revisado en esquema | J16, D5, USB2_DP y USB2_DM estan presentes. | Enumeracion USB nativa y compatibilidad de firmware. |
| ESP32-S3 | Revisado en BOM | U8 fijado como N8R2. | RF, antena, arranque, consumo y perifericos en placa. |
| IMU BMI088 | Revisado en esquema | Alimentacion IMU_3.3, SPI y CS separados. | Comunicacion, calibracion y vibracion en robot. |
| Servos | Pendiente | J17/J18 y J19 estan dibujados. | Corriente, caida de tension, conector/cable y ruido de retorno. |

## ERC registrado

La corrida del 2026-07-15 produjo seis advertencias y ningun error no excluido.

| Hoja | Aviso | Tratamiento en esta etapa |
|---|---|---|
| `ESP32` | Cuatro avisos de tipo de pin de SW1/SW2 frente a pines pasivos o de potencia. | Documentados; corresponden a la definicion de los simbolos de boton y no se cambia el circuito en esta etapa. |
| `SENSORES` | `HBRIDGE_EN` y `HB_EN` nombran la misma red. | Documentado; unificar etiqueta en una futura correccion electrica. |
| `SENSORES` | Conflicto de salida compartida en `SPI_MISO` de BMI088. | Excluido intencionalmente: SDO1/SDO2 comparten MISO y los CS separados seleccionan un sensor por vez. |

## Plan de prueba fisica

1. Alimentar `J5` con 5 V y limite inicial de corriente bajo.
2. Medir `5V_SYS`, `+3.3V` y la temperatura de U9/L2 sin cargas externas.
3. Aplicar carga escalonada al buck y medir ripple de 3.3 V con osciloscopio.
4. Probar por separado J3/CP2102N y J16/USB nativo con PC.
5. Verificar BOOT, RESET y autoprogramacion por UART0.
6. Conectar IMU, I2C y sensores de uno en uno.
7. Conectar los servos con fuente de 7 V limitada; medir picos y caida de
   tension antes de probarlos en el robot.

## Criterio de actualizacion

Cada resultado debe registrar fecha, configuracion, instrumento, limite de
corriente, mediciones y conclusion. Un bloque no se considera probado en robot
sin haber superado primero la prueba de banco.
