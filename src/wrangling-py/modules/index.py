# %%
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as io
import numpy as np
import locale
from modules.config.config import DIR

# %%
locale.setlocale(locale.LC_ALL, 'es_ES')

# %%
r2_df = pd.read_excel(
    f"{DIR}ICA_esqueleto.xlsx", sheet_name="R2", skiprows=3)
r2_df.fillna("")

# %%
header = [np.array(['', 'Exportación', 'Exportación', 'Exportación', 'Exportación', "Importación", "Importación", "Importación", "Importación", "Saldo", "Saldo"]),
          np.array(['', '2022e', '2021*', 'Variación porcentual igual período año anterior', 'Variación porcentual acumulado igual período año anterior',
                    '2022*', "2021*", 'Variación porcentual igual período año anterior', 'Variación porcentual acumulado igual período año anterior',
                    "2022*", "2021*"])]
c1 = pd.read_excel(f"{DIR}ICA_esqueleto.xlsx",
                   sheet_name="c 1", skiprows=11)

c1_columnas = ["<"+a+" - "+b+">" for a, b in zip(header[0], header[1])]
c1.columns = c1_columnas

# %%
c2 = pd.read_excel(f"{DIR}ICA_esqueleto.xlsx",
                   sheet_name="c 2", skiprows=5)
c2_columnas = [np.array(["Octubre 2022"]*4), np.array([" - "]*4),
               np.array(["", "Valor", "Precio", "Cantidad"])]

c2_columnas = ["<"+a+b+c+">" for a, b,
               c in zip(c2_columnas[0], c2_columnas[1], c2_columnas[2])]
c2.columns = c2_columnas
c2_expo = c2[:5]
c2_impo = c2[6:]
for (c, tipo) in [(c2_expo, 'Rubros'), (c2_impo, 'Usos')]:
    c.iloc[0, 0] = 'Total'
    c.columns = [f'<-{tipo}>', *c.columns[1:]]

# %%
balanza = pd.read_csv(
    f"{DIR}SerieHistorica.csv", sep=";", decimal=",")
balanza.index = pd.to_datetime(
    (balanza.Mes.astype(str) + "-"+balanza["Año"].astype(str)))  # type:ignore
balanza = balanza["2011":]

# %%
new_date = [d.strftime('%b %Y').replace(".", "").capitalize()
            for d in balanza.index]
x = new_date
plot_agregado = go.Figure()
plot_agregado.add_trace(
    go.Scatter(
        x=new_date,
        y=balanza.Exportaciones/1000000,
        name="Exportaciones",
        hovertemplate="$%{y:,.0f}"
    ))

plot_agregado.add_trace(
    go.Scatter(
        x=new_date,
        y=balanza.Importaciones/1000000,
        name="Importaciones",
        hovertemplate="$%{y:,.0f}"
    )
)
plot_agregado.add_trace(
    go.Bar(
        x=new_date,
        y=balanza['Saldo comercial']/1000000,
        name="Saldo",
        hovertemplate="$%{y:,.0f}"
    )
)
plot_agregado.update_layout(
    title_text = "",
    template="none", separators=",.", font_family="georgia")
plot_agregado.update_yaxes(tickformat=",",
                           dtick=1000)
plot_agregado.update_xaxes(rangeslider=dict(
    visible=True,
), nticks=10
)
plot_agregado.update_layout(hovermode="x unified", legend=dict(
    yanchor="top", orientation="h",
    y=1.16,
    xanchor="left",
    x=0.34))
plot_agregado.update_xaxes(tickangle=90)
