# Entregas de fabricación

La entrega más reciente conservada es [SALUS v3 del 20/08/2026 con R4 montada](actual/JLCPCB_2026-08-20_SALUS_v3_R4/README-pedido.txt).
El sufijo R4 identifica la resistencia de terminación RS-485 de 120 ohm.
No indica una versión mayor v4 ni confirma que se haya realizado el pedido.

| Carpeta | Uso |
|---|---|
| `actual/JLCPCB_2026-08-20_SALUS_v3_R4/` | Última entrega; 64 componentes SMD, R4 montada. |
| `historico/JLCPCB_2026-08-20_SALUS_v3/` | Entrega previa del mismo día; agujeros M3 y contorno redondeado, 63 componentes. |
| `historico/JLCPCB_2026-08-12_SALUS_v3/` | Entrega anterior, con archivos de montaje actualizados el 13/08. |
| `cotizaciones/JLCPCB_cotizacion_2026-07-30_v2/` | Cotización histórica; conservar su nombre original. |
| `cotizaciones/JLCPCB_cotizacion_2026-07-31_linear_v1/` | Cotización de la variante lineal. |

## Uso y conservación

Cada paquete conserva su nombre, ZIP, BOM, CPL, fuentes e informes existentes.
Los informes son evidencia de su fecha de generación, no una nueva validación.
Los archivos de entrega no se regeneraron durante la organización del 15/10/2026.
Los manifiestos de checksum usan nombres relativos al paquete. Para verificarlos:

```bash
cd fabricacion/actual/JLCPCB_2026-08-20_SALUS_v3_R4
sha256sum -c CHECKSUMS-SHA256.txt
```

Abrir el proyecto editable desde la raíz del repositorio. Las copias de `origen/`
son instantáneas de referencia y pueden no incluir bibliotecas para abrirse aisladas.
Antes de fabricar, seguir el README del paquete y revisar el visor de montaje.
Para una nueva entrega, crear un paquete fechado; trasladar el anterior a
`historico/`, actualizar este índice y las referencias documentales.
