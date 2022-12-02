from modules.expo import df_grafico1_tabla, plot_expo_rubros,cuadro5,cuadro6
from modules.impo import df_grafico2_tabla, plot_impo_usos, cuadro7, cuadro8
from modules.index import r2_df, c1, c2, balanza, plot_agregado
import plotly.io as io
import json

# Exportar a json
#Grafos
io.write_json(plot_expo_rubros, file = "./src/data/plot_expo_rubros.json")
io.write_json(plot_impo_usos, file = "./src/data/plot_impo_usos.json")
io.write_json(plot_agregado, file = "./src/data/plot_agregado.json")

#Tablas


df_grafico1_tabla.to_json("./src/data/df_grafico1_tabla.json",force_ascii=False)
cuadro5.to_json("./src/data/cuadro5.json",force_ascii=False)
cuadro6.to_json("./src/data/cuadro6.json",force_ascii=False)
df_grafico2_tabla.to_json("./src/data/df_grafico2_tabla.json",force_ascii=False)
c1.to_json("./src/data/c1.json",force_ascii=False)
cuadro7.to_json("./src/data/cuadro7.json",force_ascii=False)
cuadro8.to_json("./src/data/cuadro8.json",force_ascii=False)
r2_df.to_json("./src/data/r2_df.json",force_ascii=False)
c2.to_json("./src/data/c2.json",force_ascii=False)
balanza.to_json("./src/data/balanza.json",force_ascii=False)
