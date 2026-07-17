# Contexto de PCB SALUS V3

## Objetivo

SALUS V3 es la placa de control de bajo nivel para un robot Ackermann. La
Jetson Orin Nano conserva las tareas de alto nivel y el ESP32-S3 se ocupa de
FreeRTOS, adquisicion de sensores, PID, entradas, salidas y comunicaciones de
campo. La placa no controla directamente la potencia de traccion.

## Arquitectura confirmada

```text
Jetson Orin Nano <--> USB / UART segun interfaz <--> ESP32-S3
                                                    |-- sensores e IMU
                                                    |-- actuadores de logica
                                                    `-- headers de servo

Step-down externo 5 V --> J5 --> 5V_SYS --> AP63203WU-7 --> +3.3V
Step-down externo 7 V --> J19 --> +7V --> J17/J18 (servos)
```

- `U8` es `ESP32-S3-WROOM-1-N8R2`, con 8 MB de flash y 2 MB de PSRAM.
- `U9` es `AP63203WU-7`, buck fijo de 3.3 V desde el riel `5V_SYS`.
- `J3` ofrece USB-C a UART0 mediante `U3` CP2102N y conserva la
  autoprogramacion por `Q3/Q4`.
- `J16` ofrece USB-C nativo del ESP32-S3 mediante `USB2_DP` y `USB2_DM`.
- `J17` y `J18` son headers de tres pines para servo; `J19` recibe el riel de
  7 V externo.

## Ensamblaje JLCPCB

La placa requiere PCBA Standard por el modulo ESP32-S3 y la IMU BMI088. Los
componentes SMD se montaran en la cara superior. Todos los headers son THT y
se compran/sueldan manualmente: permanecen en la PCB para fabricar sus agujeros
metalizados, pero se excluyen de la BOM y CPL de ensamblaje.

Las existencias y precios de JLCPCB son una fotografia de la fecha de revision;
deben comprobarse nuevamente antes del pedido.

## Limites actuales

- `J5` recibe 5 V ya regulados. El esquema activo no implementa corte por
  sobretension, fusible ni TVS de entrada frente a una falla aguas arriba.
- `J19` recibe 7 V ya regulados para los servos. La capacidad de corriente del
  header y del cableado debe confirmarse frente a los picos de servo antes del
  layout final.
- La proteccion de la Jetson y sus 19 V no pertenece a esta placa.
- GPS RTK de doble antena sigue sin modulo, conector, protocolo ni pinout
  definido.
- `R2` y `R3` aun tienen valor `R`; no se pueden comprar ni montar hasta que
  se defina el acondicionamiento de los finales de carrera.

## Principios de diseno

- Mantener potencia de traccion, 7 V de servos y logica de 3.3 V separados en
  placement, retorno de masa y ruteo.
- Respetar el keep-out de antena del ESP32-S3 en todas las capas de cobre.
- Situar TVS junto a cada USB-C y desacoples junto a sus pines de alimentacion.
- Resolver ERC, DRC, fiduciales, puntos de prueba y conexion de entradas
  externas antes de fabricar.
