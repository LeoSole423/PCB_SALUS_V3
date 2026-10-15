# Preparacion de cotizacion JLCPCB — 15/10/2026

Solicitud: 5 PCB totales, de las cuales 2 con montaje SMD y 3 sin componentes. Los headers THT del paquete siguen para soldadura manual. No se ha pagado ni encargado fabricacion.

Se busca montaje Economic superior si todos los componentes y geometria son admitidos, FR4 2 capas 1.6 mm, verde/blanco, cobre 1 oz, HASL con plomo como entrega anterior, vias tentadas, sin extras de acabado, stencil separado, limpieza o recubrimiento. Las opciones efectivas y precio final deben comprobarse en el sitio.

La cotizacion anterior del carrito mostraba PCB $9.30 y Standard PCBA para 2 unidades $111.57, con C107125 sin stock. Es referencia observada, no precio del paquete nuevo ni total con envio/impuestos.

Sustitucion para C14/C16: YAGEO CC0805KKX5R6BB475 / C107125 (4.7uF 10V X5R +/-10% 0805) por Samsung CL21A475KAQNNNE / C1779 (4.7uF 25V X5R +/-10% 0805). Uso: desacoplo +3.3V e IMU_3.3; sin cambio de pistas ni valor nominal. JLCPCB mostro Basic, stock 2459174, precio inicial $0.0346; stock/precio son instantaneos y no reserva. Se cotejo documento Samsung, dimensiones 2.00+/-0.15 por 1.25+/-0.15 mm, altura 1.25+/-0.15 mm y X5R -55..85 C. No se atribuye una curva de sesgo DC no medida.

Fuente fabricante: https://media.digikey.com/pdf/Data%20Sheets/Samsung%20PDFs/CL21A475KAQNNNE_Spec.pdf

Se sincronizaron propiedades del esquema y PCB, BOM de seguimiento y BOM de montaje de la entrega D9_DNP. D9 permanece excluido. Otros IC se conservan; no sustituir por precio sin revisar pinout y comportamiento.

Resultado de comprobacion en el sitio: Economic no admite BMI088 C194919 ni ESP32-S3-WROOM-1-N8R2 C2913204 (ambos Standard Only). Se selecciona Standard superior para montar los 63 SMD previstos, sin excluir estos IC por ahorro.

Cotizacion nueva guardada: PCB $9.30, montaje Standard $112.18, total mercaderia $121.48 antes de envio/impuestos/cupones. Desglose montaje: setup25.75, stencil8.27, componentes32.43, feeders40.30, SMT1.63, rayosX3.30, embalaje0.50 USD. Fabricacion PCB24 horas sin recargo (PCBA Only); ensamblaje3–4 dias sin urgencia paga. Montaje2/5 confirmado; 26 grupos confirmados; D9 ausente. Se selecciono Circuit Control y se anoto expresamente robot terrestre, D9 no montar/puentear y headers THT fuera del montaje. No se pago.
