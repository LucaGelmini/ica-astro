# Tanto expo como impo van a quedar en desuso
from modules.expo import df_grafico1_tabla, cuadro5, cuadro6
from modules.impo import df_grafico2_tabla, cuadro7, cuadro8
###
from modules.config.utils import genera_plot_json
from modules.config.config import DIR_CUADROS
from modules.index import r2_df, c1, c2_expo, c2_impo, balanza, plot_agregado
from modules.desestacional import plot_desestacionalizado, desest_tabla_expo, desest_tabla_impo, df_plot_desest_expo, df_plot_desest_impo
from modules.socios import tablas_socios, plots_socios
from modules.rubros_usos import plot_barras_usos_rubros, plot_sunburst_usos_rubros
import plotly.io as io

# Exportar a json
# Grafos


genera_plot_json(plot_barras_usos_rubros(importacion=False,acumulado=False), "barras_expo_mensual")
genera_plot_json(plot_barras_usos_rubros(importacion=False,acumulado=True), "barras_expo_acumulado")
genera_plot_json(plot_barras_usos_rubros(importacion=True,acumulado=False), "barras_impo_mensual")
genera_plot_json(plot_barras_usos_rubros(importacion=True,acumulado=True), "barras_impo_acumulado")

genera_plot_json(plot_sunburst_usos_rubros(acumulado=False), "sunburst_rubros_usos_mensual")
genera_plot_json(plot_sunburst_usos_rubros(acumulado=True), "sunburst_rubros_usos_acumulado")

genera_plot_json(plot_agregado,"plot_agregado") #no tiene titulo
genera_plot_json(plot_desestacionalizado(df_plot_desest_expo),"plot_desestacionalizado_expo") #no tiene titulo
genera_plot_json(plot_desestacionalizado(df_plot_desest_impo), "plot_desestacionalizado_impo") #no tiene titulo

genera_plot_json(plots_socios[0], "sunburst_socios_impo_mensual")
genera_plot_json(plots_socios[1], "sunburst_socios_impo_acumulado")
genera_plot_json(plots_socios[2], "anillo_socios_expo_mensual")
genera_plot_json(plots_socios[3], "anillo_socios_expo_acumulado")

# Tablas
df_grafico1_tabla.to_json(
    f"{DIR_CUADROS}df_grafico1_tabla.json", force_ascii=False, orient='table')

cuadro5.to_json(f"{DIR_CUADROS}cuadro5.json",
                force_ascii=False, orient='table')

cuadro6.to_json(f"{DIR_CUADROS}cuadro6.json",
                force_ascii=False, orient='table')

df_grafico2_tabla.to_json(
    f"{DIR_CUADROS}df_grafico2_tabla.json", force_ascii=False, orient='table')

c1.to_json(f"{DIR_CUADROS}c1.json", force_ascii=False, orient='table')

cuadro7.to_json(f"{DIR_CUADROS}cuadro7.json",
                force_ascii=False, orient='table')

cuadro8.to_json(
    f"{DIR_CUADROS}cuadro8.json",
    force_ascii=False,
    orient='table'
)

r2_df.to_json(f"{DIR_CUADROS}r2_df.json",
              force_ascii=False, orient='table')

c2_expo.to_json(f"{DIR_CUADROS}c2_expo.json",
                force_ascii=False, orient='table')
c2_impo.to_json(f"{DIR_CUADROS}c2_impo.json",
                force_ascii=False, orient='table')

balanza.to_json(f"{DIR_CUADROS}balanza.json",
                force_ascii=False, orient='table')

desest_tabla_expo.to_json(
    f"{DIR_CUADROS}tabla desestacionalizada expo.json", force_ascii=False, orient='table')

desest_tabla_impo.to_json(
    f"{DIR_CUADROS}tabla desestacionalizada impo.json", force_ascii=False, orient='table')

tablas_socios[0].to_json(f"{DIR_CUADROS}socios_impo_mensual.json",
         force_ascii=False, orient='table')
tablas_socios[1].to_json(f"{DIR_CUADROS}socios_impo_acumulado.json",
         force_ascii=False, orient='table')
tablas_socios[2].to_json(f"{DIR_CUADROS}socios_expo_mensual.json",
         force_ascii=False, orient='table')
tablas_socios[3].to_json(f"{DIR_CUADROS}socios_expo_acumulado.json",
              force_ascii=False, orient='table')
