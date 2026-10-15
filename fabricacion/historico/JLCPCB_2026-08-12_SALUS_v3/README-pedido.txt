PAQUETE DE FABRICACION Y ENSAMBLAJE — SALUS v3
Fecha de regeneracion: 2026-08-13
Origen: rama main, revision de consolidacion Basic

ESTADO DE LIBERACION
LISTO PARA CARGAR EN JLCPCB. Se corrigio la conexion de la etiqueta 3.3V_EXT
y se regeneraron ERC, DRC, BOM, posiciones y auditoria CPL. Los Gerbers,
taladros y render permanecen identicos: esta revision solo cambia valores y
datos de compra de pasivos 0603.

La advertencia anterior sobre ausencia de pasta en U1 y U8 era un falso
positivo del control auxiliar: ambas huellas implementan F.Paste mediante
ventanas separadas sin numero de pad, una tecnica normal para pads termicos.
U1 tiene 4 ventanas de pasta sobre el tab del pad 2. U8 tiene 9 ventanas de
pasta y 12 vias termicas en el pad GND 41. No fue necesario cambiar huellas.

CONFIGURACION PREVISTA EN JLCPCB
- Cantidad: 5 placas / 5 PCBA.
- PCB: 2 capas, FR-4, 1.6 mm, cobre 1 oz, mascara verde, serigrafia blanca.
- Acabado: HASL con plomo.
- Ensamblaje: Standard PCBA, cara superior (Top). Es obligatorio para este
  proyecto por la elegibilidad de montaje de U4 (BMI088) y U8
  (ESP32-S3-WROOM-1-N8R2); no seleccionar Economic PCBA.
- No pedir stencil: el montaje lo realiza JLCPCB.
- Cargar PCB_SALUS_v3-Gerbers.zip; cargar BOM y CPL por separado en PCBA.

CONTENIDO
- PCB_SALUS_v3-Gerbers.zip: exclusivamente archivos de fabricacion.
- PCB_SALUS_v3-JLC-BOM.csv: 25 lineas y 63 componentes, todos con LCSC.
- PCB_SALUS_v3-JLC-CPL.csv: 63 designadores en milimetros y cara Top,
  generado con tools/jlc_cpl.py y calibraciones verificadas en el visor JLCPCB.
- gerbers/: archivos sin comprimir, Excellon, informe de taladros y .gbrjob.
- origen/: exportaciones intermedias de KiCad/BOM para trazabilidad.
- validacion/: ERC, DRC, BOM/CPL, Gerbers, pasta, stock y controles visuales.

COMPONENTES EXCLUIDOS DEL MONTAJE JLCPCB (MANUALES)
J1,J2,J3,J4,J5,J6,J7,J8,J9,J10,J11,J12,J13,J14,J15,J17,J18,J19,J20,J21,
J22, JP1, JP2 y R4. Los headers/conectores THT se compran y sueldan de forma
manual. JP1, JP2 y R4 tambien quedan fuera de BOM/CPL y deben montarse de
acuerdo con la configuracion deseada.

VALIDACION REALIZADA
- ERC: 0 errores. Quedan 6 avisos activos y 1 aviso excluido ya existente:
  extremo corto de cable, tipos de pin de SW1/SW2, alias HBRIDGE_EN/HB_EN y
  conflicto excluido SDO1/SDO2 de U4. No impiden la exportacion de PCB/PCBA.
- La red /ALIMENTACION/3.3V_EXT llega correctamente a J20.1 y a su pista.
- DRC con zonas recalculadas: 0 errores y 0 conexiones sin rutear.
- Paridad esquema-PCB: 0 diferencias.
- DRC conserva solo 2 avisos lib_footprint_mismatch de SW1 y SW2. Se aceptan:
  pads, mascara y pasta coinciden con el componente C318884.
- BOM/CPL: 63 designadores en ambos archivos, sin duplicados ni ausentes;
  25 grupos de BOM con MPN, fabricante y numero LCSC.
- Consolidacion Basic: C6,C7,C12,C13,C15,C17-C23 usan C14663 (100 nF, 0603,
  Basic); R17 y R19 usan C25819 (47 kOhm, 0603, Basic). Se eliminaron C1590
  y C108463 de la BOM. El ahorro estimado para cinco PCBA es USD 5.60.
- La CPL conserva exactamente los mismos 63 designadores, posiciones,
  capas y rotaciones que la liberacion anterior.
- Gerbers: contorno cerrado de 100.05 x 100.05 mm, dos capas de cobre, todas
  las capas alineadas y taladros PTH/NPTH presentes.
- Pasta termica: U1 y U8 aprobados; detalle en validacion/cobertura_pasta.json.
- Render superior actualizado en validacion/render-superior.png.
- CPL final: 63 designadores, sin duplicados ni ausentes, validada contra BOM
  y placa actual. La auditoria, CPL cruda, revision de centroides y superposicion
  estan en validacion/cpl-candidate-*.
- Compensaciones confirmadas en el visor JLCPCB se guardan de forma versionada
  en config/jlcpcb-cpl.json y config/jlcpcb-cpl-observations-2026-08-12.json.

STOCK LCSC
La consulta actual confirma C14663 y C25819 como Basic, con stock suficiente
para cinco PCBA. Otras referencias pueden requerir verificacion en el visor
de JLCPCB antes de pagar; detalle: validacion/stock_LCSC.csv.

COMPROBACION FINAL OBLIGATORIA EN JLCPCB
1. Abrir el ZIP y confirmar 100.05 x 100.05 mm, 2 capas y orientacion.
2. Cargar BOM/CPL y confirmar que JLCPCB reconoce los 63 componentes.
3. Revisar en el visor pin 1, polaridad y rotacion de diodos, C30,
   U1/U2/U4-U8, SW1/SW2 y USB-C J16.
4. Confirmar visualmente las ventanas de pasta centrales de U1 y U8.
5. Confirmar stock y cualquier tarifa de componentes Extended.

SHA-256 (archivos de carga)
Los valores vigentes se encuentran tambien en CHECKSUMS-SHA256.txt.
6ee5002bde1fff0caad7f54dc98fefe96334ed9ef1e805ff14bcc706a5bb4e47  PCB_SALUS_v3-Gerbers.zip
f13a3babbc79ec71218ae51103612ef4ea92074adc0f4cb5e417bb843a23b9f9  PCB_SALUS_v3-JLC-BOM.csv
2bc02c03520af4c7ff43d2e0fb4eced395bdb52725917987f4055ff701b6ae9b  PCB_SALUS_v3-JLC-CPL.csv
