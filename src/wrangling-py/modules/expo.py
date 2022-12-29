# %%
import pandas as pd
import plotly.express as px
import plotly.io as io

# %%
df_grafico1_tabla = pd.read_excel("./src/wrangling-py/data/ICA_esqueleto.xlsx",
                                  sheet_name="graf1 expo.rubros.", skipfooter=1, skiprows=1)
df_grafico1_tabla

# %%
df_grafico1 = df_grafico1_tabla[["Rubros", "Octubre 2021*", "Octubre 2022e"]].melt(
    id_vars="Rubros", value_name="Dólares", var_name="Período")
plot_expo_rubros = px.histogram(df_grafico1[df_grafico1.Rubros != "Total"],
                                x="Rubros", y="Dólares", color="Período", barmode="group", template="none")
plot_expo_rubros.update_yaxes(tickformat=",", title_text='En millones de USD')
plot_expo_rubros.update_layout(separators=",.", font_family='georgia', title_text="Exportación por rubros económicos. Octubre de 2022 y octubre de 2021",
                               legend=dict(
                                   yanchor="top", orientation="h",
                                   y=1.07,
                                   xanchor="left",
                                   x=0.3))
# type:ignore
plot_expo_rubros.data[
    0].hovertemplate = 'Periodo: Octubre 2021*<br>Rubro: %{x}<br>Dolares: $%{y}<extra></extra>'  # type:ignore
# type:ignore
plot_expo_rubros.data[
    1].hovertemplate = 'Periodo: Octubre 2022e<br>Rubro: %{x}<br>Dolares: $%{y}<extra></extra>'  # type:ignore

# %%
columnas = ["Rubros", "Octubre 2022e", "Octubre 2021*", "Octubre Variación porcentual",
            "Diez meses 2022e", "Diez meses 2021*", "Diez meses Variación porcentual"]
cuadro5 = pd.read_excel("./src/wrangling-py/data/ICA_esqueleto.xlsx",
                        sheet_name="c5", skipfooter=0, skiprows=4, names=columnas)
cuadro5.head()

# %%
cuadro6 = pd.read_excel("./src/wrangling-py/data/ICA_esqueleto.xlsx",
                        sheet_name="c6", skipfooter=0, skiprows=3)[1:]
cuadro6 = cuadro6.fillna("-")
cuadro6.head()
