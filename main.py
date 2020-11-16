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
py.sign_in('alexlamattina', 'WMl4yDvoKm1xPWk9Wjxx')
import pandas as pd

mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjaXhzYTB0bHcwOHNoMnFtOWZ3YWdreDB3In0.pjROwb9_CEuyKPE-x0lRUw'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = flask.Flask(__name__)

url = 'https://raw.githubusercontent.com/AlexLaMattina/ProjectDarien/master/BuildingData.csv'
url2 = 'https://raw.githubusercontent.com/AlexLaMattina/COVID-19-Modeling/main/Data.csv'
url3='https://raw.githubusercontent.com/AlexLaMattina/ProjectDarien/master/PeopleActivity.csv'
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

masktrace = []
for i in range(len(dates)):
    masktrace.append(withmasklist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="People With Masks",
        name="",
        mode='lines+markers',
        x=dates,
        y=masktrace, ),
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

masktrace = []
for i in range(len(dates)):
    masktrace.append(withnomasklist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="People Without Masks",
        name="",
        mode='lines+markers',
        x=dates,
        y=masktrace, ),
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

masktrace = []
for i in range(len(dates)):
    masktrace.append(correctmasklist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="People Wearing Masks Correctly",
        name="",
        mode='lines+markers',
        x=dates,
        y=masktrace, ),
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
masktrace = []
for i in range(len(dates)):
    masktrace.append(incorrectmasklist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="People Wearing Masks Inorrectly",
        name="",
        mode='lines+markers',
        x=dates,
        y=masktrace, ),
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
masktrace = []
for i in range(len(dates)):
    masktrace.append(exposednoselist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="Exposed Noses",
        name="",
        mode='lines+markers',
        x=dates,
        y=masktrace, ),
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
masktrace = []
for i in range(len(dates)):
    masktrace.append(exposedmouthlist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="Exposed Nose and Mouths",
        name="",
        mode='lines+markers',
        x=dates,
        y=masktrace, ),
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

masktrace = []
for i in range(len(dates)):
    masktrace.append(socialdistancelist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="People Social Distancing",
        name="",
        mode='lines+markers',
        x=dates,
        y=masktrace),
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

masktrace = []
for i in range(len(dates)):
    masktrace.append(notsocialdistancelist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="People Not Social Distancing",
        name="",
        mode='lines+markers',
        x=dates,
        y=masktrace),
        row=2,
        col=1)
masktrace = []
for i in range(len(dates)):
    masktrace.append(numofsmoking.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="People Smoking",
        name="",
        mode='lines+markers',
        x=dates,
        y=masktrace),
        row=2,
        col=4)
masktrace = []
for i in range(len(dates)):
    masktrace.append(numofobese.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="People Who Are Obese",
        name="",
        mode='lines+markers',
        x=dates,
        y=masktrace,),
        row=2,
        col=2)
masktrace = []
for i in range(len(dates)):
    masktrace.append(numoftouchsurface.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="People Touching Surfaces",
        name="",
        mode='lines+markers',
        x=dates,
        y=masktrace),
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
masktrace = []
for i in range(len(dates)):
    masktrace.append(numofmalelist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="Males",
        name="", #"Number of People With Etiquette",
        mode='lines+markers',
        x=dates,
        y=masktrace),#numofetiquette),
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
masktrace = []
for i in range(len(dates)):
    masktrace.append(numoffemalelist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="Females",
        name="",#"Number of People With Etiquette",
        mode='lines+markers',
        x=dates,
        y=masktrace),#numofetiquette),
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
masktrace = []
for i in range(len(dates)):
    masktrace.append(notmovinglist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        name="Not Moving",
        mode="lines+markers",
        x=dates,
        y=masktrace,
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
masktrace = []
for i in range(len(dates)):
    masktrace.append(walkinglist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        name="Walking",
        mode="lines+markers",
        x=dates,
        y=masktrace),
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
masktrace = []
for i in range(len(dates)):
    masktrace.append(runninglist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        name="Running",
        mode="lines+markers",
        x=dates,
        y=masktrace),
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
masktrace = []
for i in range(len(dates)):
    masktrace.append(bikinglist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        name="Biking",
        mode="lines+markers",
        x=dates,
        y=masktrace),
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
masktrace = []
for i in range(len(dates)):
    masktrace.append(skatelist.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        name="SkateBoarding",
        mode="lines+markers",
        x=dates,
        y=masktrace),
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

masktrace = []
for i in range(len(dates)):
    masktrace.append(lessthan18list.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="People Less than or equal to 18 Years old",
        name="",
        mode="lines+markers",
        x=dates,
        y=masktrace),
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

masktrace = []
for i in range(len(dates)):
    masktrace.append(lessthan30list.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="People Between 18 and 30 years old",
        name="",
        mode="lines+markers",
        x=dates,
        y=masktrace,),
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

masktrace = []
for i in range(len(dates)):
    masktrace.append(lessthan55list.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="People Between 30 and 55 years old",
        name="",
        mode="lines+markers",
        x=dates,
        y=masktrace),
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

masktrace = []
for i in range(len(dates)):
    masktrace.append(morethan55list.get(key=dates[i]))
    fig.append_trace(go.Scatter(
        hovertext="People Greater than or equal to 55 Years old",
        name="",
        mode="lines+markers",
        x=dates,
        y=masktrace,),
        row=2,
        col=5

    )
steps=[]
num_steps=5
for i in range(num_steps):
    step=dict(
        method='restyle',
        args=['visible', [False] * len(fig.data)],
    )
    step['args'][1][i]=True
    step['args'][1][i+num_steps]=True
    steps.append(step)

slidersfig=[dict(steps=steps,)]

###########################################################################

#SPLIT UP DATA BY DATE
date1masklon = []
date1masklat = []
date1id=[]
date1nomasklon=[]
date1nomasklat=[]
date1unknownlon=[]
date1unknownlat=[]


date2masklon = []
date2masklat = []
date2id=[]
date2nomasklon=[]
date2nomasklat=[]
date2unknownlon=[]
date2unknownlat=[]

date3masklon = []
date3masklat = []
date3id=[]
date3nomasklon=[]
date3nomasklat=[]
date3unknownlon=[]
date3unknownlat=[]

date4masklon = []
date4masklat = []
date4id=[]
date4nomasklon=[]
date4nomasklat=[]
date4unknownlon=[]
date4unknownlat=[]

date5masklon = []
date5masklat = []
date5id=[]
date5nomasklon=[]
date5nomasklat=[]
date5unknownlon=[]
date5unknownlat=[]

date6masklon = []
date6masklat = []
date6id=[]
date6nomasklon=[]
date6nomasklat=[]
date6unknownlon=[]
date6unknownlat=[]

date7masklon = []
date7masklat = []
date7id=[]
date7nomasklon=[]
date7nomasklat=[]
date7unknownlon=[]
date7unknownlat=[]

masklon=[]
masklat=[]
ids=[]
nomasklon=[]
nomasklat=[]
unknownlon=[]
unknownlat=[]

for i in pf.index:
    ids.append(pf['id'][i])
    if pf["withmask 0=no, 1=yes"][i] == 1:
        masklon.append(pf['LON'][i])
        masklat.append(pf['LAT'][i])
    elif pf["withmask 0=no, 1=yes"][i] == 0:
        nomasklon.append(pf['LON'][i])
        nomasklat.append(pf['LAT'][i])
    else:
        unknownlon.append(pf['LON'][i])
        unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '8/24/2020':
        date1id.append(pf['id'][i])
        if pf["withmask 0=no, 1=yes"][i] == 1:
            date1masklon.append(pf['LON'][i])
            date1masklat.append(pf['LAT'][i])
        elif pf["withmask 0=no, 1=yes"][i] == 0:
            date1nomasklon.append(pf['LON'][i])
            date1nomasklat.append(pf['LAT'][i])
        else:
            date1unknownlon.append(pf['LON'][i])
            date1unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '8/24/2020':
        date2id.append(pf['id'][i])
        if pf["withmask 0=no, 1=yes"][i] == 1:
            date2masklon.append(pf['LON'][i])
            date2masklat.append(pf['LAT'][i])
        elif pf["withmask 0=no, 1=yes"][i] == 0:
            date2nomasklon.append(pf['LON'][i])
            date2nomasklat.append(pf['LAT'][i])
        else:
            date2unknownlon.append(pf['LON'][i])
            date2unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '9/03/2020':
        date3id.append(pf['id'][i])
        if pf["withmask 0=no, 1=yes"][i] == 1:
            date3masklon.append(pf['LON'][i])
            date3masklat.append(pf['LAT'][i])
        elif pf["withmask 0=no, 1=yes"][i] == 0:
            date3nomasklon.append(pf['LON'][i])
            date3nomasklat.append(pf['LAT'][i])
        else:
            date3unknownlon.append(pf['LON'][i])
            date3unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '9/11/2020':
        date4id.append(pf['id'][i])
        if pf["withmask 0=no, 1=yes"][i] == 1:
            date4masklon.append(pf['LON'][i])
            date4masklat.append(pf['LAT'][i])
        elif pf["withmask 0=no, 1=yes"][i] == 0:
            date4nomasklon.append(pf['LON'][i])
            date4nomasklat.append(pf['LAT'][i])
        else:
            date4unknownlon.append(pf['LON'][i])
            date4unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '9/16/2020':
        date3id.append(pf['id'][i])
        if pf["withmask 0=no, 1=yes"][i] == 1:
            date5masklon.append(pf['LON'][i])
            date5masklat.append(pf['LAT'][i])
        elif pf["withmask 0=no, 1=yes"][i] == 0:
            date5nomasklon.append(pf['LON'][i])
            date5nomasklat.append(pf['LAT'][i])
        else:
            date5unknownlon.append(pf['LON'][i])
            date5unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '9/22/2020':
        date6id.append(pf['id'][i])
        if pf["withmask 0=no, 1=yes"][i] == 1:
            date6masklon.append(pf['LON'][i])
            date6masklat.append(pf['LAT'][i])
        elif pf["withmask 0=no, 1=yes"][i] == 0:
            date6nomasklon.append(pf['LON'][i])
            date6nomasklat.append(pf['LAT'][i])
        else:
            date6unknownlon.append(pf['LON'][i])
            date6unknownlat.append(pf['LAT'][i])

    if pf['date'][i] == '9/28/2020':
        date3id.append(pf['id'][i])
        if pf["withmask 0=no, 1=yes"][i] == 1:
            date7masklon.append(pf['LON'][i])
            date7masklat.append(pf['LAT'][i])
        elif pf["withmask 0=no, 1=yes"][i] == 0:
            date7nomasklon.append(pf['LON'][i])
            date7nomasklat.append(pf['LAT'][i])
        else:
            date7unknownlon.append(pf['LON'][i])
            date7unknownlat.append(pf['LAT'][i])

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
    legendgroup="Buildings",
)
date1df = DataFrame(date1id,columns=['ID'])
trace2 = Scattermapbox(
    name="Mask Data",
    mode="markers",
    lon=date1masklat,
    lat=date1masklon,
    text="ID: " + date1df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='green',
        opacity=0.6
    ),
    legendgroup="Mask Data",
    showlegend=False,

)

trace3 = Scattermapbox(
    name="No Mask Data",
    mode="markers",
    lon=date1nomasklat,
    lat=date1nomasklon,
    text="ID: " + date1df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='red',
        opacity=0.6
    ),
    legendgroup="No Mask Data",
    showlegend=False,

)
trace4 = Scattermapbox(
    name="Unknown Mask Data",
    mode="markers",
    lon=date1unknownlat,
    lat=date1unknownlon,
    text="ID: " + date1df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='blue',
        opacity=0.6
    ),
    legendgroup="Unknown data",
    showlegend=False,

)
date2df = DataFrame(date2id,columns=['ID'])
trace5 = Scattermapbox(
    name="8/24/2020 Mask Data",
    mode="markers",
    lon=date2masklat,
    lat=date2masklon,
    text="ID: " + date2df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='green',
        opacity=0.6
    ),
    legendgroup="Mask Data",
    showlegend=False,

)

trace6 = Scattermapbox(
    name="8/24/2020 No Mask Data",
    mode="markers",
    lon=date2nomasklat,
    lat=date2nomasklon,
    text="ID: " + date2df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='red',
        opacity=0.6
    ),
    legendgroup="No Mask Data",
    showlegend=False,

)
trace7 = Scattermapbox(
    name="8/24/2020 Unknown Data",
    mode="markers",
    lon=date2unknownlat,
    lat=date2unknownlon,
    text="ID: " + date2df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='blue',
        opacity=0.6
    ),
    legendgroup="Unknown data",
    showlegend=False,

)
date3df = DataFrame(date3id,columns=['ID'])
trace8 = Scattermapbox(
    name="9/03/2020 Mask Data",
    mode="markers",
    lon=date3masklat,
    lat=date3masklon,
    text="ID: " + date3df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='green',
        opacity=0.6
    ),
    legendgroup="Mask Data",
    showlegend=False,

)

trace9 = Scattermapbox(
    name="No Mask Data",
    mode="markers",
    lon=date3nomasklat,
    lat=date3nomasklon,
    text="ID: " + date3df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='red',
        opacity=0.6
    ),
    legendgroup="No Mask Data",
    showlegend=False,

)
trace10 = Scattermapbox(
    name="9/03/2020 Unknown Data",
    mode="markers",
    lon=date3unknownlat,
    lat=date3unknownlon,
    text="ID: " + date3df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='blue',
        opacity=0.6
    ),
    legendgroup="Unknown data",
    showlegend=False,

)
date4df = DataFrame(date4id,columns=['ID'])
trace11 = Scattermapbox(
    name="9/11/2020 Mask Data",
    mode="markers",
    lon=date3masklat,
    lat=date3masklon,
    text="ID: " + date3df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='green',
        opacity=0.6
    ),
    legendgroup="Mask Data",
    showlegend=False,

)

trace12 = Scattermapbox(
    name="9/11/2020 No Mask Data",
    mode="markers",
    lon=date4nomasklat,
    lat=date4nomasklon,
    text="ID: " + date4df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='red',
        opacity=0.6
    ),
    legendgroup="No Mask Data",
    showlegend=False,

)
trace13 = Scattermapbox(
    name="9/11/2020 UnKnown Data",
    mode="markers",
    lon=date4unknownlat,
    lat=date4unknownlon,
    text="ID: " + date4df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='blue',
        opacity=0.6
    ),
    legendgroup="Unknown data",
    showlegend=False,

)
date5df = DataFrame(date5id,columns=['ID'])
trace14 = Scattermapbox(
    name="9/16/2020 Mask Data",
    mode="markers",
    lon=date5masklat,
    lat=date5masklon,
    text="ID: " + date5df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='green',
        opacity=0.6
    ),
    legendgroup="Mask Data",
    showlegend=False,

)

trace15 = Scattermapbox(
    name="9/16/2020 No Mask Data",
    mode="markers",
    lon=date5nomasklat,
    lat=date5nomasklon,
    text="ID: " + date5df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='red',
        opacity=0.6
    ),
    legendgroup="No Mask Data",
    showlegend=False,

)
trace16 = Scattermapbox(
    name="9/16/2020 UnKnown Data",
    mode="markers",
    lon=date5unknownlat,
    lat=date5unknownlon,
    text="ID: " + date5df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='blue',
        opacity=0.6
    ),
    legendgroup="Unknown data",
    showlegend=False,

)
date6df = DataFrame(date6id,columns=['ID'])
trace17 = Scattermapbox(
    name="9/22/2020 Mask Data",
    mode="markers",
    lon=date6masklat,
    lat=date6masklon,
    text="ID: " + date6df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='green',
        opacity=0.6
    ),
    legendgroup="Mask Data",
    showlegend=False,

)

trace18 = Scattermapbox(
    name="9/22/2020 No Mask Data",
    mode="markers",
    lon=date6nomasklat,
    lat=date6nomasklon,
    text="ID: " + date6df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='red',
        opacity=0.6
    ),
    legendgroup="No Mask Data",
    showlegend=False,

)
trace19 = Scattermapbox(
    name="9/22/2020 UnKnown Data",
    mode="markers",
    lon=date6unknownlat,
    lat=date6unknownlon,
    text="ID: " + date6df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='blue',
        opacity=0.6
    ),
    legendgroup="Unknown data",
    showlegend=False,

)


date7df = DataFrame(date7id,columns=['ID'])

trace20 = Scattermapbox(
    name="9/28/2020 Mask Data",
    mode="markers",
    lon=date7masklat,
    lat=date7masklon,
    text="ID: " + date7df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='green',
        opacity=0.6
    ),
    legendgroup="Mask data",
    showlegend=False,

)

trace21 = Scattermapbox(
    name="9/28/2020 No Mask Data",
    mode="markers",
    lon=date7nomasklat,
    lat=date7nomasklon,
    text="ID: " + date7df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='red',
        opacity=0.6
    ),
    legendgroup="No Mask data",
    showlegend=False,

)
trace22 = Scattermapbox(
    name="9/28/2020 UnKnown Data",
    mode="markers",
    lon=date7unknownlat,
    lat=date7unknownlon,
    text="ID: " + date7df['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='blue',
        opacity=0.6
    ),
    legendgroup="Unknown data",
    showlegend=False,

)
iddf = DataFrame(ids,columns=['ID'])
trace23 = Scattermapbox(
    name="Mask Data",
    mode="markers",
    lon=masklat,
    lat=masklon,
    text="ID: " + iddf['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='green',
        opacity=0.6
    ),
    legendgroup="Mask data",

)

trace24 = Scattermapbox(
    name="No Mask Data",
    mode="markers",
    lon=nomasklat,
    lat=nomasklon,
    text="ID: " + iddf['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='red',
        opacity=0.6
    ),
    legendgroup="No Mask data",

)
trace25 = Scattermapbox(
    name="UnKnown Mask Data",
    mode="markers",
    lon=unknownlat,
    lat=unknownlon,
    text="ID: " + iddf['ID'].astype(str),
    hoverinfo="lon+lat+text",
    # SPECS
    marker=dict(

        # BASIC
        size=8,
        color='blue',
        opacity=0.6
    ),
    legendgroup="Unknown data",

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
    showlegend=False,
    hovermode="x unified",

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
    #showlegend=False,
    hovermode="closest",
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
data = [trace1,trace23,trace24,trace25,trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10, trace11, trace12, trace13,
        trace14, trace15, trace16, trace17, trace18, trace19, trace20, trace21, trace22]
labels=["Buildings","All Data","","", "8/20/2020","","","8/24/2020","","","9/03/2020","","","9/11/2020","","","9/16/2020","","","9/22/2020","","","9/28/2020""","",]
figure = go.Figure(data=data, layout=layout)
steps=[]
num_steps=25
count=8

for i in range(1,num_steps,3):
    step = dict(
        label=labels[i],
        method='restyle',
        args=['visible', ['legendonly'] * len(figure.data)],
    )
    if i < num_steps:
        step['args'][1][i] = True

    if i+1 < num_steps:
        step['args'][1][i+1] = True

    if i+2 < num_steps or i+2 == num_steps:
        step['args'][1][i+2] = True

    step['args'][1][0] = True
    steps.append(step)

sliders = [dict(
    steps =steps,
    currentvalue=dict(
        font=dict(size=16),
        prefix="Date : ",
        xanchor="right",
        visible=True,
    ),


)]
steps=[]
num_steps = 7
for i in range(num_steps):
    step=dict(
        label=dates[i],
        method='restyle',
        args=['visible', [False] * len(fig.data)],
    )
    step['args'][1][i]=True
    step['args'][1][i+num_steps]=True
    step['args'][1][i+2*(num_steps)]=True
    step['args'][1][i+3*(num_steps)]=True
    step['args'][1][i+4*(num_steps)]=True
    step['args'][1][i+5*(num_steps)]=True
    step['args'][1][i+6*(num_steps)]=True
    step['args'][1][i+7*(num_steps)]=True
    step['args'][1][i+8*(num_steps)]=True
    step['args'][1][i+9*(num_steps)]=True
    step['args'][1][i+10*(num_steps)]=True
    step['args'][1][i+11*(num_steps)]=True
    step['args'][1][i+12*(num_steps)]=True
    step['args'][1][i+13*(num_steps)]=True
    step['args'][1][i+14* (num_steps)] = True
    step['args'][1][i+15* (num_steps)] = True
    step['args'][1][i+16* (num_steps)] = True
    step['args'][1][i+17* (num_steps)] = True
    step['args'][1][i+18* (num_steps)] = True
    step['args'][1][i+19* (num_steps)] = True
    step['args'][1][i+20* (num_steps)] = True
    step['args'][1][i+21* (num_steps)] = True

    steps.append(step)

slidersfig=[dict(steps=steps,
    currentvalue=dict(
    font=dict(size=15),
    prefix="Date : ",
    xanchor="right",
    visible=True,

    ),y=-.15,)]

fig.layout.sliders=slidersfig
figure.layout.sliders = sliders
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