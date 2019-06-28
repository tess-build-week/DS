from flask import Flask, render_template, request, make_response
import numpy as np
import requests
import pandas as p
from IPython.display import display, HTML
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from matplotlib.pyplot import figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io


import mpld3
from mpld3 import fig_to_html, plugins
planeturl = "https://exo.mast.stsci.edu/api/v0.1/exoplanets/"
dvurl = "https://exo.mast.stsci.edu/api/v0.1/dvdata/tess/"
header={}


app = Flask(__name__)

# receive tessid, sector name
@app.route('/planet/<planet_name>/')

def default(planet_name):
    planet_name = "WASP-18"
    #planet_name = "TIC 117739806"
    planet_name = planet_name.replace('%20', ' ').replace('+', ' ')

    url = planeturl + "/identifiers/"

    myparams = {"name": planet_name}

    r = requests.get(url=url, params=myparams, headers=header)
    print(r.headers.get('content-type'))
    planet_names = r.json()
    ticid = planet_names['tessID']
    tce = planet_names['tessTCE']

    url = dvurl + str(ticid) + '/tces/'
    myparams = {"tce": tce}

    r = requests.get(url=url, params=myparams, headers=header)
    sectorInfo = r.json()
    print("TICID: ", ticid)
    print("TCE: ", tce)

    print("SECTORS:", sectorInfo)

    sectors = [x[:11] for x in sectorInfo["TCE"] if tce in x]


    url = dvurl + str(ticid) + '/table/'
    myparams = {"tce": tce,
                "sector": sectors[0]}

    print("PASS ThiS THROUGH:", sectors[0])
    print("PARAMS:", myparams)

    r = requests.get(url=url, params=myparams, headers=header)
    tce_data = r.json()


    data = p.DataFrame.from_dict(tce_data['data'])

    detrend = data['LC_DETREND']
    model = data['MODEL_INIT']
    time = data['TIME']
    fig = figure()
    ax = fig.gca()
    #ax.plot([1, 2, 3, 4])
    ax.plot(time, detrend, '.', lw=0.4)
    ax.plot(time, model, 'r-', lw=0.6)
    ax.set_xlabel('TIME (BTJD)')
    ax.set_ylabel('Relative Flux')
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/json/<planet_name>')

def json_stuff(planet_name):


    planet_name = planet_name.replace('%20', ' ').replace('+', ' ')

    url = planeturl + "/identifiers/"

    myparams = {"name": planet_name}

    r = requests.get(url=url, params=myparams, headers=header)
    print(r.headers.get('content-type'))
    planet_names = r.json()

    return str(planet_names)

if __name__ == '__main__':
    app.run()
