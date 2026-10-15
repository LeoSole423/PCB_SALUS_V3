SALUS v3 — paquete de fabricación y ensamblaje JLCPCB, revisión R4

Pedido: 5 placas, Standard PCBA, ensamblaje SMD cara superior.
PCB: 2 capas, FR-4 1,6 mm, cobre 1 oz, máscara verde, serigrafía blanca,
HASL con plomo.

Cambio de esta revisión
- R4 se monta: 120 ohm entre RS485_A y RS485_B.
- Parte: C22787 / 0603WAF1200T5E / UNI-ROYAL, 0603, Basic.
- Uso previsto actual: enlace RS-485 punto a punto entre SALUS y PZEM-017.

Archivos para cargar en JLCPCB
- PCB_SALUS_v3-Gerbers.zip
- PCB_SALUS_v3-JLC-BOM.csv
- PCB_SALUS_v3-JLC-CPL.csv

Validación
- BOM/CPL: 26 grupos y 64 componentes; sin faltantes, duplicados ni revisiones pendientes.
- DRC: cero conexiones sin rutear y sin errores. Avisos aceptados: SW1/SW2
  lib_footprint_mismatch; H1-H4 son agujeros mecánicos sin símbolo esquemático.
- ERC: 6 avisos históricos, sin errores.
- Gerbers: 2 capas, contorno 100,05 x 100,05 mm, PTH y 4 agujeros M3 NPTH.
- La advertencia GR-004 de pasta corresponde a aperturas térmicas segmentadas de U1/U8.

No se incluyen headers THT en BOM/CPL: se sueldan manualmente.
Antes de confirmar el pedido, revisar en el visor JLCPCB el pin 1 y rotación de
todos los componentes asimétricos, en particular U1, U2, U4-U8, SW1/SW2 y J16.
