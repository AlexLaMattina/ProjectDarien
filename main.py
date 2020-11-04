import dash
import flask
import numpy as np
from collections import defaultdict
from plotly.graph_objs import Scattermapbox
from flask import Flask
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import chart_studio.plotly as py
py.sign_in('alexlamattina', 'WMl4yDvoKm1xPWk9Wjxx')
import pandas as pd

mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjaXhzYTB0bHcwOHNoMnFtOWZ3YWdreDB3In0.pjROwb9_CEuyKPE-x0lRUw'
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = flask.Flask(__name__)

url = 'https://raw.githubusercontent.com/AlexLaMattina/COVID-19-Modeling/main/COVID19%20Building%20Data.csv'
url2 = 'https://raw.githubusercontent.com/AlexLaMattina/COVID-19-Modeling/main/COVID-19%20Data.csv'
url3 = 'https://raw.githubusercontent.com/AlexLaMattina/COVID-19-Modeling/main/COVID%20People%20Activity%20Data.csv'
df = pd.read_csv(url, dtype={"Location": "string", "LON": "float", "LAT": "float"})
pf = pd.read_csv(url2, dtype={"id": "int", "date": "string", "timeofday": "int", "LON": "float", "LAT": "float",
                              "activity 1=not morving, 2=walking, 3=running, 4=biking, 6=skateboarding": "int",
                              "direction 1=n, 2=s, 3=e, 4=w, 5=sw, 6=se, 7=nw, 8=ne": "int",
                              "withmask 0=no, 1=yes": "int",
                              "nomaskimpr 0=no mask or mask but incorrect, 1=mask and correct": "int",
                              "maskreason 1=nose exposed, 2=nose and mouth exposed": "int",
                              "maskother 1=exhalation valve or vent, 2=on forehead, 3=around neck, 4=touched mask, 5=<2 years of age, 6=in hand, 7=hanging on ear": "int",
                              "socialdist 0=no, 1=yes": "int", "agegroup 1=<18, 2=18-30, 3=31-55, 4=>55": "int",
                              "white 0=not white, 1=white": "int", "sex 1=male, 2=female": "int",
                              "smoking 0= not smoking, 1=smoking": "int",
                              "obese 0=not overweight/obese, 1=overweight/obese": "int",
                              "touchsurface 0=no, 1=yes": "int",
                              "surfacetype 1=trash can, 2=parking meter, 3=door handle, 4=railing, 5=auto, 6=building, 7=other, 8=bench, 9=phone, 11=tools, 12=table": "int",
                              "Etiquette1 0=no hands to head, 1= hands to head": "int"})
af = pd.read_csv(url3, dtype={"date": "string",
                              "activity 1=not morving, 2=walking, 3=running, 4=biking, 6=skateboarding": "int"})

dates = pf["date"].unique()
dates = list(sorted(dates.astype(str)))


activities = pf["activity 1=not morving, 2=walking, 3=running, 4=biking, 6=skateboarding"].unique()
activities = list(activities.astype(int))

afdate = pf["date"]
afact = pf["activity 1=not morving, 2=walking, 3=running, 4=biking, 6=skateboarding"]
activitieslist = list(zip(afdate, afact))
activitieslist.sort()

maskvals = pf["withmask 0=no, 1=yes"]
maskvallist = list(zip(afdate, maskvals))

correctmaskvals =pf["nomaskimpr 0=no mask or mask but incorrect, 1=mask and correct"]
correctmaskvalslist = list(zip(afdate, correctmaskvals))

noseandmouthvals =pf["maskreason 1=nose exposed, 2=nose and mouth exposed"]
noseandmouthvalslist = list(zip(afdate,noseandmouthvals))

socialdistvals = pf["socialdist 0=no, 1=yes"]
socialdistvalslist = list(zip(afdate,socialdistvals))

agegroupvals=pf["agegroup 1=<18, 2=18-30, 3=31-55, 4=>55"]
agegroupvalslist=list(zip(afdate,agegroupvals))

gendervals=pf["sex 1=male, 2=female"]
gendervalslist=list(zip(afdate, gendervals))

smoking = pf["smoking 0= not smoking, 1=smoking"]
smoking = list(smoking.astype(int))

obese = pf["obese 0=not overweight/obese, 1=overweight/obese"]
obese = list(obese.astype(int))

touchsurface = pf["touchsurface 0=no, 1=yes"]
touchsurface = list(touchsurface.astype(int))

etiquette = pf["Etiquette1 0=no hands to head, 1= hands to head"]
etiquette = list(etiquette.astype(int))

# Still need to add mask other, gender, surface type, fix mouth exposed, and direction?

fig = go.Figure()
fig = make_subplots(rows=2, cols=5, subplot_titles=("Mask Wearing", "Correct Mask Wearing",
                                                    "Exposed Noses and Mouths",
                                                    "Number of Different Activities",
                                                    "Number of People Touching Surfaces",
                                                    "Number of People Social Distancing","Number of People Obese",
                                                    "Number of Different Genders",
                                                    #"Number of People With Etiquette",
                                                    "Number of People Smoking",
                                                    "Number of Different Age Groups"))


for i in fig['layout']['annotations']:
    i['font'] = dict(size=10)



pf["smoking 0= not smoking, 1=smoking"].replace(9, np.NaN, inplace=True)
pf["smoking 0= not smoking, 1=smoking"].replace(0, np.NaN, inplace=True)

pf["obese 0=not overweight/obese, 1=overweight/obese"].replace(9, np.NaN, inplace=True)
pf["obese 0=not overweight/obese, 1=overweight/obese"].replace(0, np.NaN, inplace=True)

pf["touchsurface 0=no, 1=yes"].replace(9, np.NaN, inplace=True)
pf["touchsurface 0=no, 1=yes"].replace(0, np.NaN, inplace=True)

pf["Etiquette1 0=no hands to head, 1= hands to head"].replace(9, np.NaN, inplace=True)
pf["Etiquette1 0=no hands to head, 1= hands to head"].replace(0, np.NaN, inplace=True)



numofsmoking = pf.groupby("date").count()["smoking 0= not smoking, 1=smoking"]

numofobese = pf.groupby("date").count()["obese 0=not overweight/obese, 1=overweight/obese"]

numoftouchsurface = pf.groupby("date").count()["touchsurface 0=no, 1=yes"]

numofetiquette = pf.groupby("date").count()["Etiquette1 0=no hands to head, 1= hands to head"]



numwearingmask=[]
numnotwearingmask=[]


#MASK WEARING TREND
numofmasks=defaultdict(list)

for d, a in maskvallist:
   numofmasks[d].append(a)

numwithmasklist=[]
for d, a in numofmasks.items():
  for i in a:
      if i==1:
          numwearingmask.append(i)
  numwithmasklist.append((numwearingmask.count(1)))
  numwearingmask=[]

withmasklist=[]
withmasklist=pd.Series(numwithmasklist, index=dates)
fig.append_trace(go.Scatter(
    hovertext="People With Masks",
    name="",
    mode='lines+markers',
    x=dates,
    y=withmasklist, ),
    row=1,
    col=1)



#NO MASK WEARING TREND


numwithnomasklist=[]
for d, a in numofmasks.items():
  for i in a:
      if i==0:
          numnotwearingmask.append(i)
  numwithnomasklist.append((numnotwearingmask.count(0)))
  numnotwearingmask=[]

withnomasklist=[]
withnomasklist=pd.Series(numwithnomasklist, index=dates)

fig.append_trace(go.Scatter(
    hovertext="People Without Masks",
    name="",
    mode='lines+markers',
    x=dates,
    y=withnomasklist, ),
    row=1,
    col=1)


numcorrectmask=[]
numincorrectmask=[]
#CORRECT WEARING TREND
numofcorrect=defaultdict(list)

for d, a in correctmaskvalslist:
   numofcorrect[d].append(a)

numcorrectmasklist=[]
for d, a in numofcorrect.items():
  for i in a:
      if i==1:
          numcorrectmask.append(i)
  numcorrectmasklist.append((numcorrectmask.count(1)))
  numcorrectmask=[]

correctmasklist=[]
correctmasklist=pd.Series(numcorrectmasklist, index=dates)

fig.append_trace(go.Scatter(
    hovertext="People Wearing Masks Correctly",
    name="",

    mode='lines+markers',
    x=dates,
    y=correctmasklist, ),
    row=1,
    col=2)
#CHANGE ROW AND COL

#INCORRECT WEARING TREND
numincorrectmasklist=[]
for d, a in numofcorrect.items():
  for i in a:
      if i==0:
          numincorrectmask.append(i)
  numincorrectmasklist.append((numincorrectmask.count(0)))
  numincorrectmask=[]

incorrectmasklist=[]
incorrectmasklist=pd.Series(numincorrectmasklist, index=dates)

fig.append_trace(go.Scatter(
    hovertext="People Wearing Masks Inorrectly",
    name="",
    mode='lines+markers',
    x=dates,
    y=incorrectmasklist, ),
    row=1,
    col=2)
#CHANGE ROW AND COL


numexposednoses=[]
numexposedmouth=[]
#Num of exposed noses TREND
numofexposednose=defaultdict(list)

for d, a in noseandmouthvalslist:
   numofexposednose[d].append(a)

numexposednoselist=[]
for d, a in numofexposednose.items():
  for i in a:
      if i==1:
          numexposednoses.append(i)
  numexposednoselist.append(numexposednoses.count(1))
  numexposednoses=[]

exposednoselist=[]
exposednoselist=pd.Series(numexposednoselist, index=dates)
fig.append_trace(go.Scatter(
    hovertext="Exposed Noses",
    name="",
    mode='lines+markers',
    x=dates,
    y=exposednoselist, ),
    row=1,
    col=3)


#Num of exposed noses and mouths TREND

numexposednoseandmouthlist=[]
for d, a in numofexposednose.items():
  for i in a:
      if i==2:
          numexposedmouth.append(i)
  numexposednoseandmouthlist.append(numexposedmouth.count(2))
  numexposedmouth=[]

exposedmouthlist=[]
exposedmouthlist=pd.Series(numexposednoseandmouthlist, index=dates)

fig.append_trace(go.Scatter(
    hovertext="Exposed Nose and Mouths",
    name="",
    mode='lines+markers',
    x=dates,
    y=exposedmouthlist, ),
    row=1,
    col=3)


numsocialdistance=[]
numnotsocialdistance=[]
#Num of Social distancing trend

numsocialdist=defaultdict(list)

for d, a in socialdistvalslist:
   numsocialdist[d].append(a)

numsocialdistlist=[]
for d, a in numsocialdist.items():
  for i in a:
      if i==1:
          numsocialdistance.append(i)
  numsocialdistlist.append((numsocialdistance.count(1)))
  numsocialdistance=[]

socialdistancelist=[]
socialdistancelist=pd.Series(numsocialdistlist, index=dates)


fig.append_trace(go.Scatter(
    hovertext="People Social Distancing",
    name="",
    mode='lines+markers',
    x=dates,
    y=socialdistancelist),
    row=2,
    col=1)
#Num Not Social distancing trend



numnotsocialdistlist=[]
for d, a in numsocialdist.items():
  for i in a:
      if i==0:
          numnotsocialdistance.append(i)
  numnotsocialdistlist.append((numnotsocialdistance.count(0)))
  numnotsocialdistance=[]

notsocialdistancelist=[]
notsocialdistancelist=pd.Series(numnotsocialdistlist, index=dates)


fig.append_trace(go.Scatter(
    hovertext="People Not Social Distancing",
    name="",
    mode='lines+markers',
    x=dates,
    y=notsocialdistancelist),
    row=2,
    col=1)

fig.append_trace(go.Scatter(
    hovertext="People Smoking",
    name="",
    mode='lines+markers',
    x=dates,
    y=numofsmoking),
    row=2,
    col=4)

fig.append_trace(go.Scatter(
    hovertext="People Who Are Obese",
    name="",
    mode='lines+markers',
    x=dates,
    y=numofobese),
    row=2,
    col=2)

fig.append_trace(go.Scatter(
    hovertext="People Touching Surfaces",
    name="",
    mode='lines+markers',
    x=dates,
    y=numoftouchsurface),
    row=1,
    col=5)



numofgender=defaultdict(list)


#Number of male TREND
for d, a in gendervalslist:
   numofgender[d].append(a)

nummalelist=[]
nummale=[]
for d, a in numofgender.items():
  for i in a:
      if i==1:
          nummale.append(i)
  nummalelist.append((nummale.count(1)))
  nummale=[]

numofmalelist=[]
numofmalelist=pd.Series(nummalelist, index=dates)

fig.append_trace(go.Scatter(
    hovertext="Males",
    name="", #"Number of People With Etiquette",
    mode='lines+markers',
    x=dates,
    y=numofmalelist),#numofetiquette),
    row=2,
    col=3)
numfemalelist=[]
numfemale=[]
for d, a in numofgender.items():
  for i in a:
      if i==2:
          numfemale.append(i)
  numfemalelist.append((numfemale.count(2)))
  numfemale=[]

numoffemalelist=[]
numoffemalelist=pd.Series(numfemalelist, index=dates)

fig.append_trace(go.Scatter(
    hovertext="Females",
    name="",#"Number of People With Etiquette",
    mode='lines+markers',
    x=dates,
    y=numoffemalelist),#numofetiquette),
    row=2,
    col=3)



numnotmoving=[]
numwalking=[]
numrunning=[]
numbiking=[]
numskate=[]
numofactivities=defaultdict(list)


#NOTMOVING TREND
for d, a in activitieslist:
   numofactivities[d].append(a)

numnotmovinglist=[]
for d, a in numofactivities.items():
  for i in a:
      if i==1:
          numnotmoving.append(i)
  numnotmovinglist.append((numnotmoving.count(1)))
  numnotmoving=[]

notmovinglist=[]
notmovinglist=pd.Series(numnotmovinglist, index=dates)
fig.append_trace(go.Scatter(
    name="Not Moving",
    mode="lines+markers",
    x=dates,
    y=notmovinglist
    ),
    row=1,
    col=4

)


#WALKING TREND
numwalkinglist=[]
for d, a in numofactivities.items():
  for i in a:
      if i==2:
          numwalking.append(i)
  numwalkinglist.append((numwalking.count(2)))
  numwalking=[]

walkinglist=[]
walkinglist=pd.Series(numwalkinglist, index=dates)

fig.append_trace(go.Scatter(
    name="Walking",
    mode="lines+markers",
    x=dates,
    y=walkinglist),
    row=1,
    col=4

)

#RUNNING TREND
numrunninglist=[]
for d, a in numofactivities.items():
  for i in a:
      if i==3:
          numrunning.append(i)
  numrunninglist.append((numrunning.count(3)))
  numrunning=[]

runninglist=[]
runninglist=pd.Series(numrunninglist, index=dates)
fig.append_trace(go.Scatter(
    name="Running",
    mode="lines+markers",
    x=dates,
    y=runninglist),
    row=1,
    col=4

)




#BIKING TREND
numbikinglist=[]
for d, a in numofactivities.items():
  for i in a:
      if i==4:
          numbiking.append(i)
  numbikinglist.append((numbiking.count(4)))
  numbiking=[]

bikinglist=[]
bikinglist=pd.Series(numbikinglist, index=dates)
fig.append_trace(go.Scatter(
    name="Biking",
    mode="lines+markers",
    x=dates,
    y=bikinglist),
    row=1,
    col=4

)

#SKATEBOARDING TREND
numskatelist=[]
for d, a in numofactivities.items():
  for i in a:
      if i==6:
          numskate.append(i)
  numskatelist.append((numskate.count(6)))
  numskate=[]

skatelist=[]
skatelist=pd.Series(numskatelist, index=dates)

fig.append_trace(go.Scatter(
    name="SkateBoarding",
    mode="lines+markers",
    x=dates,
    y=skatelist),
    row=1,
    col=4

)
lessthan18=[]
#Agegroup trend agegroupvals=pf["agegroup 1=<18, 2=18-30, 3=31-55, 4=>55"]
numofages=defaultdict(list)

for d, a in agegroupvalslist:
   numofages[d].append(a)

numlessthan18=[]
for d, a in numofages.items():
  for i in a:
      if i==1:
          lessthan18.append(i)
  numlessthan18.append((lessthan18.count(1)))
  lessthan18=[]

lessthan18list=[]
lessthan18list=pd.Series(numlessthan18, index=dates)


fig.append_trace(go.Scatter(
    hovertext="People Less than or equal to 18 Years old",
    name="",
    mode="lines+markers",
    x=dates,
    y=lessthan18list),
    row=2,
    col=5

)
lessthan30=[]
numlessthan30=[]
for d, a in numofages.items():
  for i in a:
      if i==2:
          lessthan30.append(i)
  numlessthan30.append((lessthan30.count(2)))
  lessthan30=[]

lessthan30list=[]
lessthan30list=pd.Series(numlessthan30, index=dates)


fig.append_trace(go.Scatter(
    hovertext="People Between 18 and 30 years old",
    name="",
    mode="lines+markers",
    x=dates,
    y=lessthan30list),
    row=2,
    col=5

)
lessthan55=[]
numlessthan55=[]
for d, a in numofages.items():
  for i in a:
      if i==3:
          lessthan55.append(i)
  numlessthan55.append((lessthan55.count(3)))
  lessthan55=[]

lessthan55list=[]
lessthan55list=pd.Series(numlessthan55, index=dates)


fig.append_trace(go.Scatter(
    hovertext="People Between 30 and 55 years old",
    name="",
    mode="lines+markers",
    x=dates,
    y=lessthan55list),
    row=2,
    col=5

)
morethan55=[]
nummorethan55=[]
for d, a in numofages.items():
  for i in a:
      if i==4:
          morethan55.append(i)
  nummorethan55.append((morethan55.count(4)))
  morethan55=[]

morethan55list=[]
morethan55list=pd.Series(nummorethan55, index=dates)


fig.append_trace(go.Scatter(
    hovertext="People Greater than or equal to 55 Years old",
    name="",
    mode="lines+markers",
    x=dates,
    y=morethan55list),
    row=2,
    col=5

)
###########################################################################

#SPLIT UP DATA BY DATE
date1lon = []
date1lat = []
date2lon = []
date2lat = []
date3lon = []
date3lat = []
date4lon = []
date4lat = []
date5lon = []
date5lat = []
for i in pf.index:
    if pf['date'][i] == '9/03/2020':
        date1lon.append(pf['LON'][i])
        date1lat.append(pf['LAT'][i])
    if pf['date'][i] == '9/11/2020':
        date2lon.append(pf['LON'][i])
        date2lat.append(pf['LAT'][i])
    if pf['date'][i] == '9/16/2020':
        date3lon.append(pf['LON'][i])
        date3lat.append(pf['LAT'][i])
    if pf['date'][i] == '9/22/2020':
        date4lon.append(pf['LON'][i])
        date4lat.append(pf['LAT'][i])
    if pf['date'][i] == '9/28/2020':
        date5lon.append(pf['LON'][i])
        date5lat.append(pf['LAT'][i])
trace1=Scattermapbox(
    name ="Buildings",
    mode = "markers",
    lon=df['LAT'],
    lat=df['LON'],
    text=df['Location'],
    hoverinfo="lon+lat+text",
    # SPECS
    marker = dict(

        # BASIC
        size=12,
        color='black',
        opacity=0.8

    ),
)

trace2 = Scattermapbox(
    name="People",
    mode="markers",
    lon=date1lat,
    lat=date1lon,
    text=pf['id'],
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='red',
        opacity=0.6
    ),

)
trace3 = Scattermapbox(
    name="People",
    mode="markers",
    lon=date2lat,
    lat=date2lon,
    text=pf['id'],
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='red',
        opacity=0.6
    ),

)
trace4 = Scattermapbox(
    name="People",
    mode="markers",
    lon=date3lat,
    lat=date3lon,
    text=pf['id'],
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='red',
        opacity=0.6
    ),

)
trace5 = Scattermapbox(
    name="People",
    mode="markers",
    lon=date4lat,
    lat=date4lon,
    text=pf['id'],
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='red',
        opacity=0.6
    ),

)
trace6 = Scattermapbox(
    name="People",
    mode="markers",
    lon=date5lat,
    lat=date5lon,
    text=pf['id'],
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='red',
        opacity=0.6
    ),

)







#Do not touch
sliders = dict(
    active=0,
    steps=[],
    currentvalue=dict(
        font=dict(size=16),
        prefix="Date : ",
        xanchor="right",
        visible=True,
    ),
    transition=dict(
        duration=300,
        easing="cubic-in-out",
    ),
    # PLACEMENT
    x=0.1,
    y=0,
    pad=dict(t=40, b=10),
    len=0.9,
    xanchor="left",
    yanchor="top",
)
#Do not touch
for date in dates:
    slider_step = dict(

        # GENERAL
        method="animate",
        value=date,
        label=date,

        # ARGUMENTS
        args=[
            [date],
            dict(
                frame=dict(duration=1000, redraw=False),
                transition=dict(duration=300),
                mode="immediate",
            ),
        ],

    )
    sliders["steps"].append(slider_step)



updatemenus = dict(

    # GENERAL
    type="buttons",
    showactive=False,
    x=0.1,
    y=0,
    pad=dict(t=40, r=125),
    xanchor="right",
    yanchor="top",
    direction="left",

    buttons=[
        dict(
            method="animate",
            label="Play",
            # PLAY
            args=[
                None,
                dict(
                    frame=dict(duration=300, redraw=False),
                    fromcurrent=True,
                    transition=dict(duration=300, easing="quadratic-in-out"),
                    mode="immediate",
                ),
            ],
        ),
        dict(
            method="animate",
            label="Pause",
            # PAUSE
            args=[
                [None],  # Note the list
                dict(
                    frame=dict(duration=0, redraw=False),  # Idem
                    mode="immediate",
                    transition=dict(duration=0),
                ),
            ],
        ),
    ],
)



fig.update_layout(
    autosize=True,
    # plot_bgcolor="#191A1A",
    # paper_bgcolor="#020202",
    margin=dict(
        t=100,
        l=100,
        b=100,
        r=100,
        pad=2,
    ),
    #sliders=[sliders],
    showlegend=False,
    hovermode="x unified",

    #sliders=[sliders],
    #updatemenus=[updatemenus],

)
layout =dict(
    title="COVID-19 Modeling Data",

    autosize = True,

    margin = dict(
        t = 80,
        l = 80,
        b = 80,
        r = 80,
        pad = 2,
    ),
    showlegend=True,
    hovermode="closest",
    #sliders=[sliders],
   #updatemenus=[updatemenus],
    #plot_bgcolor="#191A1A",
    #paper_bgcolor="#020202",
    mapbox=dict(
        accesstoken = mapbox_access_token,
        center = dict(
            lat=39.654,
            lon=-75.66
        ),
        pitch=0,
        zoom=10,
        #style = "dark",
        domain = dict(
            x = [0, 1],
            y = [0.18, 0.77]
        ),
    ),

)
#have to add back in buildings
data = [trace1, trace2, trace3, trace4,trace5, trace6]
figure = go.Figure(data=data, layout=layout)
steps=[]
num_steps=5
for i in range(num_steps):
    # Hide all traces
    step = dict(
        label=dates[i],
        method='restyle',
        args=['visible', [False] * (len(figure.data)-1)],

    )
    # Enable the two traces we want to see
    step['args'][1][i] = True
    #step['args'][1][i + num_steps] = True

    # Add step to step list
    steps.append(step)
sliders1 = [dict(
    steps =steps,
)]




figure.layout.sliders = sliders1
#fig.show()
#py.create_animations(figure)

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
              'height': 700,
            },
        ),

    ]),

    html.Div([
        dcc.Graph(
            figure=fig,
            style={
                'height':900,
            },
        ),
    ]),

])

if __name__ == '__main__':
    app.run_server(debug=True)
