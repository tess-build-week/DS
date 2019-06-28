#! /usr/bin/env python

from .getter import aqTicReq, getSector, getPlanetProp, pnameGenerator
import pandas as pd


def getStarCsv(starlist, csv_out_name, verbose=1):
    """Gets star properties for list of stars. Outputs
    to specified csv file. Do not include .csv extension"""

    Stars = pd.DataFrame(
        columns=[
            "star_tessid",
            "twomass",
            "gaiaid",
            "sector",
            "magnitude",
            "luminosity",
            "star_mass",
            "star_radius",
            "constellation",
            "disposition",
            "rightascension",
            "declination",
        ]
    )

    i = 0
    for tessid in starlist:
        if tessid not in Stars["star_tessid"].values:
            if verbose == 1:
                print(".", end="")
            elif verbose >= 2:
                print(i, tessid)
            else:
                None
            star = {
                "star_tessid": int(tessid),
                "twomass": aqTicReq(tessid, "TWOMASS"),
                "gaiaid": aqTicReq(tessid, "GAIA"),
                "sector": getSector(tessid, True),
                "magnitude": aqTicReq(tessid, "Tmag"),
                "luminosity": aqTicReq(tessid, "lumclass"),
                "star_mass": aqTicReq(tessid, "mass"),
                "star_radius": aqTicReq(tessid, "rad"),
                "constellation": getPlanetProp(
                    str(f"{tessid:011}") + "-01", "constellation"
                ),
                "disposition": aqTicReq(tessid, "disposition"),
                "rightascension": str(round(float(aqTicReq(tessid, "ra")), 8)),
                "declination": str(round(float(aqTicReq(tessid, "dec")), 8)),
            }
            Stars = Stars.append(star, ignore_index=True)
            i += 1
            if verbose >= 3:
                print(star)
    Stars.to_csv(r"{}.csv".format(csv_out_name))


def getPlanetCsv(tcelist, csv_out, verbose=1):

    """Get planet properties from a list of threshold crossing
    events in format <tessid [11]><-xx>. Outputs csv file
    <csv_out>.csv . Do not put .csv extension in input"""

    Planets = pd.DataFrame(
        columns=[
            "planet_tce",
            "planetid",
            "star_tessid",
            "orbit_period",
            "planet_mass",
            "planet_mass",
            "planet_radius",
        ]
    )

    i = 0
    for tce in tcelist:
        if tce not in Planets["planet_tce"].values:
            if verbose == 1:
                print(".", end="")
            elif verbose >= 2:
                print(i, tce)
            else:
                None
            planet = {
                "planet_tce": tce,
                "planetid": pnameGenerator(tce),
                "star_tessid": int(tce.split("-")[0]),
                "orbit_period": getPlanetProp(tce, "orbital_period"),
                "planet_mass": getPlanetProp(tce, "Mp"),
                "planet_radius": str(getPlanetProp(tce, "Rp"))
                + str(getPlanetProp(tce, "Rp_unit")),
            }
            Planets = Planets.append(planet, ignore_index=True)
            i += 1
            if verbose >= 3:
                print(planet)
    Planets.to_csv(r"{}.csv".format(csv_out))
