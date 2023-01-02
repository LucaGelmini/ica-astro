import plotly.io as io
import json
from modules.config.config import DIR_PLOTS


def genera_plot_json(plot,nombre:str):
    '''Crea un json con todo separado: titulo y plot'''
    dir = DIR_PLOTS+nombre+".json"
    io.write_json(plot, file=dir)

    with open(dir,'r') as file:
        coso=json.load(file)
        titulo = coso["layout"]["title"]["text"]
    coso["layout"]["title"]["text"] = ""
    with open(dir, 'w') as file:
        file.write(json.dumps({'title': titulo, 'plot': coso}))
