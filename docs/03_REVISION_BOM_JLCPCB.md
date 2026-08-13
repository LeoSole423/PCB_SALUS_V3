# Revision de BOM y huellas para JLCPCB

Fecha de revision: 2026-07-15.

## Alcance

Se revisaron `ESP32.kicad_sch`, `SENSORES.kicad_sch` y
`ALIMENTACION.kicad_sch`. Todos los SMD con valor definido tienen huella, MPN,
fabricante y `LCSC PN`. La excepcion es `R2/R3`: su valor sigue siendo `R`, por
lo cual quedan sin pieza de compra y no se deben montar.

Los stocks son una fotografia del 2026-07-15. Confirmar disponibilidad, precio,
Basic/Extended y elegibilidad Standard PCBA al preparar el pedido final.

El pedido debe configurarse como `Standard PCBA`, cara superior. U4 (BMI088)
y U8 (ESP32-S3-WROOM-1-N8R2) requieren esta modalidad de ensamblaje; Economic
PCBA no es una opcion valida para esta placa.

## Piezas criticas

| Referencias | MPN / LCSC PN | Huella | Categoria JLC | Stock observado | Decision |
|---|---|---|---|---:|---|
| U8 | ESP32-S3-WROOM-1-N8R2 / C2913204 | RF_Module:ESP32-S3-WROOM-1 | Extended, Standard | 17,776 | Keep-out de antena obligatorio. |
| U9 | AP63203WU-7 / C780769 | TSOT-23-6 | Extended | 615 | Buck fijo de 3.3 V. |
| L2 | FXL0530-4R7-M / C177246 | L_Changjiang_FXL0530 | Extended | 150,986 | 4.7 uH, 4.5 A nominal, 5 A Isat. |
| C28 | CL21A106KPFNNNE / C17024 | 0805 | Extended | 1,868,129 | 10 uF para entrada del buck. |
| C30,C31 | CL21A226MAQNNNE / C45783 | 0805 | Extended | 5,389,915 | 22 uF; reemplaza MPN erroneo de 10 uF. |
| U3 | CP2102N-A02-GQFN24R / C969151 | QFN-24-EP 4x4 | Extended | 5,744 | USB-UART y pad expuesto a GND. |
| U4 | BMI088 / C194919 | Bosch LGA-16 4.5x3 | Extended, Standard | 2,378 | Verificar orientacion, desacople y placement. |
| J3,J16 | GT-USB-7010ASV / C2988369 | USB-C G-Switch | Extended | 32,723 | Un conector UART0 y uno USB nativo. |
| D2,D5 | SP0503BAHTG / C3040626 | SOT-143 | Extended | 28,729 | TVS USB, colocar junto al conector correspondiente. |

## Pasivos consolidados

| Valor | MPN / LCSC PN | Huella | Referencias de esta revision |
|---|---|---|---|
| 100 nF | CC0603KRX7R9BB104 / C14663 | 0603 | C6,C7,C12,C13,C15,C17-C23 |
| 10 uF | CL21A106KPFNNNE / C17024 | 0805 | C5,C8,C28 |
| 22 uF | CL21A226MAQNNNE / C45783 | 0805 | C30,C31 |
| 22 ohm | 0603WAF220JT5E / C23345 | 0603 | R27,R28 |
| 330 ohm | 0603WAF3300T5E / C23138 | 0603 | R11,R18,R20 |
| 4.7 kohm | 0603WAF4701T5E / C23162 | 0603 | R21 |
| 10 kohm | 0603WAF1002T5E / C25804 | 0603 | R1,R8,R9,R12-R16,R22-R24,R34,R36 |
| 47 kohm | 0603WAF4702T5E / C25819 | 0603 | R17,R19 |
| 100 kohm | 0603WAF1003T5E / C25803 | 0603 | R35 |

Los restantes SMD ya conservaban MPN/LCSC validos en el esquema. `R2` y `R3`
mantienen huella 0603 pero no se incluyen como linea de compra hasta definir su
valor electrico.

## Conectores THT manuales

| Referencias | Huella | Uso |
|---|---|---|
| J1,J9,J10 | Header vertical 1x06 P2.54 mm | Debug y cargas. |
| J2,J12,J13,J14 | Header vertical 1x04 P2.54 mm | I2C y sensores. |
| J4,J15,J17,J18 | Header vertical 1x03 P2.54 mm | UART, RF y servos. |
| J5,J7,J8,J11,J19 | Header vertical 1x02 P2.54 mm | Entradas, sensores y 7 V. |
| J6 | Header vertical 2x04 P2.54 mm | BTS7960. |

Todos estan anotados como `Compra manual`; excluirlos de BOM y CPL de JLCPCB.

## Verificacion mecanica pendiente

- Mantener el keep-out de antena de U8 libre de cobre, vias, pistas y metal.
- Colocar D2/D5 antes de las pistas USB y adyacentes a J3/J16.
- Colocar C28, C30/C31 y L2 segun el loop corto VIN-SW-L-COUT de U9.
- Revisar la corriente admisible de J19, J17, J18 y sus pistas antes de usar
  servos con picos cercanos a 5 A.
