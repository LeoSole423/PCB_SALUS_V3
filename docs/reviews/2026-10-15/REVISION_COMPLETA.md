# Revisión de diseño PCB SALUS v3 — 15/10/2026

> Actualización de decisiones: ver [registro vigente](DECISIONES_Y_PENDIENTES.md). Se conserva el lineal, se prevé USB Serial/JTAG sin detección VBUS y queda pendiente desconectar D9. Las descripciones siguientes reflejan el circuito revisado, todavía sin modificar.

## Dictamen

**La PCB está completamente ruteada y es coherente con el esquema, pero no se aprueba todavía de forma incondicional para fabricar e integrar en el robot.** Hay un margen funcional estrecho en la etapa del acelerador para el firmware actual, y la escala completa0–3.3V no queda garantizada en temperatura y quedan contratos eléctricos de interfaces y alimentación sin cerrar. No encontré un cortocircuito o una inversión de pines entre esquema y PCB en las comprobaciones realizadas.

Esto es una revisión del diseño y de sus archivos de fabricación. No inspecciona soldaduras de una placa física ni acredita funcionamiento en banco, RF, EMC o seguridad del robot.

Base: commit `5d39f71`, paquete `fabricacion/actual/JLCPCB_2026-08-20_SALUS_v3_R4/`, KiCad 10.0.6, kicad-happy `6a91aaea`. La reorganización ya está subida a GitHub. Durante esta revisión no se cambió el circuito, el layout ni las entregas.

## Prioridades antes de aprobar

| ID | Prioridad / confianza | Hallazgo | Cierre necesario |
|---|---|---|---|
| A1 | Media con firmware actual / alta en cálculo | PWM actual62..228/255 produce máximo medio2.951V: dentro del límite nominal3.0V del LM358, pero con solo49mV de margen. Duty100% futuro sí lo excedería. No hace falta entregar5V. | Validar alimentación mínima, tolerancias, carga y calibración del acelerador filtrado; valorar operacional con más margen. |
| A2 | Alta / alta en topología, media en efecto | Alimentación USB puede encender ESP32 sin alimentar el LM358. | Aplicar desconexión de D9 decidida para USB de datos/programación/depuración; validar secuencia y salida segura. |
| A3 | Alta / media | AMS1117 después de SS14: margen de dropout y temperatura no demostrado a carga máxima. | Presupuesto de consumo y ensayo con peor entrada, carga y ambiente. |
| A4 | Alta condicional / alta | Hall usa solo 1 kΩ serie; no adapta una salida push-pull de 5 V. | Modelo y nivel de sensores; adaptación o pull-ups/protección adecuados. |
| A5 | Media condicional / alta | PPM con divisor no garantiza HIGH para señal externa de 3.3 V. | Definir receptor, amplitud y tolerancias o revisar interfaz. |
| A6 | Media condicional / alta | I2C no tiene pull-ups propios. | Identificar pull-ups en módulos y validar tensión, capacitancia y velocidad. |
| A7 | Alta condicional / alta | ULN2003 COM está NC; no protege bobinas directas con sus diodos internos. | Confirmar módulos de relé con driver/clamp o incorporar protección correcta. |
| A8 | Alta de fabricación / alta | U6 tiene MPN ULN2003BDR, obsoleto según TI. | Disponibilidad del lote o sustitución controlada y revalidada. |
| A9 | Media / alta en ausencia de datos | Corriente de servos, conectores y cableado sin especificación cerrada. | Corriente de bloqueo/pico y validación térmica/caída de tensión. |
| A10 | Media / alta | H2 está desplazado 0.5 mm respecto de la columna de H1. | Cotejar plano mecánico del chasis. |
| A11 | Media / media | Sin fiduciales propios y componentes cerca de bordes. | Coordinar rieles, panelización y referencias de ensamblaje. |
| A13 | Alta condicional / alta | J4 comparte UART con RO/DI del RS485 y puede generar contención si se conecta otro transmisor. | Definir uso exclusivo o aislamiento/habilitación. |
| A12 | Media / media | Impedancia y robustez USB/ESD no demostradas por estas herramientas. | Comprobar geometría y ensayo de enlace/ESD. |

Las prioridades condicionales no afirman que los periféricos externos sean incompatibles: el receptor RC fue identificado por el operador como FlySky FS-iA6B, pero faltan su nivel lógico medido y los modelos de los demás periféricos. Hasta obtenerlos, se indican requisitos de compatibilidad.

## Resumen del diseño actual

87 referencias físicas de esquema, 91 huellas en PCB incluyendo H1–H4; 89 redes; 964 segmentos; 334 vías independientes. Hay 64 componentes SMD para montaje superior, 21 conectores THT y dos puentes de soldadura. Los 7 IC físicos son U1, U2, U4, U5, U6, U7 y U8; U7 tiene tres unidades de símbolo. No existen U3 ni U9 en el diseño actual.

La placa tiene dos capas, 1.6 mm y cobre de 35 µm en el stackup. Contorno nominal 100×100 mm, esquinas de radio 2.5 mm; el job Gerber informa 100.05×100.05 mm por la representación del borde. Los agujeros M3 son cuatro NPTH de 3.2 mm.

### Árbol de alimentación real

```text
J5 / +5V ────────────────> U7 LM358, conectores externos de 5V
       └─ D7 SS14 ─┐
J16 USB VBUS ─ D9 ─┴─> 5V_SYS ─ U1 AMS1117CD-3.3 ─ LINEAR_3.3V
                                                    └─ JP1 cerrado ─> +3.3V
J20 / 3.3V_EXT ─────────────────────────── JP2 abierto ──────> +3.3V
+3.3V ─> ESP32, SP3485, HC595, conectores I2C
       └─ FB1 ─> IMU_3.3 / BMI088
J19 / +7V ─> J17 y J18 / servos
GND común
```

D7/D9 forman OR de alimentación de lógica; no convierten USB en alimentación de toda la red +5V. JP1 debe abrirse si se usa la alternativa externa por JP2, salvo diseño explícito para paralelo, que aquí no existe. No hay fusible ni protección de sobretensión dedicada en J5/J19; su provisión externa debe quedar definida. Los periféricos conectados directamente a +5V no quedan protegidos por D7.

## Verificación nativa y cobertura

| Comprobación | Resultado | Evidencia |
|---|---|---|
| DRC con refill y paridad | 0 errores, 0 sin rutear; 2 avisos SW y 4 huellas mecánicas extra. | `drc.json` |
| ERC con exclusiones incluidas | 0 errores; 7 avisos listados, incluyendo conflicto MISO excluido históricamente. | `erc.json` |
| Netlist KiCad vs pads PCB | 325 terminales nativos, 0 diferencias de red. | `native_crosscheck.json` |
| Analizador vs netlist nativo | 315 comprobaciones de pines conectados, 0 diferencias. NC se trata aparte. | `helpers/verify_design.py` |
| Fuentes actuales vs paquete | Coinciden; checksums de ZIP/BOM/CPL correctos. | Paquete y `source-hashes.json` |
| BOM/CPL actual | 64/64 referencias, sin duplicados ni ausencias. | `cpl-validation.json` |
| Pruebas CPL del repositorio | 11/11 pasan con `/usr/bin/python3`. | Ejecución 15/10/2026 |
| SPICE automático con parásitos | 14 simulaciones pasan. | `spice.json` |
| Filtro de acelerador específico | 8.766 mVpp al 50%, 20 kHz; t10–90=10.327 ms. | `spice_work/throttle_0.5.log`, `throttle_step.log` |

El DRC conserva cinco categorías ignoradas en el proyecto: courtyard ausente, extremo de pista no centrado en vía, geometrías de tuning, filtros de huella y tipo de huella/pads. No debe interpretarse como revisión de todas las posibles reglas de fabricación. Clearance de clase por defecto 0.2 mm, mínimo de pista configurado 0.2 mm; las pistas existentes más finas son 0.25 mm. Los microtaladros de 0.2 mm de U8 tienen excepción explícita en las reglas.

Los avisos ERC son cuatro de tipos de pin SW1/SW2, dos nombres de red HBRIDGE_EN/HB_EN, SDO1/SDO2 compartiendo MISO, y un extremo de alambre de 0.0127 mm en la raíz. El MISO común es coherente con CS independientes; requiere firmware correcto, no puentear CS.

## Revisión por componente y asignación de pines

Se cotejaron todos los pines de los 7 IC y la paridad de todos los componentes con el netlist nativo. El [inventario de cobertura](COBERTURA_COMPONENTES.md) explicita las verificaciones documentales y las pendientes; tener paridad no demuestra por sí solo que una pieza física sea la correcta.

| Referencia | Componente | Base documental y resultado |
|---|---|---|
| U8 | ESP32-S3-WROOM-1-N8R2 | Espressif v1.8 pp11–12: 41 terminales corresponden. Alimentación/USB/boot coherentes. GPIO35–37 disponibles para N8R2 Quad SPI; no extrapolar limitación de variantes Octal. |
| U4 | BMI088 | Bosch BST-BMI088-DS001, tabla de pines y sección SPI: 16 terminales corresponden; PS a GND, CS separados, SDO común y VDD/VDDIO en IMU_3.3. |
| U2 | SP3485EN-L/TR | MaxLinear rev2.0.2 pp1,4: RO1, RE2, DE3, DI4, GND5, A6, B7, VCC8 correctos. |
| U5 | SN74HC595DR | TI SCLS041J p3: SOIC16 correcto, VCC16/GND8, SER14, CLOCK11, LATCH12, OE13, SRCLR10. C19=100nF es su bypass local. |
| U6 | ULN2003BDR | TI SLRS064B p3: entradas1–7, masa8, COM9, salidas16–10 correctos. El value ULN2003A no describe exactamente el MPN B de la BOM. |
| U7 | LM358DR | TI SLOS068AB p3: ambos amplificadores y alimentación correctos. Canal B terminado como seguidor a GND. Límite funcional A1 pese a pinout correcto. |
| U1 | AMS1117CD-3.3 | Documento AMS DS1117 pp1,3,4, localizado por C841796: GND1, OUT/tab2, IN3 y 22µF tantalio correctos. Sitio directo del fabricante no descargó; contraste con copia de documento AMS publicada por el proveedor. |
| D1 | DOWO SM712-02HTG | Documento DOWO pp1,4: líneas en1/2 y GND3 correctos. El enlace del esquema a Littelfuse corresponde a otra marca; no usarlo como garantía de parámetros DOWO. |
| D5 | Littelfuse SP0503BAHTG | PDF local pp1–3: GND1, canales2/3/4 para VBUS/D+/D− coherentes, SOT143. El dispositivo ya protege VBUS. |
| D7/D9 | SS14 | OR y polaridad A→K correctos en archivos; pin1 K. El proveedor C2480 muestra actualmente MDD y la documentación cita otra marca: cerrar identificación antes de usar curvas exactas de caída. |
| SW1/SW2 | TS-1187A-B-A-B | La red eléctrica es correcta y cada par de pads comparte número; queda pendiente cotejo dimensional/pin1 con PDF exacto. El PDF local TS1201 no es el MPN actual y existe mismatch de biblioteca. |
| J16 | GT-USB-7010ASV | Paridad de todos los pads; A6/B6 D+, A7/B7 D−; CC1/CC2 separados a5.1k. Huella estándar coherente; dibujo exacto del proveedor y orientación final siguen como cierre de montaje. |
| R/C/FB/JP/H | Pasivos y mecánica | Valores/conexiones se recorrieron completos; pinout de resistencias y MLCC de dos terminales no es direccional. C30 polarizado1+ a OUT y2− aGND. Ferrita/bias DC y tolerancias de pasivos no se caracterizaron con medición. |
| Headers THT | Interfaces externas | Pinout completo en [tabla de conectores](CONECTORES.md). Varios MPN son texto genérico; no acreditan corriente, keying o compatibilidad del cable. |

### Acelerador y LM358

**Corrección del requisito y contraste con firmware (15/10/2026).** El operador aclaró que el potenciómetro original usaba0–5V, pero el controlador alcanza aceleración máxima con PWM de amplitud3.3V. La exigencia previa de entregar5V se retira. No se requiere ganancia1.515 para reproducir el comportamiento actual.

Se inspeccionó solo lectura `SALUS/ESP32_SALUS`, commit `037c1ed`: `src/main.cpp` líneas70–87 configura20kHz/8bits, referenciaESP3.3V y escala los valores Arduino41..150 a duty62..228 de255. Los promedios ideales son0.80235..2.95059V antes del buffer, aproximadamente0.79676..2.93002V enJ11 con R18/R19 y carga altaZ. Son cálculos del PWM filtrado, no mediciones de salida ni prueba de que el controlador interprete solo el promedio. `quadThrottleStop()` aplica62, no duty0; no cambiar ese nivel sin calibrar el umbral del controlador.

**Reevaluación A1:** con el firmware actual, salidaGPIO nominal3.3V y alimentaciónU7 exactamente5V, el máximo medio2.95059V queda por debajo del límite3.0V de modo común en temperatura. Por tanto no se demostró que la configuración actual exceda ese límite. El margen nominal es solo49.4mV: tolerancias y caídas de+5V pueden eliminarlo; para dicho máximo el límiteV+−2 exige alimentaciónU7≥4.95059V, antes de otros márgenes. Si una configuración futura permite duty100%, vuelve a aplicarse el análisis3.3V siguiente. El GPIO13 del firmware clásico no corresponde al GPIO21 de esta PCB; la migración alS3 requiere mapearlo explícitamente.

El PWM sin filtro funcionando es evidencia operativa aportada por el operador. El RC+buffer es una mejora razonable para aproximar una tensión continua, pero cambia la forma de señal, agrega respuesta temporal y necesita volver a comprobar umbral de reposo, máximo y salida al perder alimentación. No se alteraron firmware niPCB.

La cadena correcta es GPIO21 → R17=47k → C20=100nF aGND → U7A seguidor → R18=330Ω → J11, con R19=47k en la salida. R35=100k es pull-down del GPIO y no un divisor que reduzca la entrada del operacional cuando el GPIO conduce.

El filtro tiene τ=4.7ms, fc=33.86Hz, t10–90=10.327ms. En modelo ideal la salida máxima es3.27699V para una entrada3.3V de alta impedancia. Pero [TI, LM358, pp5 y10](https://www.ti.com/lit/ds/symlink/lm358.pdf) limita el modo común en temperatura a V+−2: con5V son3.0V. El rango hasta3.5V solo corresponde a25°C en esas condiciones. Si se utiliza la escala completa hasta100%, la última parte del duty no queda garantizada en0–70°C; a5V nominal el límite3V se alcanza a90.9% de duty. Con4.75V de alimentación el margen empeora.

La simulación ideal reproduce el RC, no las limitaciones de modo común, swing, offset o recuperación del LM358. Por tanto el documento de agosto no aprueba el rango real completo. La salida además depende de impedancia/capacitancia del controlador externo; R17 multiplica el error por corriente de polarización. Revisar operacional apropiado con rango de entrada/salida y estabilidad a ganancia unitaria, o justificar una reducción de rango con requisitos explícitos.

### Alimentación y térmica

Actualización: [revisión térmica focalizada con escenarios y geometría nativa](thermal/REVISION_TERMICA_3V3.md). Sustituye cualquier lectura de49.7°C del analizador como temperatura prevista real.

**Prioridad de diseño aclarada por el operador:** presupuesto limitado y primera revisión funcional; mantener arquitectura sencilla y evitar introducir un buck enPCB si el lineal puede justificarse. El regulador3.3V solo alimentará cargas de la propiaPCB; no se debe presupuestar aquí corriente de servos, motor,Jetson o módulos externos3.3V. Conservar una solución lineal es una opción válida: la revisión no exige cambiar a conmutación. Falta cerrar la carga interna real, transitorios y temperatura; el presupuesto automático omite la ramaIMU y utiliza corrientes heurísticas, por lo que no es un total fiable. C30 tantalio y cobre/vías existentes son medidas favorables. Evaluar AMS1117 y, si hace falta, otro LDO con compensación/encapsulado apropiados antes de introducir una topología nueva. Un LDO de menor dropout no elimina la disipación(Vin−Vout)I.

**Condiciones de instalación aclaradas por el operador (15/10/2026).** Batería nominal48V alimentará dos bucks externos, uno de5V y otro de7V. USB se usará para programación y enlace de datos con Jetson Orin, conectado simultáneamente con la alimentación externa; no se desea alimentar la placa desdeUSB ni retornar potencia hacia laJetson. Gabinete de chapa blanca, ventilado, en robot exterior; PCB sin sol directo, con ambiente interno potencialmente alto pero aún sin máximo cuantificado.

El diseño actual no es USB solo datos: D9 permiteUSB2_VBUS→5V_SYS. Con ambas fuentes, el OR porD7/D9 toma corriente de la rama con mayor tensión efectiva y puede repartirla; no impone prioridad al buck. En operación normal los diodos bloquean el retorno directo de5V_SYS a los orígenes, pero no son garantía de fuga cero, aislamiento ni tolerancia a una falla. Al apagar el buck conJetson encendida, D9 mantiene alimentada la lógica y U7 sigue sin+5V. Para cumplir estrictamente USB de datos hay que eliminar/deshabilitar esa ruta de potencia o rediseñar la selección, y revisar las condiciones del periférico/firmware USB elegido. Se decidió USB Serial/JTAG inicial y no añadir monitor VBUS; TinyUSB autoalimentado queda condicionado a revisión futura. No se cambióD9.

Si se usa USB-OTG/TinyUSB autoalimentado, [Espressif documenta monitor deVBUS](https://documentation.espressif.com/projects/esp-idf/en/v5.4.2/esp32s3/api-reference/peripherals/usb_device.html): detectar presencia deVBUS mediante circuito compatible con3.3V y configurar el stack; el esquema actual no tiene un GPIO de detección. USB Serial/JTAG integrado requiere comprobar por separado su configuración y condiciones de conexión. No aplicarVBUS5V directamente aGPIO ni eliminar indiscriminadamenteGND/CC/ESD. Jetson y placa compartenGND porUSB; no confundir bloqueo de potencia inversa con aislamiento galvánico.

Falta identificar los bucks: tensión máxima de entrada debe cubrir la batería cargada y transitorios, no solo48V nominales; corriente, temperatura, ventilación y rizado deben cubrir las cargas reales. Definir si sus negativos están unidos y dónde se hace el retorno de servos/motores frente a la masaUSB/Jetson. Confirmar la protección a nivelbatería/ramales y respuesta a falla de buck; no asumir que existe por el nombreDC-DC.

La ventilación y pintura blanca no fijan una temperatura máxima dePCB. El objetivo térmico se referirá al aire interno local junto aU1 y al calor deJetson/bucks. Ejemplo de sensibilidad, no condición medida: IN4.6V,0.5A sostenidos y80°C/W producen0.65W y52°C de elevación; a60°C de aire interno serían112°C de unión. Esto justifica revisar disipación/arquitectura antes de aceptar el AMS1117 para verano. También debe revisarse el rango de todos los componentes: LM358DR comercial0–70°C y receptorFS-iA6B declarado−10..60°C, no solo la temperatura de unión deU1.

El [documento AMS DS1117](https://datasheet.lcsc.com/datasheet/pdf/e6935943fc6b1bbf350a1a0f3e90dc4a.pdf?productCode=C841796), p3, da hasta1.3V de dropout a0.8A: necesitaría4.6V en IN para3.3V. La fuente de5V y la caída SS14 dejan poco margen para tolerancia, cable y corriente. Esto no demuestra fallo a toda carga; exige un presupuesto real. Espressif pide capacidad de fuente de al menos0.5A para el módulo (v1.8 p27); hay además IMU, interfaz y cargas externas.

C28=10µF/C23=100nF están a entrada y C30 es22µF tantalio10V a salida, coherente con la recomendación AMS de estabilidad. No hay un problema demostrado de reemplazo por MLCC en C30.

El analizador térmico a40°C calcula49.7°C en U1, suponiendo0.22A y26°C/W efectivos. No son parámetros medidos de esta placa. El documento AMS indica80°C/W para TO252 en sus condiciones. Como sensibilidad, con IN=4.6V y80°C/W: a0.35A,0.455W y76.4°C; a0.5A,0.65W y92°C; a0.8A,1.04W y123.2°C. No son predicciones ni cargas máximas permitidas. La geometría tiene cobre de salida y vías, pero no justifica adoptar automáticamente26°C/W.

La placa no alimenta U7 desdeUSB a través de D7. Durante programación USB el firmware debe mantener actuadores inhibidos; también deben revisarse retroalimentación y comportamiento de entradas de un IC apagado. JP1/JP2 no son un OR de fuentes3.3V.

### Hall, PPM, finales y UART

Hall_A/B/C entran a GPIO35/36/37 mediante1k serie, sin adaptación de nivel. Si el sensor es push-pull5V, falta una interfaz apropiada; si es open-collector, hacen falta pull-ups3.3V definidos. No se garantiza funcionamiento dependiendo de diodos internos del ESP32.

PPM: divisor4.7k/10k, factor0.680272. Entrada3.3V→2.245V, por debajo de VIHmin2.475V conVDD3.3V. Entrada5V→3.401V; entrada5.5V→3.741V, fuera del nivel máximo de entrada especificado VDD+0.3 conVDD3.3. El límite inferior externo para HIGH nominal es3.638V. Incorporar tolerancias de fuente, resistencias y amplitud del receptor.

El operador especificó **FlySky FS-iA6B**. Su [ficha oficial](https://www.flysky-cn.com/ia6b-canshu) admite alimentación4.0–8.4V y salidaPPM; la alimentación+5V de J15 cae dentro de ese rango. La ficha no especifica amplitudVIH/VOH de salidaPPM: no se puede deducir5V de señal por alimentarlo a5V. Medir en CH1/PPM de la unidad y después del divisorR21/R24; confirmar configuraciónPPM en la emisora y pérdida de enlace. [FlySky explica que PPM/CH1 debe seleccionarse en el menú del receptor](https://www.flysky-cn.com/0enfaq). Si el HIGH medido es3.3V, este divisor necesita revisión; si es5V, evaluar tolerancias y transitorios. No se hizo medición en el receptor.

Finales J7/J8 sí tienen pull-ups4.7k y100nF, τ0.47ms/corte338.6Hz; pensados para contacto aGND. No aplicar tensión externa sin revisar. UART J4 comparte TX/RX con SP3485 a través de resistencias1k hacia el MCU: conectar otro transmisor a RX mientras RO está activo puede causar contención. Debe definirse exclusión/configuración, no tratarlo como UART independiente del bus485.

### I2C, IMU, relés y servos

SDA/SCL no incluyen pull-ups locales. Un módulo AS5600 puede aportarlos, pero debe comprobarse su tensión; no asumir que alimentarlo a3.3V garantiza que todos sus pull-ups estén a ese mismo rail. Dimensionar para frecuencia y capacitancia del cable, y evitar múltiples resistencias excesivamente bajas en paralelo.

BMI088 tiene100nF y4.7µF en su rail filtrado, CS con pull-ups, PS aGND y SDO compartido válidos. INT2/INT4 NC no requieren pull-up por ser interrupciones no utilizadas. La inicialización SPI/dummy byte del acelerómetro es obligación de firmware.

OE de HC595 tiene pull-up10k y LATCH pull-down10k, una buena condición de arranque. No asegura el contenido inicial del registro de almacenamiento: cargar ceros y latchear antes de habilitar OE. Compartir MOSI/CLOCK con IMU no es un error si se controla LATCH y el byte final. Hay siete salidas de relé; J10.5 está NC. No interpretar los500mA de rating individual ULN como corriente garantizada de cada canal simultáneo con HC595 a3.3V.

COM9 está NC. Es aceptable para entradas de módulos externos protegidos; para bobinas directas sin diodos no cumple protección inductiva. Confirmar también polaridad activa y estado con salidas en alta impedancia.

J17/J18 tienen PWM serie330Ω y pull-down10k: máximo nominal aproximado3.195V con salida GPIO3.3V. Debe superar el umbral del servo real. El rail7V usa pistas1mm y headers genéricos2.54mm: no permite deducir corriente de bloqueo segura. Faltan modelo, rating, cableado, fuente, capacitancia bulk y ensayo de ruido/retorno.

### RS-485

R4=120Ω es terminación permanente y ambas cabeceras J3/J21 están en el mismo bus. Debe estar en un extremo y no multiplicarse con más de dos terminaciones de extremo. R37 baja DIR para deshabilitar el transmisor al arranque.

No hay bias A/B local. El [datasheet SP3485 rev2.0.2](https://www.maxlinear.com/ds/sp3485.pdf) tiene una tabla enp7 que menciona open/shorted, mientras su texto y [FAQ del fabricante](https://www.maxlinear.com/product/interface/serial-transceivers/rs-485-rs-422/sp3485) limitan standard fail-safe a entradas abiertas. No se declara fallo automático por esta ambigüedad: caracterizar el bus terminado sin driver, ruido y desconexión, o aclarar con fabricante. D1 aporta TVS, pero no aislamiento galvánico; el cable y tierra común deben mantenerse dentro de especificaciones.

## Layout, EMC y fabricación

El ruteo es completo. Tracks3.3V0.6mm,5V/7V1mm; USB VBUS tiene16 segmentos de0.25mm y129.7mm acumulados: añade resistencia en una alimentación ya limitada por dropout. Los datos USB van en F.Cu sin vías; tramos a conector D−44.448mm y D+43.556mm, más4.412/4.289mm hacia MCU detrás de resistencias. Diferencia acumulada aproximada1.015mm; son sumas de pistas, no un cálculo preciso de retardo por trayecto que quite ramas de pads.

Para Full-Speed12Mbps esa diferencia no demuestra fallo. Tampoco demuestra90Ω diferencial: el modelo microstrip informa103.6Ω por pista usando stackup, pero no incluye acoplamiento/copla­nar y no puede convertirse directamente en impedancia diferencial. [Espressif recomienda90Ω±10% y referencia continua](https://documentation.espressif.com/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html). Revisar con geometría real y ensayo de enlace.

El análisis EMC genera64 hallazgos, pero solo declara9 categorías efectivamente comprobadas; no equivale a ejecutar44 pruebas normativas ni a un certificado. Tiene avisos de retorno y stitching para revisar en cobre real. No hay una conclusión defendible de que pasará/fallará EMC a partir de un score70.

D5 sí tiene GND; la vía de GND independiente más próxima a su pad1 está a3.23mm. Mejorar descarga local si el layout lo permite, pero ausencia de vía en un radio heurístico no es ausencia de retorno: hay plano superior. Probar ESD por conector y operación con cableado. Sensores, finales y UART tienen protección limitada para un entorno con motores y cables largos.

Existe keep-out de antena dentro de la huella U8 en F.Cu/B.Cu: x74.325..122.325,y143.75..164.75, prohibiendo cobre, pistas, vías, pads y componentes. No falta la regla RF. El parser no lo incluye en `keepout_zones` por estar anidado. Se observaron también la regla de U4 y las doce perforaciones térmicas integradas en pad41 de U8.

H1=(145,145), H2=(145.5,55), H3=(55,55), H4=(55,145)mm: los centros no forman exactamente un cuadrado90×90. Confirmar si0.5mm es intencional. No corregir sin plano del soporte.

El ZIP enviado contiene11 archivos:8 capas de cobre/máscara/pasta/serigrafía, Edge.Cuts, drill y job. Se analizaron los archivos reales extraídos del ZIP y también la carpeta extendida. Hay437 perforaciones; el taladro incluyeNPTH yPTH con atributos. La clasificación heurística llama «component holes» a las12 vías de0.2mm integradas en la huella U8: no son componentes adicionales.

BOM/CPL coinciden64/64 y se mantienen los nombres originales. No se reprodujo el visor del ensamblador ni su interpretación de cada rotación. Los fiduciales faltan en la placa, pero se pueden proporcionar en rieles del panel; [la política de panelización del ensamblador](https://jlcpcb.com/help/article/pcb-panelization) contempla añadirlos. Debe acordarse, no clasificarlo automáticamente como defecto eléctrico.

Cero puntos TP dedicados no significa acceso cero: los headers y pads ofrecen acceso manual. Para producción conviene definir puntos de alimentación, GND, reset, buses y acelerador con procedimiento de banco. Revisar holgura J6 y rieles de ensamblaje por componentes cercanos a bordes.

## Simulaciones y falsos positivos

SPICE automático:14/14 pasan, con parasíticos geométricos de79 redes. No prueba lógica de firmware, analogía exacta de todos los IC ni condiciones externas. El detector clasifica erróneamente R17/R35 como divisor y no reconstruye por completo U7 multiunidad; su «pass» no aprueba el acelerador.

El testbench específico reproduce el RC al10/50/90% de20kHz:0.327739/1.638523/2.949344V medios y3.183/8.766/3.219mVpp. A0/100% se usaron fuentesDC explícitas para evitar que `PULSE` con ancho0 adopte el valor por defecto de ngspice; resultan0/3.276991V sin ripple. No se modificaron los bancos históricos durante esta revisión. Respuesta10–90%10.327ms.

| Resultado automático | Tratamiento de revisión |
|---|---|
| U6 sin desacoplo: error EMC DC-002 | Falso positivo: ULN2003 no tiene pinVCC; es array de colector abierto, no IC lógico alimentado. La cuestión real es COM/carga. |
| U4 INT2 requiere pull-up | Falso positivo: salida de interrupción marcada NC, no entrada de bus. |
| VBUS sin TVS | Falso positivo: D5.2 está en VBUS. |
| VBUS sin condensador local | Aviso real de topología; C28 está después del diodo y lejos del conector. Revisar arranque/inrush/ESD, no agregar capacidad arbitrariamente. |
| USB D+/D− «crosstalk» XT-001 | Acoplamiento intencional de par diferencial; no separar por regla genérica3H. |
| C17/C18 como desacoplo U8 | Falso: son filtros de finales. C6/C5 son bypass/bulk del ESP32. |
| C30 como capacitor que deba cambiarse | No elevar: ya es22µF tantalio en esta revisión. |
| Falta keepout U8 | No: existe dentro de la huella y se cotejó archivo nativo. |
| H1–H4 «huellas extra» | Mecánicas intencionales; revisar coordenadas, no borrar. |
| SW1/SW2 mismatch | No es prueba de fallo eléctrico; exige comparar versión de huella con dibujo exacto y biblioteca. |
| GR-004:255 flashes de pasta frente679 de cobre | Conteo mezcla THT y ventanas térmicas; no demuestra pasta ausente. Ventanas U1/U8 existen. Revisión de máscara y stencil con ensamblador pendiente. |
| Resultado favorable del gate de fabricación | 11pass/1warn solo para sus12 comprobaciones; no considera todos los riesgos manuales anteriores. No aprueba automáticamente el diseño. |

## Ciclo de vida y revisión anterior

Se ejecutó `lifecycle_audit.py`:26MPN quedaron con estado desconocido porque la fuente sin credenciales no aporta lifecycle. No se interpretan26 observaciones como26 piezas obsoletas. En contraste manual, [TI sí marca ULN2003B como obsoleto](https://www.ti.com/product/ULN2003B), consultado15/10/2026. Los otros estados no se dieron por comprobados. No se hizo una auditoría de stock/precio como aprobación de compra.

Se ejecutó `diff_analysis.py` frente al análisis local de julio:19 cambios (3altas,16modificaciones). Cambiaron diseño y versión de analizador; no son19bugs nuevos. Frente al informe15/07: contorno/ruteo/paridad quedaron resueltos y R2/R3 ahora son4.7k; U9buck y U3USB-UART ya no existen; persisten observaciones de alimentación, servos y avisos SW/MISO. Los análisis antiguos no acreditan el circuito actual.

## Límites explícitos y evidencia

Se ejecutaron `analyze_schematic.py`, `analyze_pcb.py --full --proximity`, `cross_analysis.py`, `cross_verify.py`, `analyze_gerbers.py` (carpeta y ZIP), `analyze_thermal.py` a40°C, `analyze_emc.py --spice-enhanced`, extracción de parásitos, `simulate_subcircuits.py`, lifecycle, delta, gate de fabricación y revisión manual por IC. El gate de evidencia de revisión profunda aceptó13 entradas,0parciales,0cuarentenadas: valida enlaces/cálculos estructurados, no funcionamiento físico.

Datasheets existentes leídos manualmente; PDFs nuevos de TI, Espressif y MaxLinear recuperados de fabricante. DigiKey no pudo sincronizar sin credenciales. La sincronización alternativa devolvió varios PDFs de MPN distintos; se aislaron en `datasheets-untrusted/` y no se aceptaron por nombre de archivo. El manifiesto previo se preservó. No se generó un caché completo de extracciones tipadasv1.4; por tanto las comprobaciones automáticas que dependen de él no tienen cobertura de fabricante completa. El cotejo manual por IC y las brechas anteriores sustituyen afirmaciones automáticas de confianza alta.

Quedan sin comprobación completa: dibujo exacto de pulsadores y conectorUSB, especificación real de headers/cables, ratings y sesgoDC de cada pasivo con la pieza física final, modelos de periféricos externos, fuente/gabinete/ambiente máximo, impedancia de campo2D/3D, integridad de señal medida y tolerancias de producción. No se hicieron ensayo EMC, RF, carga térmica, ripple, ESD, enumeración USB, HIL ni pruebas de actuadores. No se conoce una placa física ensamblada inspeccionada en este trabajo.

Los analizadores no consideran continuamente todas las geometrías3D, ni certifican estándares. Creepage de red/mains no aplica al dominio de3.3/5/7V de esta placa; la instalación general del robot y protecciones externas se evalúan aparte. Las curvas térmicas, retorno y emisiones se usan como riesgos, no como mediciones.

Resultados completos y scripts reproducibles locales en `analysis/review-2026-10-15/` (caché ignorado porGit). En esta carpeta de documentación se conserva un resumen de evidencia y tablas legibles. `source-hashes.json` identifica los archivos revisados.

## Plan de cierre

1. Resolver A1 y definir la entrada real del acelerador: rango, impedancia, capacidad y comportamiento seguro al perder alimentación.
2. Cerrar modos J5/USB/J20 y puentes; medir3.3V a peor tensión y carga escalonada con Wi-Fi/periféricos representativos, sin conectar actuadores.
3. Especificar modelos y niveles de Hall, receptorPPM, módulos de relé y servos; cerrar pull-upsI2C y exclusión de UART/RS485.
4. Revisar continuidad de fabricación de U6, dibujos SW/USB, coordenadas de fijación y plan de rieles/fiduciales.
5. Ejecutar arranque/reset/USB/SPI/RS485, osciloscopio en J11 y alimentación, carga térmica y pruebasEMC/ESD proporcionales al producto.
6. Tras correcciones, repetir DRC/ERC/paridad, revisión focalizada y BOM/CPL/Gerbers en un paquete nuevo. Mantener esta entrega como evidencia histórica.

Las pruebas de banco requieren autorización y condiciones seguras del operador; ninguna prueba de movimiento se ejecutó en esta revisión.
