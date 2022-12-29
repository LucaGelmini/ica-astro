import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv("./src/wrangling-py/data/expo_impo_rubros_usos.csv",
                 sep=",", encoding="latin-1")
df.valor = df.valor / 1000000  # En millones de USD
ultimo_anio = df.sort_values(["anio", "mes"], ascending=True).anio.iloc[-1]
ultimo_mes = df.sort_values(["anio", "mes"], ascending=True).mes.iloc[-1]

# Funciones para encontrar las tablas agrupadas


def genera_uso_rubro_mensual(df, comercio):
    valuacion = "Importaciones" if comercio == "impo" else "Exportaciones"
    df_separada = df[df.comercio == valuacion].reset_index(drop=True)
    df_separada["Participación porcentual"] = df_separada['valor'] / \
        df_separada.groupby(["anio", "mes"])['valor'].transform('sum')
    df_separada["Variación porcentual"] = df_separada.groupby(
        ['rubro_uso'])["valor"].pct_change(12, fill_method=None)
    df_separada = df_separada[(df_separada.anio == ultimo_anio) & (
        df_separada.mes == ultimo_mes)].reset_index(drop=True)
    return df_separada


def genera_uso_rubro_acumulada(df, comercio):
    valuacion = "Importaciones" if comercio == "impo" else "Exportaciones"
    df_separada = df[df.comercio == valuacion].reset_index(drop=True)
    df_separada = df_separada[df_separada.mes <=
                              ultimo_mes].reset_index(drop=True)
    df_separada = df_separada.groupby(
        ["comercio", "anio", "rubro_uso"], as_index=False).sum()
    df_separada["Participación porcentual"] = df_separada['valor'] / \
        df_separada.groupby(["anio"])['valor'].transform('sum')
    df_separada["Variación porcentual"] = df_separada.groupby(
        ['rubro_uso'])["valor"].pct_change(1, fill_method=None)
    df_separada = df_separada[(
        df_separada.anio == ultimo_anio)].reset_index(drop=True)
    return df_separada


def genera_uso_rubro_agrupada():
    usos_mensual = genera_uso_rubro_mensual(df, "impo")
    rubros_mensual = genera_uso_rubro_mensual(df, "expo")
    df_mensual = pd.concat([usos_mensual, rubros_mensual]
                           ).reset_index(drop=True)
    usos_acumulada = genera_uso_rubro_acumulada(df, "impo")
    rubros_acumulada = genera_uso_rubro_acumulada(df, "expo")
    df_acumulada = pd.concat([usos_acumulada, rubros_acumulada]).reset_index(
        drop=True).drop("mes", axis=1)
    return df_mensual, df_acumulada


df_mensual, df_acumulada = genera_uso_rubro_agrupada()

DIC_MESES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre"
}


def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    total_pa_color = df.valor.sum()
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dfg = df.groupby(levels[i:]).sum()
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'ICA'
        df_tree['value'] = dfg[value_column]

        # df_tree['color'] = dfg[color_columns]/total_pa_color
        df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
        # df_all_trees = pd.concat([df_all_trees,df_tree] ,ignore_index=True)
    total = pd.Series(dict(id='ICA', parent='',
                              value=df[value_column].sum(),
                           #   color=df[color_columns]
                           ))
    df_all_trees = df_all_trees.append(total, ignore_index=True)
    # para reemplazar el nan del total
    # df_all_trees.color.iloc[-1] = 1
    # df_all_trees =pd.concat([df_all_trees,total], ignore_index=True)
    return df_all_trees


def plot_sunburst_socios(df_impo, acumulado: bool):
    fecha = F"acumulado hasta {DIC_MESES[ultimo_mes]}" if acumulado else F"mes de {DIC_MESES[ultimo_mes]}"
    socios_sas_mensual_tree = build_hierarchical_dataframe(df=df_impo, levels=[
                                                           "rubro_uso", "comercio"], value_column="valor", color_columns="valor")

    fig = go.Figure(go.Sunburst(
        labels=socios_sas_mensual_tree['id'],
        parents=socios_sas_mensual_tree['parent'],
        values=socios_sas_mensual_tree['value'],
        branchvalues='total',
        marker=dict(
            # colors=socios_sas_mensual_tree['color'],
            # colorscale='Sunsetdark',
            # cmid=average_score
        ),
        # Me jode la proporcion, sí o sí entra por color
        hovertemplate='<b>%{label} </b> <br> CIF: $%{value:,.2f}<br> Proporcion: %{color:.2%}',
        name='',
        maxdepth=2
    ))
    fig.update_layout(title_text=f"Principales socios comerciales {fecha}", template=None,
                      margin={"t": 70, "b": 20, "l": 10, "r": 10}, separators=",.",
                      #   uniformtext=dict(minsize=10, mode='hide'),
                      font_family="verdana",
                      # paper_bgcolor='rgba(0,0,0,0)',
                      )

    return fig


# Exportaciones
plots_rubros_usos = [
    plot_sunburst_socios(df_acumulada, acumulado=True),
    plot_sunburst_socios(df_mensual, acumulado=False)]
