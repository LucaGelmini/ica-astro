import pandas as pd
import plotly.graph_objects as go
from modules.config.config import DIC_MESES, DIR, CONTINENTES_DICT


def genera_tablas_con_continentes(df):
    df["continente"] = df.pais_cod.apply(lambda x: CONTINENTES_DICT[str(x)[0]])
    df.pais_descri = df.pais_descri.apply(lambda x: x.capitalize())
    df = df.sort_values(["anio","mes"],ascending=True).reset_index(drop=True)
    return df    

def genera_tablas_acumulado_y_mensual(df, comercio):
    valuacion = "cif" if comercio == "impo" else "fob"
    # Los datos mensuales
    ultimo_mes = df.mes.iloc[-1]
    ultimo_anio = df.anio.iloc[-1]
    socios_sas_mensual = df.copy()
    socios_sas_mensual["Variación porcentual"] = socios_sas_mensual.groupby(['pais_cod', 'pais_descri'])[valuacion].pct_change(12,fill_method=None)
    socios_sas_mensual = socios_sas_mensual[(socios_sas_mensual.anio == ultimo_anio)&(socios_sas_mensual.mes == ultimo_mes)].reset_index(drop=True)
    socios_sas_mensual["Participación Porcentual"] = socios_sas_mensual[valuacion] / socios_sas_mensual[valuacion].sum()
    
    # Acumulados
    socios_sas_acumulado = df[(df.mes <= ultimo_mes)].reset_index(drop=True).copy()
    socios_sas_acumulado = socios_sas_acumulado.groupby(["anio","pais_descri","pais_cod","continente"],as_index=False).sum().drop("mes",axis=1)
    socios_sas_acumulado["Variación porcentual"] = socios_sas_acumulado.groupby(['pais_cod', 'pais_descri'])[valuacion].pct_change(fill_method=None)
    socios_sas_acumulado = socios_sas_acumulado[socios_sas_acumulado.anio == 2022].reset_index(drop=True).drop("anio",axis=1)
    socios_sas_acumulado["Participación Porcentual"] = socios_sas_acumulado[valuacion] / socios_sas_acumulado[valuacion].sum()
    
    return socios_sas_acumulado, socios_sas_mensual

def genera_tabla_presentable_mensual(df_mensual, comercio):
    valuacion = "cif" if comercio == "impo" else "fob"
    socios_sas_mensual_presentable = df_mensual.rename({"pais_descri":"País",valuacion: "Millones de dólares"}, axis = 1).copy()
    socios_sas_mensual_presentable.drop(["anio","mes","pais_cod","continente"],axis = 1, inplace=True)
    socios_sas_mensual_presentable = socios_sas_mensual_presentable.sort_values("Millones de dólares",ascending=False).reset_index(drop=True)
    socios_sas_mensual_presentable = socios_sas_mensual_presentable[:10]
    total = df_mensual[valuacion].sum()
    sub_total = socios_sas_mensual_presentable[:10]["Millones de dólares"].sum()
    socios_sas_mensual_presentable.loc[-1] = ["Resto", (total-sub_total),0, (total-sub_total)/total]
    socios_sas_mensual_presentable = socios_sas_mensual_presentable.reset_index(drop=True)
    return socios_sas_mensual_presentable
    
def genera_tabla_presentable_acumulado(df_acumulado, comercio):
    #incorporar comercio
    valuacion = "cif" if comercio == "impo" else "fob"
    socios_sas_acumulado_presentable = df_acumulado.rename({"pais_descri":"País",valuacion: "Millones de dólares"}, axis = 1).copy()
    socios_sas_acumulado_presentable.drop(["pais_cod","continente"],axis = 1, inplace=True)
    socios_sas_acumulado_presentable = socios_sas_acumulado_presentable.sort_values("Millones de dólares",ascending=False).reset_index(drop=True)
    total = df_acumulado[valuacion].sum()
    sub_total = socios_sas_acumulado_presentable[:10]["Millones de dólares"].sum()
    socios_sas_acumulado_presentable = socios_sas_acumulado_presentable[:10]
    socios_sas_acumulado_presentable.loc[-1] = ["Resto", (total-sub_total),0, (total-sub_total)/total]
    socios_sas_acumulado_presentable = socios_sas_acumulado_presentable.reset_index(drop=True)
    return socios_sas_acumulado_presentable
    
#IMPORTACIONES
socios_sas_impo = pd.read_csv(f"{DIR}socios_impo.csv", sep=";")
socios_sas_impo.cif = socios_sas_impo.cif/1000000

#Agregamos continentes y capitalizamos los países
socios_sas_impo = genera_tablas_con_continentes(socios_sas_impo)

#última fecha de los datos. Útil para los gráficos
ultimo_mes = socios_sas_impo.mes.iloc[-1]
ultimo_anio = socios_sas_impo.anio.iloc[-1]

# Tablas mensuales y acumuladas. Importan las presentables
socios_sas_impo_acumulado, socios_sas_impo_mensual = genera_tablas_acumulado_y_mensual(socios_sas_impo, "impo")

socios_sas_impo_mensual_presentable = genera_tabla_presentable_mensual(socios_sas_impo_mensual, "impo")

socios_sas_impo_acumulado_presentable = genera_tabla_presentable_acumulado(socios_sas_impo_acumulado, "impo")

#EXPORTACIONES
socios_sas_expo = pd.read_csv(f"{DIR}socios_expo.csv", sep=";")
socios_sas_expo.fob = socios_sas_expo.fob/1000000

#Agregamos continentes y capitalizamos los países
socios_sas_expo = genera_tablas_con_continentes(socios_sas_expo)

# Tablas mensuales y acumuladas. Importan las presentables
socios_sas_expo_acumulado, socios_sas_expo_mensual = genera_tablas_acumulado_y_mensual(socios_sas_expo, "expo")

socios_sas_expo_mensual_presentable = genera_tabla_presentable_mensual(socios_sas_expo_mensual, "expo")

socios_sas_expo_acumulado_presentable = genera_tabla_presentable_acumulado(socios_sas_expo_acumulado, "expo")

# GRÁFICOS

def plot_anillo_socios(acumulado:bool):
    df = socios_sas_expo_acumulado_presentable if acumulado else socios_sas_expo_mensual_presentable
    fecha = f"Acumulado hasta {DIC_MESES[ultimo_mes]} de {ultimo_anio}" if acumulado else f"Mes de {DIC_MESES[ultimo_mes]}"
    total = "{:,d}".format(int(round(df['Millones de dólares'].sum(),0))).replace(",",".")+"M"
    fig = go.Figure(data=[go.Pie(labels=df.País, values=df['Millones de dólares'], hole=.5)])
    fig.update_layout(title_text = f"Principales países de exportación: {fecha}", template = None, font_family = "verdana",
                    margin = dict(t=70, l=10, r=10, b=30), separators = ",.",
                    annotations = [dict(text = f"{total}", showarrow = False, font_size = 20)],
                    showlegend= False,
                    paper_bgcolor='rgba(0,0,0,0)')
    fig.update_traces(textposition='inside', textinfo='label+percent+label')
    return fig

def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    total_pa_color = df.cif.sum()
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dfg = df.groupby(levels[i:]).sum()
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'Importaciones'
        df_tree['value'] = dfg[value_column]
        
        df_tree['color'] = dfg[color_columns]/total_pa_color
        df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
        # df_all_trees = pd.concat([df_all_trees,df_tree] ,ignore_index=True)
    total = pd.Series(dict(id='Importaciones', parent='',
                              value=df[value_column].sum(),
                              color=df[color_columns]
                            ))
    df_all_trees = df_all_trees.append(total, ignore_index=True)
    #para reemplazar el nan del total
    df_all_trees.color.iloc[-1] = 1
    # df_all_trees =pd.concat([df_all_trees,total], ignore_index=True)
    return df_all_trees

def plot_sunburst_socios(acumulado:bool):
    df = socios_sas_impo_acumulado if acumulado else socios_sas_impo_mensual
    fecha = "acumulado hasta noviembre" if acumulado else "mes de noviembre"
    socios_sas_mensual_tree = build_hierarchical_dataframe(df=df, levels=["pais_descri", "continente"],value_column="cif", color_columns = "cif")

    fig = go.Figure(go.Sunburst(
        labels=socios_sas_mensual_tree['id'],
        parents=socios_sas_mensual_tree['parent'],
        values=socios_sas_mensual_tree['value'],
        branchvalues='total',
        marker=dict(
            colors=socios_sas_mensual_tree['color'],
            colorscale='Sunsetdark',
            # cmid=average_score
            ),
        hovertemplate='<b>%{label} </b> <br> CIF: $%{value:,.2f}<br> Proporcion: %{color:.2%}', #Me jode la proporcion, sí o sí entra por color
        name='',
        maxdepth=2
        ))
    fig.update_layout(title_text = f"Principales países de importación: {fecha}", template = None,
                    margin = {"t":70, "b":20, "l":10, "r":10},separators = ",." ,
                    #   uniformtext=dict(minsize=10, mode='hide'),
                    font_family = "verdana",
                    paper_bgcolor='rgba(0,0,0,0)',
                    ) 
    
    return fig

# Exportaciones

tablas_socios = [
socios_sas_impo_mensual_presentable,
socios_sas_impo_acumulado_presentable,
socios_sas_expo_mensual_presentable,
socios_sas_expo_acumulado_presentable,]

plots_socios = [
plot_sunburst_socios(acumulado=False),
plot_sunburst_socios(acumulado=True),
plot_anillo_socios(acumulado=False),
plot_anillo_socios(acumulado=True)]