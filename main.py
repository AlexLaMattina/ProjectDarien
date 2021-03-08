import dash
import flask
import numpy as np
from collections import defaultdict
from pandas import DataFrame
from plotly.graph_objs import Scattermapbox
from flask import Flask
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import chart_studio.plotly as py
import pandas as pd

py.sign_in('alexlamattina', 'WMl4yDvoKm1xPWk9Wjxx')

mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjaXhzYTB0bHcwOHNoMnFtOWZ3YWdreDB3In0.pjROwb9_CEuyKPE-x0lRUw'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = flask.Flask(__name__)

url = 'https://raw.githubusercontent.com/AlexLaMattina/ProjectDarien/master/BuildingData.csv'
url2 = 'https://raw.githubusercontent.com/AlexLaMattina/ProjectDarien/master/ProjectDarienData.csv'
url3 = 'https://raw.githubusercontent.com/AlexLaMattina/ProjectDarien/master/SocialDistanceVar.csv'
url4 = 'https://raw.githubusercontent.com/AlexLaMattina/ProjectDarien/master/PercentageFall2020.csv'
df = pd.read_csv(url, dtype={"Location": "string", "LON": "float", "LAT": "float"})
pf = pd.read_csv(url2, dtype={"id": "int", "date": "string", "timeofday": "int", "LON": "float", "LAT": "float",
                              "activity 1=not morving, 2=walking, 3=running, 4=biking, 6=skateboarding": "int",
                              "direction 1=n, 2=s, 3=e, 4=w, 5=sw, 6=se, 7=nw, 8=ne": "int",
                              "withmask 0=no, 1=yes": "int",
                              "nomaskimpr 0=no mask or mask but incorrect, 1=mask and correct": "int",
                              "maskreason 1=nose exposed, 2=nose and mouth exposed": "int",
                              "maskother 1=exhalation valve or vent, 2=on forehead, 3=around neck, 4=touched mask, "
                              "5=<2 years of age, 6=in hand, 7=hanging on ear": "int",
                              "socialdist 0=no, 1=yes": "int", "agegroup 1=<18, 2=18-30, 3=31-55, 4=>55": "int",
                              "white 0=not white, 1=white": "int", "sex 1=male, 2=female": "int",
                              "smoking 0= not smoking, 1=smoking": "int",
                              "obese 0=not overweight/obese, 1=overweight/obese": "int",
                              "touchsurface 0=no, 1=yes": "int",
                              "surfacetype 1=trash can, 2=parking meter, 3=door handle, 4=railing, 5=auto, "
                              "6=building, 7=other, 8=bench, 9=phone, 11=tools, 12=table": "int",
                              "Etiquette1 0=no hands to head, 1= hands to head": "int"})
sf = pd.read_csv(url3, dtype={"id": "int",
                              "Masksd 0=Mask Non-Complient and Not Social Distancing; "
                              "1 = Mask Complient and Social Distancing; 9= could not be determined": "int"})
per = pd.read_csv(url4, dtype={"semester 1=fall 2=spring": "float",
                               "studyweek 1=baseline": "float",
                               "activity % moving (walk, run, bike)": "float",
                               "withmask % with a mask": "float",
                               "maskincorrect (% without mask or with mask but worn incorrectly)": "float",
                               "notphysicaldist (% < 6 ft from someone)": "float",
                               "percentnotcomliantsdmask (% non-compliant with mask wearing and physical distancing)": "float",
                               "ageover55": "float",
                               "percentmale": "float",
                               "percentobese": "float",
                               "percentnonwhite": "float", })




fig = go.Figure()
fig = make_subplots(rows=3, cols=3, subplot_titles=("Percent of Total Described Moving",
                                                    "Percent of Total Described With a Mask",
                                                    "Percent of Total Described Wearing a Mask Incorrectly",
                                                    "Percent of Total Described Not Social Distancing<br>"
                                                    "(<6 Feet From Someone)",
                                                    "Percent of Total Described Not Compliant with Regulations",
                                                    "Percent of Total Described Over the Age 55",
                                                    "Percent of Total Described Male",
                                                    "Percent of Total Described Obese",
                                                    "Percent of Total Described Non-white"))

for i in fig['layout']['annotations']:
    i['font'] = dict(size=10)

activityper = []
wearingmaskper = []
incorrectmaskper = []
notsocialdistper = []
notcompliantper = []
ageper = []
malesper = []
obeseper = []
nonwhiteper = []

for i in per.index:
    wearingmaskper.append(per['withmask % with a mask'][i])
    incorrectmaskper.append(per['maskincorrect (% without mask or with mask but worn incorrectly)'][i])
    notcompliantper.append(per['percentnotcomliantsdmask (% non-compliant with mask wearing and physical distancing)'][i])
    activityper.append(per['activity % moving (walk, run, bike)'][i])
    notsocialdistper.append(per['notphysicaldist (% < 6 ft from someone)'][i])
    obeseper.append(per['percentobese'][i])
    malesper.append(per['percentmale'][i])
    nonwhiteper.append(per['percentnonwhite'][i])
    ageper.append(per['ageover55'][i])


dates = ["8/20/2020 & 8/24/2020", "9/03/2020", "9/11/2020", "9/16/2020", "9/22/2020", "9/28/2020"]

fig.append_trace(go.Scatter(
    hovertext="Percent Doing an Activity",
    name="",
    mode='lines+markers',
    x=dates,
    y=activityper, ),
    row=1,
    col=1)

fig.append_trace(go.Scatter(
    hovertext="Percent Wearing Masks",
    name="",
    mode='lines+markers',
    x=dates,
    y=wearingmaskper, ),
    row=1,
    col=2)

fig.append_trace(go.Scatter(
    hovertext="Percent Wearing Masks Incorrectly",
    name="",
    mode='lines+markers',
    x=dates,
    y=incorrectmaskper, ),
    row=1,
    col=3)


fig.append_trace(go.Scatter(
    hovertext="Percent Not Social Distancing",
    name="",
    mode='lines+markers',
    x=dates,
    y=notsocialdistper),
    row=2,
    col=1)

fig.append_trace(go.Scatter(
    hovertext="Percent Non-Compliant",
    name="",
    mode='lines+markers',
    x=dates,
    y=notcompliantper, ),
    row=2,
    col=2)


fig.append_trace(go.Scatter(
    hovertext="Percent Over the Age of 55",
    name="",
    mode='lines+markers',
    x=dates,
    y=ageper),
    row=2,
    col=3)

fig.append_trace(go.Scatter(
    hovertext="Percent Male",
    name="",
    mode='lines+markers',
    x=dates,
    y=malesper),
    row=3,
    col=1)

fig.append_trace(go.Scatter(
    hovertext="Percent Obese",
    name="",
    mode='lines+markers',
    x=dates,
    y=obeseper, ),
    row=3,
    col=2)

fig.append_trace(go.Scatter(
    hovertext="Percent NonWhite",
    name="",
    mode='lines+markers',
    x=dates,
    y=nonwhiteper),
    row=3,
    col=3)

###########################################################################

# SPLIT UP DATA BY DATE, MASKS, and SOCIAL DIST
date1masklon = []
date1masklat = []
date1id = []
date1nomasklon = []
date1nomasklat = []
date1unknownlon = []
date1unknownlat = []

date2masklon = []
date2masklat = []
date2id = []
date2nomasklon = []
date2nomasklat = []
date2unknownlon = []
date2unknownlat = []

date3masklon = []
date3masklat = []
date3id = []
date3nomasklon = []
date3nomasklat = []
date3unknownlon = []
date3unknownlat = []

date4masklon = []
date4masklat = []
date4id = []
date4nomasklon = []
date4nomasklat = []
date4unknownlon = []
date4unknownlat = []

date5masklon = []
date5masklat = []
date5id = []
date5nomasklon = []
date5nomasklat = []
date5unknownlon = []
date5unknownlat = []

date6masklon = []
date6masklat = []
date6id = []
date6nomasklon = []
date6nomasklat = []
date6unknownlon = []
date6unknownlat = []

date7masklon = []
date7masklat = []
date7id = []
date7nomasklon = []
date7nomasklat = []
date7unknownlon = []
date7unknownlat = []

masklon = []
masklat = []
ids = []
nomasklon = []
nomasklat = []
unknownlon = []
unknownlat = []

for i in pf.index:
    ids.append(pf['id'][i])
    for j in sf.index:
        if i == j:
            if sf[
                "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; 9= "
                "could not be determined"][i] == 1:
                masklon.append(pf['LON'][i])
                masklat.append(pf['LAT'][i])
            elif sf[
                "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; 9= "
                "could not be determined"][
                i] == 0:
                nomasklon.append(pf['LON'][i])
                nomasklat.append(pf['LAT'][i])
            else:
                unknownlon.append(pf['LON'][i])
                unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '8/20/2020':
        date1id.append(pf['id'][i])
        for j in sf.index:
            if i == j:
                if sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; " \
                    "9= could not be determined"][
                    i] == 1:
                    date1masklon.append(pf['LON'][i])
                    date1masklat.append(pf['LAT'][i])
                elif sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; " \
                    "9= could not be determined"][
                    i] == 0:
                    date1nomasklon.append(pf['LON'][i])
                    date1nomasklat.append(pf['LAT'][i])
                else:
                    date1unknownlon.append(pf['LON'][i])
                    date1unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '8/24/2020':
        date1id.append(pf['id'][i])
        for j in sf.index:
            if i == j:
                if sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; " \
                    "9= could not be determined"][
                    i] == 1:
                    date1masklon.append(pf['LON'][i])
                    date1masklat.append(pf['LAT'][i])
                elif sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; " \
                    "9= could not be determined"][
                    i] == 0:
                    date1nomasklon.append(pf['LON'][i])
                    date1nomasklat.append(pf['LAT'][i])
                else:
                    date1unknownlon.append(pf['LON'][i])
                    date1unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '9/03/2020':
        date3id.append(pf['id'][i])
        for j in sf.index:
            if i == j:
                if sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; " \
                    "9= could not be determined"][
                    i] == 1:
                    date3masklon.append(pf['LON'][i])
                    date3masklat.append(pf['LAT'][i])
                elif sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; " \
                    "9= could not be determined"][
                    i] == 0:
                    date3nomasklon.append(pf['LON'][i])
                    date3nomasklat.append(pf['LAT'][i])
                else:
                    date3unknownlon.append(pf['LON'][i])
                    date3unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '9/11/2020':
        date4id.append(pf['id'][i])
        for j in sf.index:
            if i == j:
                if sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; " \
                    "9= could not be determined"][
                    i] == 1:
                    date4masklon.append(pf['LON'][i])
                    date4masklat.append(pf['LAT'][i])
                elif sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; " \
                    "9= could not be determined"][
                    i] == 0:
                    date4nomasklon.append(pf['LON'][i])
                    date4nomasklat.append(pf['LAT'][i])
                else:
                    date4unknownlon.append(pf['LON'][i])
                    date4unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '9/16/2020':
        date5id.append(pf['id'][i])
        for j in sf.index:
            if i == j:
                if sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; " \
                    "9= could not be determined"][
                    i] == 1:
                    date5masklon.append(pf['LON'][i])
                    date5masklat.append(pf['LAT'][i])
                elif sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; " \
                    "9= could not be determined"][
                    i] == 0:
                    date5nomasklon.append(pf['LON'][i])
                    date5nomasklat.append(pf['LAT'][i])
                else:
                    date5unknownlon.append(pf['LON'][i])
                    date5unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '9/22/2020':
        date6id.append(pf['id'][i])
        for j in sf.index:
            if i == j:
                if sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; "
                    "9= could not be determined"][i] == 1:
                    date6masklon.append(pf['LON'][i])
                    date6masklat.append(pf['LAT'][i])
                elif sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing; "
                    "9= could not be determined"][i] == 0:
                    date6nomasklon.append(pf['LON'][i])
                    date6nomasklat.append(pf['LAT'][i])
                else:
                    date6unknownlon.append(pf['LON'][i])
                    date6unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '9/28/2020':
        date7id.append(pf['id'][i])
        for j in sf.index:
            if i == j:
                if sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing;"
                    " 9= could not be determined"][i] == 1:
                    date7masklon.append(pf['LON'][i])
                    date7masklat.append(pf['LAT'][i])
                elif sf[
                    "Masksd 0=Mask Non-Complient and Not Social Distancing; 1 = Mask Complient and Social Distancing;"
                    " 9= could not be determined"][i] == 0:
                    date7nomasklon.append(pf['LON'][i])
                    date7nomasklat.append(pf['LAT'][i])
                else:
                    date7unknownlon.append(pf['LON'][i])
                    date7unknownlat.append(pf['LAT'][i])

trace1 = Scattermapbox(
    name="Buildings",
    mode="markers",
    lon=df['LAT'],
    lat=df['LON'],
    text=df['Location'],

    hoverinfo="lon+lat+text",
    marker=dict(
        symbol='square-stroked',
        size=12,
        color='black',
        opacity=1
    ),
    legendgroup="Buildings",

)


def maketrace(name, lats, lons, dataframe, color, shape, group, showlegend, sd):
    return Scattermapbox(

        name=name,
        mode="markers",

        lon=lats,
        lat=lons,
        text="ID: " + dataframe['ID'].astype(str) + "<br>Mask/Social Distance Compliance: " + sd,
        hoverinfo="lon+lat+text",
        # SPECS
        marker=dict(
            size=12,
            color=color,
            symbol=shape,
            opacity=0.8,
        ),

        legendgroup=group,
        showlegend=showlegend,

    )


def makeborder(name, lats, lons, dataframe, color, shape, group, showlegend, sd, mask):
    return Scattermapbox(

        name=name,
        mode="markers",

        lon=lats,
        lat=lons,
        text="ID: " + dataframe['ID'].astype(
            str) + "<br>Social Distance Compliance: " + sd + "<br>Mask Compliance: " + mask,
        hoverinfo="lon+lat+text",
        # SPECS
        marker=dict(
            size=15,
            color=color,
            symbol=shape,
            opacity=0.8,
        ),

        legendgroup=group,
        showlegend=showlegend,

    )


def makeborder2(name, lats, lons, dataframe, color, shape, group, showlegend, sd, mask, date):
    return Scattermapbox(

        name=name,
        mode="markers",

        lon=lats,
        lat=lons,
        text="ID: " + dataframe['ID'].astype(
            str) + "<br>Date: " + date['date'].astype(
            str) + "<br>Social Distance Compliance: " + sd + "<br>Mask Compliance: " + mask,
        hoverinfo="lon+lat+text",
        # SPECS
        marker=dict(
            size=10,
            color=color,
            symbol=shape,
            opacity=0.8,
        ),

        legendgroup=group,
        showlegend=showlegend,

    )


def makeborder3(name, lats, lons, color, shape, group, showlegend):
    return Scattermapbox(

        name=name,
        mode="markers",

        lon=lats,
        lat=lons,

        # SPECS
        marker=dict(
            size=15,
            color=color,
            symbol=shape,
            opacity=0.8,
        ),

        legendgroup=group,
        showlegend=showlegend,

    )


date1df = DataFrame(date1id, columns=['ID'])
trace2 = maketrace("8/20/2020 & 8/24/2020 ", date1masklat, date1masklon, date1df, "blue", "circle", "Mask Data", True,
                   "YES")
trace3 = maketrace("8/20/2020 & 8/24/2020", date1nomasklat, date1nomasklon, date1df, "red", "circle", "No Mask Data",
                   True, "NO")
trace4 = maketrace("8/20/2020 & 8/24/2020", date1unknownlat, date1unknownlon, date1df, "grey", "circle",
                   "Unknown data", True, "UNKNOWN")

date3df = DataFrame(date3id, columns=['ID'])
trace8 = maketrace("9/03/2020", date3masklat, date3masklon, date3df, "blue", "circle", "Mask Data", True, "YES")
trace9 = maketrace("9/03/2020", date3nomasklat, date3nomasklon, date3df, "red", "circle", "No Mask Data", True, "NO")
trace10 = maketrace("9/03/2020", date3unknownlat, date3unknownlon, date3df, "grey", "circle",
                    "Unknown data", True, "UNKNOWN")

date4df = DataFrame(date4id, columns=['ID'])
trace11 = maketrace("9/11/2020", date4masklat, date4masklon, date4df, "blue", "circle", "Mask Data", True, "YES")
trace12 = maketrace("9/11/2020", date4nomasklat, date4nomasklon, date4df, "red", "circle", "No Mask Data", True, "NO")
trace13 = maketrace("9/11/2020", date4unknownlat, date4unknownlon, date4df, "grey", "circle",
                    "Unknown data", True, "UNKNOWN")

date5df = DataFrame(date5id, columns=['ID'])
trace14 = maketrace("9/16/2020", date5masklat, date5masklon, date5df, "blue", "circle", "Mask Data", True, "YES")
trace15 = maketrace("9/16/2020", date5nomasklat, date5nomasklon, date5df, "red", "circle", "No Mask Data", True, "NO")
trace16 = maketrace("9/16/2020", date5unknownlat, date5unknownlon, date5df, "grey", "circle",
                    "Unknown data", True, "UNKNOWN")

date6df = DataFrame(date6id, columns=['ID'])
trace17 = maketrace("9/22/2020", date6masklat, date6masklon, date6df, "blue", "circle", "Mask Data", True, "YES")
trace18 = maketrace("9/22/2020", date6nomasklat, date6nomasklon, date6df, "red", "circle", "No Mask Data", True, "NO")
trace19 = maketrace("9/22/2020", date6unknownlat, date6unknownlon, date6df, "grey", "circle",
                    "Unknown data", True, "UNKNOWN")

date7df = DataFrame(date7id, columns=['ID'])
trace20 = maketrace("9/28/2020", date7masklat, date7masklon, date7df, "blue", "circle", "Mask Data", True, "YES")
trace21 = maketrace("9/28/2020", date7nomasklat, date7nomasklon, date7df, "red", "circle", "No Mask Data", True, "NO")

iddf = DataFrame(ids, columns=['ID'])
trace22 = maketrace("Mask Compliant and<br>Social Distancing", masklat, masklon, iddf, "blue", "circle", "Mask Data",
                    True,
                    "YES")
trace23 = maketrace("Mask Non-compliant and<br>not Social Distancing", nomasklat, nomasklon, iddf, "red", "circle",
                    "No Mask Data", True, "NO")
trace24 = maketrace("Mask Compliance and<br>Social Distancing Unknown", unknownlat, unknownlon, iddf, "grey", "circle",
                    "Unknown data", True, "UNKNOWN")

####################SPLIT UP DATA INTO FOUR CATEGORIES############################
maskandsdlon = []
maskandsdlat = []
maskandnsdlon = []
maskandnsdlat = []
socdistandnmasklon = []
socdistandnmasklat = []
nsocdistandnmasklon = []
nsocdistandnmasklat = []
allids = []
maskandsddate = []
maskandnsddate = []
socdistandnmaskdate = []
nsocdistandnmaskdate = []

for i in pf.index:
    allids.append(pf['id'][i])
    if pf["withmask 0=no, 1=yes"][i] == 1:
        if pf["socialdist 0=no, 1=yes"][i] == 1:
            maskandsdlat.append(pf['LAT'][i])
            maskandsdlon.append(pf['LON'][i])
            maskandsddate.append(pf['date'][i])
        elif pf["socialdist 0=no, 1=yes"][i] == 0:
            maskandnsdlat.append(pf['LAT'][i])
            maskandnsdlon.append(pf['LON'][i])
            maskandnsddate.append(pf['date'][i])
    if pf["withmask 0=no, 1=yes"][i] == 0:
        if pf["socialdist 0=no, 1=yes"][i] == 1:
            socdistandnmasklat.append(pf['LAT'][i])
            socdistandnmasklon.append(pf['LON'][i])
            socdistandnmaskdate.append(pf['date'][i])
        elif pf["socialdist 0=no, 1=yes"][i] == 0:
            nsocdistandnmasklat.append(pf['LAT'][i])
            nsocdistandnmasklon.append(pf['LON'][i])
            nsocdistandnmaskdate.append(pf['date'][i])

alliddf = DataFrame(allids, columns=['ID'])
mandsd = DataFrame(maskandsddate, columns=['date'])
mandnsd = DataFrame(maskandnsddate, columns=['date'])
sdandnm = DataFrame(socdistandnmaskdate, columns=['date'])
nsdandnm = DataFrame(nsocdistandnmaskdate, columns=['date'])

trace25 = makeborder("none", maskandsdlat, maskandsdlon, alliddf, "blue", "circle", "Nan", False, "YES", "YES")
trace26 = makeborder("none", socdistandnmasklat, socdistandnmasklon, alliddf, "blue", "circle", "Nan", False, "YES",
                     "NO")
trace27 = makeborder("none", maskandnsdlat, maskandnsdlon, alliddf, "red", "circle", "Nan", False, "NO", "YES")
trace28 = makeborder("none", nsocdistandnmasklat, nsocdistandnmasklon, alliddf, "red", "circle", "Nan", False, "NO",
                     "NO")

trace29 = makeborder2("Wearing Mask and Social Distancing", maskandsdlat, maskandsdlon, alliddf, "blue", "circle",
                      "Nan",
                      False, "YES", "YES", mandsd)

trace30 = makeborder2("Not Wearing Mask and Social Distancing", socdistandnmasklat, socdistandnmasklon, alliddf, "red",
                      "circle", "Nan", False, "YES", "NO", sdandnm)

trace31 = makeborder2("Wearing Mask and Not Social Distancing", maskandnsdlat, maskandnsdlon, alliddf, "blue", "circle",
                      "Nan", False, "NO", "YES", mandnsd)

trace32 = makeborder2("Not Wearing Mask and Not Social Distancing", nsocdistandnmasklat, nsocdistandnmasklon, alliddf,
                      "red", "circle", "Nan", False, "NO", "NO", nsdandnm)

empty = []
trace33 = makeborder3("Wearing a Mask", maskandsdlon, maskandsdlat, "blue", "circle", "Nan", True)

trace34 = makeborder3("Not Wearing a Mask", socdistandnmasklon, socdistandnmasklat, "red", "circle", "Nan", True)

trace35 = makeborder3("Social Distancing", maskandnsdlon, maskandnsdlat, "blue", "circle-open", "Nan", True)

trace36 = makeborder3("Not Social Distancing", nsocdistandnmasklon, nsocdistandnmasklat, "red", "circle-open", "Nan",
                      True)

updatemenus = list([
    dict(active=0,
         showactive=True,
         buttons=list([
             dict(label="Overall<br>Compliance",
                  method="restyle",
                  args=[{"visible": [False, True, True, True, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False]}]),
             # hide trace2
             dict(label="Mask and<br>Social Distance<br>Options",
                  method="restyle",
                  args=[{"visible": [False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, True, True, True, True, True, True, True, True, True, True, True, True]}]),

         ]),
         x=1,
         )])

layout = dict(
    title="COVID-19 Modeling Data",

    autosize=True,
    height=875,
    width=1500,
    margin=dict(l=80, r=80, t=100, b=80),
    annotations=[
        go.layout.Annotation(
            text='Use the maps dropdown menu to switch to see each Data Points Mask and Social Distancing '
                 'Characteristics<br>'
                 'OR to see compliance with UD regulations:'
                 'Non-Compliant: Mask incorrect/No mask plus not social distancing<br>'
                 'Compliant: Social Distancing (regardless of having a mask)'
                 'OR not social distancing with a mask worn correctly ',
            align='left',
            bordercolor='black',
            x=1.15,
            y=1.1,
            showarrow=False,
        ),
        go.layout.Annotation(
            text='Use the slider to see the data split up by each date',
            align='left',
            x=.15,
            y=-.15,
            bordercolor='black'

        ),
        go.layout.Annotation(
            text='Click<a href=\"https://www.weather.gov/\"> here </a>to Check the Weather on Each Date'
            '<br>Hover Over Points for More Information',
            align='left',
            x=.0,
            y=1.08,
            bordercolor='black',
            showarrow=False,

        )
    ],

    hovermode="closest",
    mapbox=dict(

        accesstoken=mapbox_access_token,
        center=dict(
            lat=39.68,
            lon=-75.75
        ),

        pitch=0,
        zoom=13.5,

    ),
    updatemenus=updatemenus,
)

fig.update_layout(
    autosize=True,
    margin=dict(
        t=50,
        l=100,
        b=50,
        r=100,
    ),
    showlegend=False,
    hovermode="x unified",

)
data = [trace1, trace22, trace23, trace24, trace2, trace3, trace4, trace8, trace9,
        trace10, trace11, trace12, trace13, trace14, trace15, trace16, trace17, trace18, trace19, trace20, trace21,
        trace25, trace26, trace27, trace28, trace29, trace30, trace31, trace32, trace33, trace34, trace35, trace36]
labels = ["Buildings", "All Data", "", "",
          "8/20/2020 & 8/24/2020<br>Time Stamps: <br>12:00:34 PM - 12:01:29 PM<br>12:01:29 PM - 12:10:35 PM",
          "", "", "9/03/2020<br>Time Stamp:<br>11:22:15 AM - 12:18:59 PM", "", "",
          "9/11/2020<br>Time Stamp:<br>11:06:49 AM - 12:13:04 PM",
          "", "", "9/16/2020<br>Time Stamp:<br>11:15:17 AM - 12:50:24 PM", "", "",
          "9/22/2020<br>Time Stamp:<br>11:12:42 AM - 12:14:38 PM", "", "",
          "9/28/2020<br>Time Stamp:<br>11:31:30 AM - 12:31:33 PM", "", "", ]

figure = go.Figure(data=data, layout=layout)
steps = []
num_steps = 21

for i in range(1, num_steps, 3):
    step = dict(
        label=labels[i],
        method='restyle',
        args=['visible', ['legendonly'] * len(figure.data)],
    )

    if i < num_steps:
        step['args'][1][i] = True

    if i + 1 < num_steps:
        step['args'][1][i + 1] = True

    if i + 2 < num_steps:
        step['args'][1][i + 2] = True

    step['args'][1][0] = True
    steps.append(step)

sliders = [dict(
    steps=steps,
    currentvalue=dict(
        font=dict(size=15),
        prefix="Date : ",
        xanchor="right",
        visible=True,
    ), )]

steps = []

num_steps = 6
for i in range(num_steps):
    step = dict(
        label=dates[i],
        method='restyle',
        args=['visible', [False] * len(fig.data)],
    )
    step['args'][1][i] = True

    steps.append(step)

slidersfig = [dict(steps=steps,
                   currentvalue=dict(
                       font=dict(size=15),
                       prefix="Date : ",
                       xanchor="right",
                       visible=True,

                   ), y=-.15, )]

fig.update_yaxes(range=[0, 100])


figure.layout.sliders = sliders

server = Flask(__name__)

app = dash.Dash(
    __name__,
    server=server,
)

app.layout = html.Div(children=[
    html.Div([
        dcc.Graph(
            figure=figure,
            style={
                'height': 1015,
            },
        ),

    ]),

    html.Div([
        dcc.Graph(
            figure=fig,
            style={
                'height': 950,
            },
        ),
    ]),

])

if __name__ == '__main__':
    app.run_server(debug=True)
