# Mapa de submodulos y pinout

Fecha de actualizacion: 2026-07-15.

## Alimentacion

`J5` recibe `5V_SYS` desde el step-down externo. `U9` AP63203WU-7, `L2`, C28,
C30/C31 y C22/C23 generan `+3.3V` para la logica. `J19` recibe `+7V` externo
para los servos; no atraviesa el buck de 3.3 V.

## ESP32-S3

U8 es `ESP32-S3-WROOM-1-N8R2`. Las etiquetas activas del esquema relacionan
las interfaces de la siguiente forma.

| Funcion | Red | GPIO / pin U8 |
|---|---|---|
| I2C SDA / SCL | I2C_SDA / I2C_SCL | GPIO7 / GPIO8 |
| SPI MOSI / MISO / reloj | SPI_MOSI / SPI_MISO / SPI_CLOCK | GPIO11 / GPIO13 / GPIO12 |
| BMI088 CS accel / gyro | CS_ACCEL / CS_GIRO | GPIO9 / GPIO10 |
| BMI088 INT accel / gyro | DR_ACCEL / DR_GIRO | GPIO14 / GPIO15 |
| BTS7960 R / L PWM | R_PWM / L_PWM | GPIO4 / GPIO5 |
| Habilitacion BTS7960 | HBRIDGE_EN | GPIO6 |
| Finales de carrera | FC_LEFT / FC_RIGHT | GPIO1 / GPIO2 |
| RF PPM | RF_PPM | GPIO16 |
| Rele latch / OE | RELAY_LATCH / RELAY_OE | GPIO38 / GPIO39 |
| Servos | SERVO1_PWM / SERVO2_PWM | GPIO40 / GPIO41 |
| Acelerador PWM | THROTTLE_PWM | GPIO21 |
| UART0 | U0TX / U0RX | TXD0 / RXD0 |
| UART1 | U1_TX / U1_RX | senales expuestas en J4; validar asignacion final en firmware |
| Arranque / reset | BOOT / RESET | GPIO0 / EN |

## USB y programacion

| Interfaz | Conector | Red | Funcion |
|---|---|---|---|
| UART0 USB | J3 | USB_DP / USB_DM | CP2102N U3, UART0 y autoprogramacion Q3/Q4. |
| USB nativo | J16 | USB2_DP / USB2_DM | D- y D+ nativos del ESP32-S3. |
| Debug manual | J1 | U0TX, U0RX, RESET, BOOT | Programacion y diagnostico alternativo. |
| UART1 | J4 | U1_TX, U1_RX, GND | Interfaz externa de tres pines. |

D2 protege J3 y D5 protege J16. Ambos USB-C son SMD para JLCPCB; todos los
demas conectores son headers THT de soldadura manual.

## Sensores

- `U4` BMI088 usa `IMU_3.3`, SPI compartido y CS separados. SDO1 y SDO2 se
  unen a `SPI_MISO`; la seleccion exclusiva depende de `CS_ACCEL` y `CS_GIRO`.
- `J2` conecta AS5600 y `J12/J13` exponen I2C externo: +3.3V, GND, SDA, SCL.
- `J7/J8` son finales de carrera en `FC_LEFT/FC_RIGHT`.
- `J14` recibe `HALL_A`, `HALL_B`, `HALL_C` y GND.
- `J11` corresponde al acelerador y `J15` al receptor RF PPM.

## Actuadores

- `J6` conecta el BTS7960 con GND, +5V, dos EN y `L_PWM/R_PWM`; los pines IS
  siguen sin conectar. Ver [Puente H BTS7960](04_PUENTE_H_BTS7960.md).
- `U5` SN74HC595 y `U6` ULN2003A forman el expansor de salidas para J9/J10.
- `J17` es SERVO2 y `J18` es SERVO1: pin de +7V, GND y PWM segun el orden
  dibujado. Confirmar orden de conector y corriente de servo antes del PCB.

## Pendientes de interfaz

- R2/R3 y el acondicionamiento de finales de carrera requieren valor.
- Nombrar las cargas finales de J9/J10 y la salida de acelerador.
- Definir el modulo GPS RTK, su conector, protocolo y alimentacion.
- Unificar las etiquetas HBRIDGE_EN/HB_EN en la proxima correccion electrica.
