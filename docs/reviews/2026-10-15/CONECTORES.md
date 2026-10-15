# Pinout de conectores — 15/10/2026

Redes del netlist nativo KiCad; dirección de TX/RX desde la perspectiva de la placa. Los nombres jerárquicos se conservaron. No sustituye el dibujo del cable/hembra ni acredita tolerancia5V.

| Conector | Valor | Pin → red |
|---|---|---|
| J1 | Debug_U0 | 1: GND; 2: +5V; 3: /ESP32/U0TX; 4: /ESP32/U0RX; 5: /ESP32/RESET; 6: /ESP32/BOOT |
| J2 | S_GIRO | 1: +3.3V; 2: GND; 3: I2C_SDA; 4: I2C_SCL |
| J3 | RS485 | 1: +5V; 2: GND; 3: /ESP32/RS485_A; 4: /ESP32/RS485_B |
| J4 | Uart1 | 1: /ESP32/U1_TX; 2: /ESP32/U1_RX; 3: GND |
| J5 | 5V_IN | 1: +5V; 2: GND |
| J6 | IBT_2 | 1: GND; 2: +5V; 3: unconnected-(J6-Pin_3-Pad3); 4: unconnected-(J6-Pin_4-Pad4); 5: HBRIDGE_EN; 6: HBRIDGE_EN; 7: L_PWM; 8: R_PWM |
| J7 | FC1 | 1: FC_LEFT; 2: GND |
| J8 | FC2 | 1: FC_RIGHT; 2: GND |
| J9 | RELES_1 | 1: +5V; 2: Net-(J9-Pin_2); 3: Net-(J9-Pin_3); 4: Net-(J9-Pin_4); 5: Net-(J9-Pin_5); 6: GND |
| J10 | RELES_2 | 1: +5V; 2: Net-(J10-Pin_2); 3: Net-(J10-Pin_3); 4: Net-(J10-Pin_4); 5: unconnected-(J10-Pin_5-Pad5); 6: GND |
| J11 | Throttle | 1: /SENSORES/THROTTLE_OUT; 2: GND |
| J12 | I2C_EXT1 | 1: GND; 2: +3.3V; 3: I2C_SDA; 4: I2C_SCL |
| J13 | I2C_EXT2 | 1: GND; 2: +3.3V; 3: I2C_SDA; 4: I2C_SCL |
| J14 | S_HALL | 1: HALL_A; 2: HALL_B; 3: HALL_C; 4: GND |
| J15 | RF_PPM | 1: GND; 2: +5V; 3: Net-(J15-Pin_3) |
| J16 | USB_NATIVO | A1: GND; A12: GND; A4: USB2_VBUS; A5: Net-(J16-CC1); A6: /ESP32/USB2_D+; A7: /ESP32/USB2_D-; A8: unconnected-(J16-SBU1-PadA8); A9: USB2_VBUS; B1: GND; B12: GND; B4: USB2_VBUS; B5: Net-(J16-CC2); B6: /ESP32/USB2_D+; B7: /ESP32/USB2_D-; B8: unconnected-(J16-SBU2-PadB8); B9: USB2_VBUS; SH: GND |
| J17 | SERVO2 | 1: GND; 2: +7V; 3: Net-(J17-Pin_3) |
| J18 | SERVO1 | 1: GND; 2: +7V; 3: Net-(J18-Pin_3) |
| J19 | +7V_IN | 1: +7V; 2: GND |
| J20 | 3V_IN | 1: /ALIMENTACION/3.3V_EXT; 2: GND |
| J21 | RS485 | 1: +5V; 2: GND; 3: /ESP32/RS485_A; 4: /ESP32/RS485_B |
| J22 | GPIOS_AUX | 1: +3.3V; 2: GND; 3: /ESP32/IO47; 4: /ESP32/IO48; 5: /ESP32/IO3; 6: /ESP32/IO46; 7: /ESP32/IO45 |

J4 comparte las redes UART del transceptorRS485. J10.5 estáNC. Los conectores físicos y cables deben cotejarse mirando la orientación correcta.
