# AMS1117 de 3.3 V: revisión térmica focalizada — 15/10/2026

## Resultado

**Conservar el regulador lineal es una opción viable, pero no se puede asignar una temperatura ambiente máxima garantizada a esta PCB sin conocer la corriente sostenida y comprobar su resistencia térmica en el gabinete.** La geometría de disipación es favorable y se detallan escenarios útiles para decidir sin imponer un buck.

Como criterio provisional, con IN del regulador no superior a5.0V, carga sostenida250mA, reserva interna10mA y resistencia térmica efectiva no superior a100°C/W, el modelo da Tj≈107.5°C con60°C de aire interno. A300mA y50°C da106°C. Esos escenarios conservan margen frente a125°C, pero sus condiciones no están medidas ni garantizadas. A400mA continuos, la misma hipótesis da123°C con50°C internos: no deja margen suficiente. No extrapolar un pico de radio a corriente continua ni interpretar estos números como certificación.

## Base física y eléctrica

- Proyecto revisado: `PCB_SALUS_v3`, commit de diseño `5d39f71`; U1 `AMS1117CD-3.3`, TO-252, pad/tab2 a salida3.3V.
- Solo cargas internas dePCB: ESP32-S3, BMI088, SP3485, HC595, sus cargas de señal y polarizaciones. No sumar motor,Jetson,servos o cargas externas a3.3V.
- Entrada normal: buck externo5V → D7 SS14 → `5V_SYS` → U1. La tensión usada en cálculos es la medida en IN deU1 después del diodo, no el ajuste del buck.
- SalidaU1: `LINEAR_3.3V` → JP1 cerrado → rail3.3V; IMU medianteFB1.
- Tab6.4×5.8mm, cobre superior de salida270.81+100.78≈371.59mm² en zonas rellenas; inferior388.59mm². Son áreas de zonas, no una medición calorimétrica ni cálculo3D.
- 32 vías independientes en la red de salida;14 dentro de6mm del anclaU1. Diámetros de perforación0.3/0.4mm. No confundir «vías próximas» de una heurística con vías realmente en esta red.
- KiCad nativo confirma conexión **FULL** de las tres zonas a pads. Los dos pads2 heredan esa conexión. No hay radios térmicos en esas conexiones de zona.
- C28=10µF/C23=100nF a entrada y C30=22µF tantalio a salida. La selección del condensador de salida es coherente con el documentoAMS; no se exige cambio a buck por estabilidad deC30.

Evidencia geométrica: [layout_native.json](layout_native.json) y caché `analysis/review-2026-10-15/pcb.json`. La suma deáreas no equivale automáticamente a cobre útil totalmente isotérmico: hay soldadura, geometría, calor vecino, orientación y convección.

## Límites del fabricante y modelo

El [documento AMS DS1117](https://datasheet.lcsc.com/datasheet/pdf/e6935943fc6b1bbf350a1a0f3e90dc4a.pdf?productCode=C841796), pp2,3,5:

- Temperatura máxima de unión para funcionamiento continuo:125°C.
- Referencia de resistencia unión–ambiente para TO-252:80°C/W en las condiciones del documento.
- El cobre dePCB cambia la resistencia térmica; el propio fabricante pide experimentación para la aplicación real. Su tabla de áreas es una guía aproximada y no permite interpolar una garantía específica deTO-252/gabinete.
- Dropout máximo1.3V especificado a0.8A; el margen de tensión es una cuestión distinta del margen térmico.

No se usa el26°C/W del analizador automático: provenía de una tabla genérica40°C/W multiplicada por una corrección0.65, sin modelo térmico validado para esta placa.

Se calcula sensibilidad con60,80y100°C/W:60 exploratorio favorable,80 referencia y100 escenario adverso de sensibilidad. **100°C/W no es una cota superior demostrada**: una instalación peor puede superarla. [TI explica por qué RθJA depende delPCB y del entorno](https://www.ti.com/document-viewer/lit/html/SSZTB80/GUID-D4E3F3F5-260D-45A1-862A-6E9A3052DC5A).

Modelo usado:

```text
P_U1 ≈ (Vin_U1 − 3.3) × I_salida + Vin_U1 × I_masa
Tj ≈ T_aire_local + RθJA × P_U1
```

Se añade una **reserva supuesta de10mA** para consumo interno del regulador; no es un máximo garantizado del fabricante ni una medición. La caída deD7 disipa potencia adicional fuera deU1 y puede calentar la región. No se simula ese acoplamiento3D. Tampoco se modelan tolerancias deVout, distribución exacta de calor ni ciclo temporal de radio.

Se elige110°C como objetivo de revisión con15°C de margen frente125°C. No es una clasificación del fabricante ni una garantía de vida útil; es un criterio prudente del análisis.

## Escenarios con4.6V en IN deU1

4.6V es un ejemplo nominal tras el diodo, no una tensión medida. Se toma corriente sostenida o equivalente térmica, no un pico breve.

| Carga3.3V sostenida | P_U1 con reserva | Tj con60°C de aire, Rθ80..100 | Aire máximo calculado paraTj≤110°C, Rθ100..80 |
|---|---:|---:|---:|
| 200mA | 0.306W | 84.5..90.6°C | 79.4..85.5°C |
| 250mA | 0.371W | 89.7..97.1°C | 72.9..80.3°C |
| 300mA | 0.436W | 94.9..103.6°C | 66.4..75.1°C |
| 350mA | 0.501W | 100.1..110.1°C | 59.9..69.9°C |
| 400mA | 0.566W | 105.3..116.6°C | 53.4..64.7°C |
| 500mA | 0.696W | 115.7..129.6°C | 40.4..54.3°C |

Una cifra por encima de125°C significa que el modelo ya incumple el límite; no que la placa vaya a estabilizarse realmente ahí: podría perder regulación o entrar en protección. No utilizar protección térmica como modo normal.

## Sensibilidad a una entrada más alta

Una tensión más alta ayuda al dropout, pero aumenta el calor. Si IN_U1 llegara a5.0V, manteniendo los demás supuestos:

| Carga sostenida | P_U1 | Tj con60°C de aire, Rθ80..100 | Aire máximo calculado paraTj≤110°C, Rθ100..80 |
|---|---:|---:|---:|
| 200mA | 0.390W | 91.2..99.0°C | 71.0..78.8°C |
| 250mA | 0.475W | 98.0..107.5°C | 62.5..72.0°C |
| 300mA | 0.560W | 104.8..116.0°C | 54.0..65.2°C |
| 400mA | 0.730W | 118.4..133.0°C | 37.0..51.6°C |
| 500mA | 0.900W | 132.0..150.0°C | 20.0..38.0°C |

No subir la salida del buck para ganar dropout sin repetir la cuenta térmica y revisar todos los componentes del rail5V. No se necesita identificar el modelo de buck para reconocer esta relación.

## Presupuesto interno: qué sabemos y qué falta

| Carga | Evidencia | Uso en esta revisión |
|---|---|---|
| ESP32-S3 N8R2 | [Espressif v1.8 pp27–29](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf): capacidad recomendada de fuente≥0.5A; TX hasta355mA en una condición de radio. | Consumidor dominante;355mA no es cota absoluta universal ni promedio permanente. CPU,PSRAM,Wi-Fi y tráfico cambian consumo. |
| BMI088 | Bosch BST-BMI088-DS000-19 p8: gyro5mA y acelerómetro150µA típicos a3V/25°C bajo condiciones indicadas. | Orden de5.15mA, no máximo garantizado en todo modo/temperatura. |
| SP3485 | MaxLinear rev2.0.2 pp2–3: consumo depende de habilitación y carga. | Separar reposo de transmisión con terminaciones: no presupuestar solo la corriente sin carga. |
| HC595 y entradasULN | TI SCLS041J ySLRS064B: consumo dinámico y corriente de entradas/cargas. | Sumar excitación de canales; no contar corrientes de bobinas o de colector como cargas del rail3.3V. |
| Pull-ups y otras señales | Valores de esquema cotejados; corriente cambia con estados. | Pequeña contribución pero no cero. |

El presupuesto automático anterior no es fiable: no propagaba bien la carga porJP1/FB1 e introducía corrientes heurísticas. No se usa como aprobación de0.22A o0.255A.

Es razonable estudiar escenarios de200–300mA medios y400–500mA exigentes, pero **no se afirma que la placa consuma esos valores**. Si el control opera normalmente porUSB y usaWi-Fi solo paraOTA, el consumo medio puede ser menor que conTX continuo; no se ha verificado el firmware finalS3 ni medido un duty térmico de radio. Un suministro debe soportar transitorios aunque el cálculo térmico de estado estacionario use el promedio de potencia adecuado. Sin curvas térmicas transitorias no se asigna una temperatura a pulsos aislados.

## Umbrales provisionales para decidir

- **Aire interno50°C:** el escenario300mA,IN≤5V,Rθ≤100 mantieneTj≈106°C;400mA con esos mismos supuestos da123°C y queda demasiado cerca del máximo.
- **Aire interno60°C:** el escenario250mA,IN≤5V,Rθ≤100 da107.5°C;300mA ya da116°C, sobre el objetivo110 aunque bajo125. ConIN4.6V y300mA el modelo da103.6°C.
- **Aire interno70°C:** no se aprueba el conjunto por extrapolación del regulador. Otros componentes, comoLM358DR comercial, tienen rango ambiente0–70°C, y su aire local/calentamiento debe revisarse. El receptorFS-iA6B externo se especifica hasta60°C de ambiente.
- Estos umbrales son condiciones de cálculo, no límites garantizados de laPCB. No se establece temperatura exterior admisible: falta el incremento dentro del gabinete y el calor deJetson/otros equipos.

Con el cobre y conexiones sólidas existentes, **no hay evidencia para descartar el lineal por defecto**. Tampoco se cierra la aprobación térmica de verano sin comprobar carga e instalación. Si se desea conservarlo, el criterio de primera placa es validar el escenario real frente a las curvas de este informe y mantener margen, en lugar de depender de protección térmica.

## Comprobación física pendiente

Sin iniciar movimiento ni conectar actuadores durante esta revisión:

1. Medir corriente de salida3.3V en reposo, control habitual,USB,Wi-Fi/OTA y transmisión representativa; registrar promedio y transitorios con instrumentos adecuados.
2. Medir IN/OUT deU1 y temperatura del aire local con gabinete representativo yJetson funcionando. Esperar estabilización térmica.
3. Medir temperatura del encapsulado y cobre con termopar correctamente instalado o cámara corregida por emisividad. No identificar temperatura superficial conTj sin la relación térmica adecuada.
4. Comprobar3.3V/ripple/reset con escalones y temperatura. La supervivencia térmica no garantiza regulación si falta dropout.
5. Definir un máximo de aire interno aceptable y un criterio de reducción de carga/ventilación, antes de aprobar servicio continuo.

No se hicieron estas pruebas en hardware. Las cuentas son reproducibles con [calculate_limits.py](calculate_limits.py); resultados [CSV](thermal_scenarios.csv) y[JSON](thermal_scenarios.json). No se modificó circuito,layout ni firmware.
