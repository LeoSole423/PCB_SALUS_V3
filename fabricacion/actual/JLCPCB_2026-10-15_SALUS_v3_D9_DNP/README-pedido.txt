SALUS v3 — 15/10/2026 — D9 NO MONTAR

D9 es DNP: no comprar, no montar y no sustituir por puente.
La huella y pistas se conservan. D7 permanece montado.
USB solo para datos/programacion/depuracion: alimentar la PCB externamente.
No se incorpora deteccion VBUS.

Archivos de carga: PCB_SALUS_v3-Gerbers.zip,
PCB_SALUS_v3-JLC-BOM.csv y PCB_SALUS_v3-JLC-CPL.csv.
BOM/CPL: 63 componentes SMD, sin D9; R4 permanece montada.
Los headers THT se montan manualmente.

Los Gerbers se reutilizan IDENTICOS de la entrega del 20/08/2026 con R4:
no cambio cobre, taladros ni mascaras. Las aperturas de pasta de D9
siguen presentes; solicitar omitir pasta en D9 si se desea, y comprobar
expresamente en el visor de montaje que no se coloque ningun componente alli.
Fuentes nuevas en origen/; validaciones nuevas en validacion/.
DRC: 0 sin conectar; 2 avisos SW conocidos; 4 agujeros mecanicos extra.
ERC: 6 avisos, sin errores. BOM/CPL validado sin errores.

Este paquete NO cierra los pendientes de la revision del 15/10/2026:
termica, acelerador, interfaces y mecanica siguen sujetos a validacion.
No es aprobacion incondicional para fabricar ni pedido realizado.

Actualizacion de abastecimiento 15/10/2026: C14/C16 pasan a Samsung
CL21A475KAQNNNE / C1779, 4.7uF 25V X5R +/-10% 0805 Basic.
Reemplazan C107125 sin stock; capacidad, tolerancia y huella se conservan.
Solicitud actual: 5 PCB totales, montaje SMD en 2; 3 sin componentes.
