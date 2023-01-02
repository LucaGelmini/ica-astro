import pandas as pd
import plotly.graph_objects as go
import numpy as np
from modules.config.config import DIR, DIC_MESES

df = pd.read_csv(f"{DIR}expo_impo_rubros_usos.csv",sep=",", encoding="latin-1")
df.valor = df.valor / 1000000 #En millones de USD
df = df.sort_values(["anio","mes"],ascending=True).reset_index(drop = True)
# df = df.sort_values(["valor"],ascending=False).reset_index(drop=True)
ultimo_anio = df.anio.iloc[-1]
ultimo_mes = df.mes.iloc[-1]
df.insert(3, "rubro_uso_corto", df.rubro_uso.apply(lambda s: s[s.find("(")+1:s.find(")")] if s != "Resto" else "Resto"))

df.rubro_uso = df.rubro_uso.apply(
    lambda x: x.split(" (",1)[0]
    )

#Funciones para encontrar las tablas agrupadas

def genera_uso_rubro_mensual(df, importacion:bool):
    valuacion = "Importaciones" if importacion else "Exportaciones"
    df_separada = df[df.comercio == valuacion].reset_index(drop=True)
    df_separada["Participación porcentual"] = df_separada['valor'] / df_separada.groupby(["anio","mes"])['valor'].transform('sum')
    df_separada["Variación porcentual"] = df_separada.groupby(['rubro_uso'])["valor"].pct_change(12,fill_method=None)
    # df_separada = df_separada[(df_separada.anio == ultimo_anio) & (df_separada.mes == ultimo_mes)].reset_index(drop = True)
    return df_separada

def genera_uso_rubro_acumulada(df, importacion:bool):
    valuacion = "Importaciones" if importacion else "Exportaciones"
    df_separada = df[df.comercio == valuacion].reset_index(drop=True)
    df_separada = df_separada[df_separada.mes <= ultimo_mes].reset_index(drop = True)
    df_separada = df_separada.groupby(["comercio","anio","rubro_uso", "rubro_uso_corto"],as_index=False).sum()
    df_separada["Participación porcentual"] = df_separada['valor'] / df_separada.groupby(["anio"])['valor'].transform('sum')
    df_separada["Variación porcentual"] = df_separada.groupby(['rubro_uso'])["valor"].pct_change(1,fill_method=None)
    # df_separada = df_separada[(df_separada.anio == ultimo_anio)].reset_index(drop = True)
    return df_separada

def genera_uso_rubro_agrupada():
    usos_mensual = genera_uso_rubro_mensual(df, importacion=True)
    rubros_mensual = genera_uso_rubro_mensual(df, importacion=False)
    df_mensual = pd.concat([usos_mensual, rubros_mensual]).reset_index(drop=True)
    df_mensual = df_mensual[(df_mensual.anio == ultimo_anio) & (df_mensual.mes == ultimo_mes)].reset_index(drop = True)
    usos_acumulada = genera_uso_rubro_acumulada(df, importacion=True)
    rubros_acumulada = genera_uso_rubro_acumulada(df, importacion=False)
    df_acumulada = pd.concat([usos_acumulada, rubros_acumulada]).reset_index(drop=True).drop("mes",axis=1)
    df_acumulada = df_acumulada[(df_acumulada.anio == ultimo_anio)].reset_index(drop = True)
    return df_mensual, df_acumulada

df_mensual, df_acumulada = genera_uso_rubro_agrupada()

def genera_var(df):
    # prueba["Variación porcentual"][-3:-1]
    impo_t_0 = (df[df.parent == "Importaciones"].value/(1+df[df.parent == "Importaciones"]["Variación porcentual"])).sum()
    impo_t = df[df.id == "Importaciones"].value.values[0]
    var_impo = impo_t/impo_t_0-1
    expo_t_0 = (df[df.parent == "Exportaciones"].value/(1+df[df.parent == "Exportaciones"]["Variación porcentual"])).sum()
    expo_t = df[df.id == "Exportaciones"].value.values[0]
    var_expo = expo_t/expo_t_0-1
    var_ica = (expo_t + impo_t)/(expo_t_0 + impo_t_0)-1
    variaciones = pd.Series([var_expo, var_impo, var_ica])
    df["Variación porcentual"].iloc[-3:] = variaciones
    return df

def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value'])
    total_pa_proporcion = df.valor.sum()
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value'])
        dfg = df.groupby(levels[i:]).sum()
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'ICA'
        df_tree['value'] = dfg[value_column]
        # df_tree['proporcion'] = dfg[color_columns] #debería ser la misma lcsm
        df_all_trees = pd.concat([df_all_trees,df_tree] ,ignore_index=True)
    total = pd.Series(dict(id='ICA', parent='',
                              value=df[value_column].sum(),
                            #   proporcion=1
                            ))
    df_all_trees = df_all_trees.append(total, ignore_index=True) #hay problema para concat una serie
    # df_all_trees = pd.concat([df_all_trees, total], ignore_index=True)
    #Agrego variables relevantes para el hover
    df_all_trees = df_all_trees.merge(df[["rubro_uso","Participación porcentual","Variación porcentual","rubro_uso_corto"]],
                       left_on = "id", right_on = "rubro_uso_corto", how="left")
    #El total comercializado para saber la prop de expo e impo
    total = df_all_trees.value.iloc[-1]
    prop_expo_impo = pd.Series([df_all_trees.value.iloc[-3]/total, df_all_trees.value.iloc[-2]/total,1]) #un uno para rellenar "ica"
    df_all_trees["Participación porcentual"].iloc[-3:] = prop_expo_impo
    df_all_trees.rubro_uso.iloc[-3:] = df_all_trees.id.iloc[-3:] #va a salir una advertencia horrible
    df_all_trees = genera_var(df_all_trees)
    return df_all_trees

def plot_sunburst_usos_rubros(acumulado:bool):
    df = df_acumulada if acumulado else df_mensual
    fecha = F"acumulado hasta {DIC_MESES[ultimo_mes]}" if acumulado else F"mes de {DIC_MESES[ultimo_mes]}"
    socios_sas_mensual_tree = build_hierarchical_dataframe(df=df, levels=["rubro_uso_corto", "comercio"],value_column="valor", color_columns = "valor")

    fig = go.Figure(go.Sunburst(
        labels=socios_sas_mensual_tree['id'],
        parents=socios_sas_mensual_tree['parent'],
        values=socios_sas_mensual_tree['value'],
        branchvalues='total',
        customdata = np.transpose([socios_sas_mensual_tree["rubro_uso"],
                                   socios_sas_mensual_tree["Variación porcentual"],
              ]),
        marker=dict(
            # colors=socios_sas_mensual_tree['color'],
            # colorscale='Sunsetdark',
            # cmid=average_score
            ),
        hovertemplate="<b>%{customdata[0]}</b> <br>Dólares: $%{value:,.2f}"
        "<br>Participación porcentual de %{entry}: %{percentEntry:.1%}"
        "<br>Variación porcentual: %{customdata[1]:.1%}"
        "<br<extra></extra>>",
        name='',
        maxdepth=3
        ))
    fig.update_layout(
        title_text = f"Intercambio Comercial Argentino {fecha}",
        template = None,
                    margin = {"t":20, "b":20, "l":20, "r":20},
                    separators = ",." ,
                    #   uniformtext=dict(minsize=10, mode='hide'),
                    font_family = "verdana",
                    # height = 1000,
                    # width = 1000,
                    paper_bgcolor='rgba(0,0,0,0)',
                    ) 
    
    return fig

def plot_barras_usos_rubros(importacion:bool, acumulado:bool):
       titulo = "Importaciones por usos económicos. " if importacion else "Exportaciones por grandes rubros. "
       if acumulado:
              df_rubro_uso = genera_uso_rubro_acumulada(df, importacion=importacion)
              titulo_plot = f"{titulo}Acumulado hasta {DIC_MESES[ultimo_mes]} del {ultimo_anio}"
              custom_data_1 = f"{ultimo_anio-1}"
              custom_data_2 = f"{ultimo_anio}"
       else:
              df_rubro_uso = genera_uso_rubro_mensual(df, importacion=importacion)[genera_uso_rubro_mensual(df, importacion=importacion).mes == ultimo_mes].reset_index(drop = True)
              titulo_plot = f"{titulo} {ultimo_anio}"
              custom_data_1 = f"{DIC_MESES[ultimo_mes].capitalize()} {ultimo_anio-1}"
              custom_data_2 = f"{DIC_MESES[ultimo_mes].capitalize()} {ultimo_anio}"
       
       df_rubro_uso = df_rubro_uso.sort_values("valor",ascending=False)
       eje_x = df_rubro_uso[df_rubro_uso.anio==ultimo_anio].rubro_uso.unique()
              
       fig = go.Figure(data = [
       go.Bar(name = custom_data_1, x = df_rubro_uso[df_rubro_uso.anio==ultimo_anio-1].rubro_uso_corto, y = df_rubro_uso[df_rubro_uso.anio==ultimo_anio-1].valor,
              customdata = np.transpose([[custom_data_1]*len(eje_x),
              eje_x,
              df_rubro_uso[df_rubro_uso.anio==ultimo_anio-1]["Participación porcentual"],
              # df_rubro_uso[df_rubro_uso.anio==ultimo_anio-1]["Variación porcentual"],
              ]),
              hovertemplate = "<b>%{customdata[0]}</b><br<extra></extra>>"+
              "%{customdata[1]}<br>Dólares $%{y:,.1f}<br>Participación porcentual: %{customdata[2]:.1%}"              
              , ) ,         
       go.Bar(name = custom_data_2, x = df_rubro_uso[df_rubro_uso.anio==ultimo_anio].rubro_uso_corto, y = df_rubro_uso[df_rubro_uso.anio==ultimo_anio].valor,
              customdata = np.transpose([[custom_data_2]*len(eje_x),
                                          eje_x,
                                          df_rubro_uso[df_rubro_uso.anio==ultimo_anio]["Participación porcentual"],
              df_rubro_uso[df_rubro_uso.anio==ultimo_anio]["Variación porcentual"],
              ]),
              hovertemplate = "<b>%{customdata[0]}</b><br><extra></extra>"+
              "%{customdata[1]}<br>Dólares $%{y:,.1f}<br>Participación porcentual: %{customdata[2]:.1%}"+
              "<br>Variación porcentual: %{customdata[3]:.1%}",           
              ), #Como odio esta mierda
       ]
       )
       fig.update_yaxes(tickformat = ",", title_text = "En millones de USD")


       fig.update_layout(barmode='group', template = None, separators=",.", title_text = titulo_plot,
                     font_family = "verdana",
                     paper_bgcolor='rgba(0,0,0,0)',
                     legend=dict(
              yanchor="top", orientation = "h",
              y=1.15,
              xanchor="left", 
              x=0.41))
       return fig
   


