#! /usr/bin/env python

import numpy as np
import requests
import pandas as pd
from IPython.display import display, HTML
import sys
import os
import time
import re
import json
from urllib.parse import quote as urlencode
from urllib.request import urlretrieve
import http.client as httpcli
from astropy.table import Table
from .query import mastQuery

planeturl = "https://exo.mast.stsci.edu/api/v0.1/exoplanets/"
dvurl = "https://exo.mast.stsci.edu/api/v0.1/dvdata/tess/"
header_secinfo = {}
header = {}


def aqTicReq(tessid, column):

    """Astroquery request from TESS candidates database"""

    requestTic = {
        "service": "Mast.Catalogs.Filtered.Tic",
        "format": "json",
        "params": {
            "columns": "c.{}".format(str(column)),  # Column name to get
            "filters": [
                {
                    "paramName": "ID",  # Filter by ID (tessid/ticid)
                    "values": [str(tessid)],
                }
            ],
        },
    }

    headers, outString = mastQuery(requestTic)
    outData = json.loads(outString)  # This isn't entirely necessary here
    return outData["data"][0][str(column)]


# Planet name assembler


def nameResolver(ticid):

    """Returns all name info of star. Can
    match to names from most major stellar
    catalogues"""

    request = {
        "service": "Mast.Name.Lookup",
        "params": {"input": str(ticid), "format": "json"},
    }

    headers, outString = mastQuery(request)

    outData = json.loads(outString)

    return outData


def pnameGenerator(tceid):

    """Planet name generator using the standard NASA
    exoplanet archive format. Used to generate likely
    names for as yet unnamed planets"""

    tessid, pl_number = tceid.split("-")
    tessid = str(int(tessid))
    pl_dict = {
        "01": "a",
        "02": "b",
        "03": "c",
        "04": "d",
        "05": "e",
        "06": "f",
        "07": "g",
        "08": "h",
        "09": "i",
        "10": "j",
        "11": "k",
        "12": "l",
    }
    star_name = nameResolver(tessid)["resolvedCoordinate"][0]["canonicalName"]
    return str(star_name + "-" + pl_dict[pl_number])


# exoMAST info getters: sector getter


def getSector(tessid, get1=True, tce="TCE_1"):

    """Get TESS sector information for threshold crossing event.
    Used to get light curves from exoMAST archive"""

    name = "TIC " + str(tessid)
    url = planeturl + "/identifiers/"
    params = {"name": name}
    r = requests.get(url=url, params=params, headers=header_secinfo)
    planet_names = r.json()
    # tce = planet_names['tessTCE']
    url = dvurl + str(tessid) + "/tces/"
    myparams = {"tce": tce}

    r = requests.get(url=url, params=myparams, headers=header_secinfo)
    sectorInfo = r.json()

    sectors = [x[:11] for x in sectorInfo["TCE"] if tce in x][0][:5]
    sector_split = [x.split(":") for x in sectorInfo["TCE"] if tce in x][0][:5]
    if get1 == True:
        return sectors
    else:
        return sector_split


def tceConverter(tce):

    """Convert <-xx> style TCE designation to <TCE_x> format"""

    tce_dict = {
        "01": "TCE_1",
        "02": "TCE_2",
        "03": "TCE_3",
        "04": "TCE_4",
        "05": "TCE_5",
        "06": "TCE_6",
        "07": "TCE_7",
        "08": "TCE_8",
        "09": "TCE_9",
        "10": "TCE_10",
        "11": "TCE_11",
        "12": "TCE_12",
    }
    return tce_dict[tce]


def getPlanetProp(tceid, prop_name):

    """Get single planet property from exoMAST.
    Takes tceid in <ticid>-<tce> format like: 
    00101365484-01. 11 digit ticid, <-xx> tce
    number"""

    tceid = str(tceid)
    tessid, pl_number = tceid.split("-")
    tce = tceConverter(pl_number)

    tessid = str(int(tessid))

    star_name = "TIC " + str(tessid)

    sectors = getSector(tessid, False, tce)
    full_pname = star_name + " (" + sectors[0].upper() + ") " + tce

    url = planeturl + str(full_pname) + "/properties/"
    r = requests.get(url=url, headers=header)
    planet_prop = r.json()

    if planet_prop[0][prop_name] == None:
        return_prop = 0
    else:
        return_prop = planet_prop[0][prop_name]
    return return_prop
