# Validacion del filtro PWM del acelerador

Fecha de validacion: 2026-08-13.

## Veredicto

Se adopta `R17 = 47 kOhm`, `C20 = 100 nF`, encapsulados 0603 y PWM de
`20 kHz`. La constante de tiempo se conserva en 4.7 ms y no cambian la
huella, el ruteo ni la colocacion.

La cadena real es `GPIO21 / THROTTLE_PWM -> R17 -> C20 a GND -> U7A` (seguidor)
`-> R18 -> J11 / THROTTLE_OUT`, con `R19` como pull-down de salida. `R35 =
100 kOhm` esta directamente en el GPIO: fija nivel bajo durante arranque, pero
no forma un divisor mientras el GPIO conduce activamente.

| Parametro nominal | Resultado |
|---|---:|
| Constante de tiempo R17-C20 | 4.70 ms |
| Corte de -3 dB | 33.86 Hz |
| Respuesta 10-90 % | 10.33 ms |
| Escala de salida R18/R19 | 0.993028 |
| Salida a 100 % PWM, carga alta Z | 3.27699 V |

El LM358 se alimenta con 5 V. La entrada de 0-3.3 V queda dentro de su rango
de modo comun especificado hasta aproximadamente `V+ - 1.5 V`; la carga de
R18/R19 a fondo de escala es solo unos 70 uA. Esta conclusion depende de que
J11 conecte una entrada de alta impedancia, como se asumio para esta revision.

## Simulacion SPICE

Los bancos reproducibles estan en
[`spice/validar_filtro_acelerador.cir`](../spice/validar_filtro_acelerador.cir)
y [`spice/validar_escalon_acelerador.cir`](../spice/validar_escalon_acelerador.cir).
Modelan GPIO de baja impedancia, R35, el RC, un seguidor ideal U7A y la salida
R18/R19. La idealizacion del seguidor es valida para el filtro de 33.86 Hz;
la ganancia-ancho de banda nominal del LM358 es muy superior a esa frecuencia.

Resultados transitorios con ngspice:

| PWM | Ciclo util | Salida media | Rizado pico a pico |
|---:|---:|---:|---:|
| 20 kHz | 0 % | 0 V | 0 V |
| 20 kHz | 10 % | 0.32774 V | 3.18 mV |
| 20 kHz | 50 % | 1.63852 V | 8.77 mV |
| 20 kHz | 90 % | 2.94934 V | 3.22 mV |
| 20 kHz | 100 % | 3.27699 V | 0 V |

El escalon de 0 a 100 % simulado mide 10.327 ms entre 10 y 90 %. Por lo tanto,
el caso de peor rizado nominal a 20 kHz es 8.77 mVpp (0.27 % de 3.3 V): cumple
el limite de 15 mVpp y la respuesta esperada para un mando mecanico.

La comparacion de frecuencia se calculo con la respuesta periodica exacta del
RC, validada por SPICE en 10, 20, 40 y 80 kHz; el maximo ocurre a 50 % de ciclo
util. Se expresa en J11, despues del divisor R18/R19.

| Frecuencia PWM | Rizado maximo a 50 % |
|---:|---:|
| 10 kHz | 17.43 mVpp |
| 20 kHz | 8.72 mVpp |
| 40 kHz | 4.36 mVpp |
| 80 kHz | 2.18 mVpp |
| 100 kHz | 1.74 mVpp |

Subir el PWM disminuye el rizado, pero no resuelve un problema presente. A
cambio, reduce la resolucion de duty util del temporizador LEDC de la
ESP32-S3: con un reloj de 80 MHz, la condicion `frecuencia x 2^bits <= 80 MHz`
permite como maximo 11 bits a 20 kHz, 10 bits a 40 kHz y 9 bits a 80 kHz. Se
mantiene 20 kHz.

## Tolerancias y margen

Para un caso conservador se uso R17 a -1 %, C20 a -10 % y una reduccion
adicional de 15 % de capacidad por sesgo DC: `R = 46.53 kOhm`, `C = 76.5 nF`.
SPICE entrega 11.52 mVpp a 20 kHz y 50 %, aun inferior a 15 mVpp. El tiempo
10-90 % queda aproximadamente entre 7.8 y 11.4 ms en los extremos pasivos;
mas rapido que el nominal no perjudica la respuesta del acelerador.

La corriente de polarizacion del LM358 es tipicamente 20 nA. Incluso usando
250 nA como cota conservadora, R17 puede introducir hasta 11.75 mV de error
DC; es aceptable para una escala de 3.3 V, pero reduce el margen frente a la
solucion original de 4.7 kOhm.
La salida a 100 % se reduce por R18/R19, no por el filtro; una carga externa
de baja impedancia reduciria esa tension y requeriria redisenar la etapa de
salida. No conectar J11 a una carga baja sin revisar ese supuesto.

## Coste y tamano

`R17 = 47 kOhm` y `C20 = 100 nF` conserva exactamente `RC = 4.7 ms`. Ambos
son 0603 y no reducen area de PCB. Se eligieron C25819 para R17 y C14663 para
C20: son piezas Basic de JLCPCB, al igual que C14663 para los otros once
capacitores de 100 nF.

La mayor impedancia aumenta la susceptibilidad a ruido y el error por corriente
de polarizacion indicado arriba. Se acepta para la entrada de alta impedancia
de J11 a cambio de eliminar C1590 y C108463, dos referencias Extended. El
ahorro estimado para cinco PCBA es USD 5.60; confirmar precio y disponibilidad
antes de pagar en [LCSC para C14663](https://www.lcsc.com/product-detail/Multilayer-Ceramic-Capacitors-MLCC-SMD-SMT_YAGEO-CC0603KRX7R9BB104_C14663.html).

## Criterio de banco antes de integrar

1. Con J11 sin carga, medir a 0, 10, 50, 90 y 100 % de PWM con sonda x10 y
   masa corta; esperar los valores medios de la tabla y menos de 15 mVpp.
2. Confirmar que el controlador conectado a J11 acepta 0-3.3 V y presenta alta
   impedancia en toda la escala.
3. Arrancar y resetear la ESP32 verificando que R35 mantiene la salida proxima
   a 0 V hasta que el firmware configure GPIO21.
