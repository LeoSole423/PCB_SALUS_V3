PAQUETE DE FABRICACION Y ENSAMBLAJE — SALUS v3
Fecha de generacion: 2026-08-20
Origen: PCB_SALUS_v3.kicad_pcb actual, KiCad 10.0.5

ESTADO
Paquete nuevo generado tras agregar cuatro agujeros de montaje M3 NPTH de
3.2 mm y redondear el contorno de placa. No sobrescribe los paquetes previos.
Las zonas de cobre se recalcularon antes de generar los Gerbers.

CONFIGURACION DEL PEDIDO JLCPCB
- Cantidad: 5 placas / 5 PCBA.
- PCB: 2 capas, FR-4 1.6 mm, cobre 1 oz, mascara verde, serigrafia blanca.
- Acabado: HASL con plomo.
- Ensamblaje: Standard PCBA, cara superior (Top). U4 (BMI088) y U8
  (ESP32-S3-WROOM-1-N8R2) requieren Standard PCBA; no seleccionar Economic.
- No pedir stencil: lo provee el proceso de montaje de JLCPCB.

ARCHIVOS PARA CARGAR
- PCB_SALUS_v3-Gerbers.zip: cargar en la cotizacion de PCB.
- PCB_SALUS_v3-JLC-BOM.csv y PCB_SALUS_v3-JLC-CPL.csv: cargar en PCBA.
- No incluir BOM, CPL ni README dentro del ZIP de Gerbers.

CONTENIDO Y VALIDACION
- Gerbers: F/B Cu, F/B Mask, F/B Paste, F/B SilkS, Edge.Cuts y Excellon.
- Contorno cerrado: 100.05 x 100.05 mm; dos capas de cobre.
- Taladros: 431 PTH y 6 NPTH, de los cuales cuatro son los agujeros M3 de
  3.2 mm (H1-H4), excluidos de BOM y CPL como corresponde.
- BOM: 25 lineas y 63 componentes de montaje; CPL: 63 designadores Top.
- BOM/CPL: sin duplicados, sin ausentes y validado con tools/jlc_cpl.py.
- DRC: cero errores de cobre, cero conexiones sin rutear y paridad electrica
  correcta. Quedan seis avisos aceptados: H1-H4 son huellas mecanicas extra
  sin simbolo de esquema; SW1/SW2 mantienen su aviso de huella de biblioteca.
- ERC: siete avisos existentes, cero errores.
- El analisis Gerber informa una advertencia de cobertura de F.Paste ya
  conocida por las ventanas de pasta de U1/U8; verificar visualmente en JLCPCB.

COMPROBACION FINAL EN JLCPCB
1. Confirmar dimensiones, contorno redondeado y los cuatro agujeros M3.
2. Cargar BOM/CPL y comprobar 63 componentes, todos en Top.
3. Revisar pin 1, polaridad y rotacion de diodos, C30, U1/U2/U4-U8, SW1/SW2
   y USB-C J16 en el visor de PCBA.
4. Confirmar stock y elegibilidad Standard PCBA antes de pagar.

SHA-256
4b5f4f1fb0d4a4b5cb2070ba38aae759d264c90bf1217e5d467e15d4c12454e3  PCB_SALUS_v3-Gerbers.zip
eed8bcc1538120209663b779e3c7be53acd6c2d8b62ca6154f92e5d332619046  PCB_SALUS_v3-JLC-BOM.csv
2bc02c03520af4c7ff43d2e0fb4eced395bdb52725917987f4055ff701b6ae9b  PCB_SALUS_v3-JLC-CPL.csv
