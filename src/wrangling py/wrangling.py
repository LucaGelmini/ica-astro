from modules.expo import df_grafico1_tabla, plot_expo_rubros, cuadro5, cuadro6
from modules.impo import df_grafico2_tabla, plot_impo_usos, cuadro7, cuadro8
from modules.index import r2_df, c1, c2_expo, c2_impo, balanza, plot_agregado
from modules.desestacional import plot_desestacionalizado, desest_tabla_expo, desest_tabla_impo, df_plot_desest_expo, df_plot_desest_impo
import plotly.io as io

# Exportar a json
# Grafos
io.write_json(plot_expo_rubros, file="./src/data/plots/plot_expo_rubros.json")
io.write_json(plot_impo_usos, file="./src/data/plots/plot_impo_usos.json")
io.write_json(plot_agregado, file="./src/data/plots/plot_agregado.json")
io.write_json(plot_desestacionalizado(df_plot_desest_expo),
              file="./src/data/plots/plot_desestacionalizado_expo.json")
io.write_json(plot_desestacionalizado(df_plot_desest_impo),
              file="./src/data/plots/plot_desestacionalizado_impo.json")
# Tablas
df_grafico1_tabla.to_json(
    "./src/data/cuadros/df_grafico1_tabla.json", force_ascii=False, orient='table')

cuadro5.to_json("./src/data/cuadros/cuadro5.json",
                force_ascii=False, orient='table')

cuadro6.to_json("./src/data/cuadros/cuadro6.json",
                force_ascii=False, orient='table')

df_grafico2_tabla.to_json(
    "./src/data/cuadros/df_grafico2_tabla.json", force_ascii=False, orient='table')

c1.to_json("./src/data/cuadros/c1.json", force_ascii=False, orient='table')

cuadro7.to_json("./src/data/cuadros/cuadro7.json",
                force_ascii=False, orient='table')

cuadro8.to_json(
    "./src/data/cuadros/cuadro8.json",
    force_ascii=False,
    orient='table'
)

r2_df.to_json("./src/data/cuadros/r2_df.json",
              force_ascii=False, orient='table')

c2_expo.to_json("./src/data/cuadros/c2_expo.json",
                force_ascii=False, orient='table')
c2_impo.to_json("./src/data/cuadros/c2_impo.json",
                force_ascii=False, orient='table')

balanza.to_json("./src/data/cuadros/balanza.json",
                force_ascii=False, orient='table')

desest_tabla_expo.to_json(
    "./src/data/cuadros/tabla desestacionalizada.json", force_ascii=False, orient='table')

desest_tabla_impo.to_json(
    "./src/data/cuadros/tabla desestacionalizada.json", force_ascii=False, orient='table')
