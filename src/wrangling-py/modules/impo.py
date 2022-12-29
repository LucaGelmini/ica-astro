# %%
import pandas as pd
import plotly.express as px
import plotly.io as io

# %%
df_grafico2_tabla = pd.read_excel(
    "./src/wrangling-py/data/ICA_esqueleto.xlsx", sheet_name="graf2 impo.usos.", skiprows=1)
df_grafico2_tabla = df_grafico2_tabla[df_grafico2_tabla.columns[[
    0, 1, 2]]].dropna(axis=0)  # type:ignore
df_grafico2_tabla[df_grafico2_tabla.columns[1]
                  ] = df_grafico2_tabla[df_grafico2_tabla.columns[1]].astype(int)
df_grafico2_tabla

# %%
df_grafico2 = df_grafico2_tabla[["Usos", "Octubre 2021*", "Octubre 2022*"]].melt(
    id_vars="Usos", value_name="Dólares", var_name="Período")
plot_impo_usos = px.histogram(df_grafico2[df_grafico2.Usos != "Total"], x="Usos", y="Dólares", color="Período", barmode="group", template="none",
                              hover_data=["Período", "Dólares"],
                              labels={
    "Usos": "Uso",
    "sum of Dólares": "Dólares"
})
plot_impo_usos.update_yaxes(tickformat=",", title_text='En millones de USD')
plot_impo_usos.update_layout(separators=",.", font_family='georgia', title_text="Importación por usos económicos. Octubre de 2022 y octubre de 2021",
                             legend=dict(
                                 yanchor="top", orientation="h",
                                 y=1.07,
                                 xanchor="left",
                                 x=0.3))

# type:ignore
# type:ignore
plot_impo_usos.data[0].hovertemplate = 'Periodo: Octubre 2021*<br>Uso: %{x}<br>Dolares: $%{y}<extra></extra>'
# type:ignore
# type:ignore
plot_impo_usos.data[1].hovertemplate = 'Periodo: Octubre 2022*<br>Uso: %{x}<br>Dolares: $%{y}<extra></extra>'


# io.write_json(plot_impo_usos, file = "./src/wrangling-py/data/impo_usos.json")
plot_impo_usos

# %%
# Aclarar que es en millones de USD
cuadro7 = pd.read_excel(
    "./src/wrangling-py/data/ICA_esqueleto.xlsx", sheet_name="c7", skiprows=4)[1:]
cuadro7.head()

# %%
cuadro8 = pd.read_excel(
    "./src/wrangling-py/data/ICA_esqueleto.xlsx", sheet_name="c8", skiprows=3)[1:]
cuadro8 = cuadro8.fillna("-")
cuadro8.head()
