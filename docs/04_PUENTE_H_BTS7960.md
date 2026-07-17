# Puente H BTS7960 para direccion

## Alcance

`J6` conecta la PCB SALUS V2 con un modulo externo IBT-2 basado en dos
BTS7960. El modulo conmuta la potencia del motor delantero; la PCB solo entrega
logica de 5 V y senales de control. La corriente del motor no debe circular por
la PCB SALUS ni por este conector de senales.

## Conexion actual de J6

| Pin J6 | Red SALUS | Funcion esperada del modulo |
|---|---|---|
| 1 | GND | Masa de logica. |
| 2 | +5V | Alimentacion de la logica del modulo. |
| 3 | Sin etiqueta | R_IS, sensado de corriente de un sentido. |
| 4 | Sin etiqueta | L_IS, sensado de corriente del otro sentido. |
| 5 | HBRIDGE_EN | R_EN. |
| 6 | HBRIDGE_EN | L_EN. |
| 7 | L_PWM | Entrada PWM de un sentido. |
| 8 | R_PWM | Entrada PWM del sentido opuesto. |

La conexion de los dos `EN` a `HBRIDGE_EN` es valida: en bajo deshabilita el
puente y en alto permite operar ambos sentidos. El firmware debe garantizar que
solo uno entre `L_PWM` y `R_PWM` este activo a la vez. Ambos en bajo dejan el
motor sin mando; para un paro seguro, poner `HBRIDGE_EN` en bajo.

Los modulos IBT-2 no tienen una numeracion fisica universal. Antes de conectar
la primera vez, comparar la serigrafia del modulo real y el pin 1 del cable con
esta tabla. No usar solo fotos de vendedores como referencia de pinout.

## Recomendaciones de hardware

1. Agregar un pull-down externo de 10 kOhm desde `HBRIDGE_EN` a GND. Deja el
   puente deshabilitado mientras el ESP32 arranca, se resetea o queda sin
   alimentacion.
2. Agregar pull-downs de 10 kOhm desde `L_PWM` y `R_PWM` a GND. Evitan pulsos
   de mando durante el arranque. No usar pull-ups a 5 V en estas redes: pueden
   retroalimentar un ESP32 apagado.
3. Si el cable entre PCB y modulo no es muy corto, agregar resistores serie de
   100 a 330 Ohm en `HBRIDGE_EN`, `L_PWM` y `R_PWM`, ubicados en la PCB SALUS.
   Reducen ringing, EMI y corriente de ESD hacia el ESP32.
4. Considerar un TVS de baja capacitancia para las tres senales y GND si el
   cable sale de una caja protegida o supera aproximadamente 20 cm. No es
   obligatorio para un cable interno corto, pero mejora robustez en un robot.
5. El modulo debe tener cerca de sus bornes `B+` y `B-` un capacitor ceramico de
   100 nF y un electrolitico low-ESR de al menos 470 uF, ambos con tension
   nominal superior al riel del motor. La foto muestra un electrolitico en el
   modulo; comprobar valor, tension y distancia real a los bornes. Estos
   capacitores no reemplazan la proteccion ni el filtrado del riel de motor.
6. Unir GND de logica y el negativo de potencia del modulo en el sistema, pero
   llevar el retorno de corriente de motor directamente a la distribucion de
   potencia. No usar la masa de J6 ni la PCB SALUS como retorno de motor.

El BTS7960 admite entradas logicas compatibles con 3.3 V en aplicaciones
tipicas. Aun asi, se debe probar con el modulo real y limitar la prueba inicial
con fuente de laboratorio: los modulos clon pueden variar en sus redes de
entrada.

## Uso de R_IS y L_IS

Cada BTS7960 tiene un pin `IS`: es una fuente de corriente proporcional a la
corriente del lado alto activo y tambien comunica fallas. No es una salida
digital. En el IC original, la relacion nominal es `I_motor / I_IS = 8500`; un
resistor externo de 1 kOhm a GND produciria aproximadamente
`V_IS = I_motor / 8.5 A` en operacion normal. Durante una falla, la salida
indica el estado mediante una corriente limitada.

En modulos IBT-2 el resistor de conversion puede estar ya instalado y su valor
no es consistente entre clones. Por eso, antes de llevar `IS` a un ADC:

1. Con el modulo apagado, medir resistencia entre cada `R_IS`/`L_IS` y GND.
2. Con fuente limitada y motor sin carga, medir la tension `IS` para una
   corriente conocida.
3. Confirmar que la tension maxima, incluidos transitorios, nunca supera 3.3 V.
4. Solo entonces conectar a un ADC1 del ESP32, preferentemente GPIO36
   (`SENSOR_VP`) y GPIO39 (`SENSOR_VN`), que no compiten con Wi-Fi.

Si se usan los dos canales, proponer en la proxima iteracion: etiqueta
`HBRIDGE_R_IS` y `HBRIDGE_L_IS`, resistor serie de 4.7 kOhm a 10 kOhm hacia el
ADC, capacitor de 10 nF a GND en el lado del ADC y clamp a 3.3 V validado para
la corriente de falla. No conectar `IS` directamente al ESP32 hasta medir el
modulo real, porque un nivel de 5 V puede danar su ADC.

La medicion solo representa el semicircuito que esta conduciendo. Debe leerse
el canal asociado al sentido ordenado y calibrarse en software; no sustituye un
sensor de corriente de precision ni una proteccion primaria de sobrecorriente.

## Estado de revision

- `J6` usa `PinHeader_2x04_P2.54mm_Vertical`. Es un header THT vertical de
  montaje manual: JLCPCB debe fabricar los agujeros y pads, pero no montarlo.
  Debe excluirse de la BOM y CPL de ensamblaje JLCPCB.
- Los pines 3 y 4 quedaron como redes sin etiqueta. Si no se usaran ahora,
  colocar marcadores `No connect`; si se reservaran, etiquetarlos como
  `HBRIDGE_R_IS` y `HBRIDGE_L_IS`.
- La relacion completa con la ESP32 y el resto de los conectores esta en el
  [mapa de submodulos y pinout](05_MAPA_DE_SUBMODULOS_Y_PINOUT.md).

## Fuente tecnica

- [Datasheet oficial BTS7960 de Infineon](https://www.infineon.com/assets/row/public/documents/10/57/infineon-bts7960-ds-en.pdf): funcion de `IS`, relacion nominal de corriente y diagnostico.
