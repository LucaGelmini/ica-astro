# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import locale

# %%
# Por las dudas lo hago con las tres series: original, desestacionalizada y tendencia-ciclo
# Primero la tabla que se vería en la publicación
desest_tabla = pd.read_excel("./src/wrangling py/data/ICA_esqueleto.xlsx",sheet_name="c9",header=3)[3:].reset_index(drop=True)
df_plot_desest = pd.read_excel("./src/wrangling py/data/ICA_esqueleto.xlsx",sheet_name="dato graf deses")
df_plot_desest = df_plot_desest.set_index("fecha")

# %%
desest_tabla["Año"] = [int(round(x,0)) for x in desest_tabla.Año]
desest_tabla = desest_tabla.set_index(["Año","Mes"])

# %%
locale.setlocale(locale.LC_ALL, 'es_ES')
new_date = [d.strftime('%b %Y').replace(".","").capitalize() for d in df_plot_desest.index]
x = new_date
plot_desestacionalizado = go.Figure()
plot_desestacionalizado.add_trace(go.Scatter(x = new_date,
                         y = df_plot_desest["Serie original"].round(2),
                         name = "Serie original", mode = "lines+markers", line_width=2.5, hovertemplate="$%{y:,.0f}"))
plot_desestacionalizado.add_trace(go.Scatter(x = new_date, y = df_plot_desest["Serie desestacionalizada"].round(2),
                         name = "Serie desestacionalizada", mode = "lines",line_width = 2.5,hovertemplate="$%{y:,.0f}"))
plot_desestacionalizado.add_trace(go.Scatter(x = new_date, y = df_plot_desest["Tendencia-ciclo"].round(2),
                         name = "Tendencia-Ciclo", mode = "lines", line_width = 2.5,hovertemplate="$%{y:,.0f}"))
plot_desestacionalizado.update_xaxes(nticks = 10)
plot_desestacionalizado.update_yaxes(tickformat = ",")
plot_desestacionalizado.update_layout(separators = ",.",template = None, hovermode = "x unified",
                  font_family = "georgia",
                  legend = dict(
                      yanchor="top", orientation = "h",
       y=-0.1,
       xanchor="left",
       x=0.34
                  ))


