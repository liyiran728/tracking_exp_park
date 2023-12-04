from itertools import product
from psychopy import gui, core
import numpy as np
import pandas as pd
import os
import time
import csv
import sys
import ast
import random

# TODO: generate multiple runs

# get input
V = {'Subject ID':'', 'Day':''}
dlg = gui.DlgFromDict(dictionary=V, sortKeys=False)
if not dlg.OK:
    core.quit()
subid = V['Subject ID']
subday = V['Day']
# set directory to be the folder that this file is in
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
infoNum = int(subid) % 8
trialfn = 'trial_info_files/trial_info_' + str(infoNum) + '.csv'
outfn = os.path.join('trial_info_files',subid + '_Day' + subday + '_trialinfo.csv')

# define conditions
frameRate = 60
timeTracking = 11.7
framesTracking = int(frameRate * timeTracking) # 702 frames in 11.7 seconds
x = np.linspace(0,2*np.pi, num = framesTracking)
heightOfScreen = 0.875

#read trial info file
df = pd.read_csv(trialfn)
# get number of trials from number of rows in the file
nRuns = max(df['run'])
nTrials = max(df['trial'])
trials = range(nTrials) # for iteration
runs = range(nRuns)
dual = df["dual"]


# ============================================
#     color
# ============================================
#10 quadrants of the tracking time available for a color switch. Choose 5-9 random
# of the quadrants (excluding quadrant 0) to switch the color of the target, and save these selected
# quadrants into divisionsChosen array
framesInEachDivision = int(np.floor(framesTracking/10))
tenDivisions = [1,2,3,4,5,6,7,8,9]

colors = ["darkorange", "yellow", "darkgreen", "palegreen", "cyan", "mediumblue", "darkorchid", "pink", "white"]
colorArrays = []
colorsChosenArrays = []
corrAnsArrays = []

# set a default color array of all red
defaultColorArr = []
for n in range(framesTracking + 48): #add filler after 702 frames
    defaultColorArr.append("red")
for run in runs:
    for trial in trials:
        # set colorArr to be a shallow copy of the default color array (all red)
        colorArr = defaultColorArr.copy()
        # decide number of switches (useless in single trials, just putting this here so it runs
        numSwitches = random.randint(5,9)
        # choose colors from choices
        colorsChosen = list(np.random.choice(colors, numSwitches, replace=False))
        colorsChosenArrays.append(colorsChosen)
        corrAnsArrays.append(colorsChosen[-3])

        if dual[run*8+trial]:
            #divisionsChosen = (np.random.choice(tenDivisions, numSwitches, replace=False)).sort()
            divisionsChosen = sorted(list(np.random.choice(tenDivisions, numSwitches, replace=False)))
            # change colors from default to new array depending on number of numSwitches
            for n in range(numSwitches):
                for frameN in range(divisionsChosen[n]*framesInEachDivision, framesTracking):
                    colorArr[frameN] = colorsChosen[n]
            # add 50ish frames to color array that match the last color value, then add list to colorArrays
            for frameN in range(702,750):
                colorArr[frameN] = colorArr[701]
        colorArrays.append(colorArr)



# ============================================
#     location
# ============================================
locArrays = []
for run in runs:
    for trial in trials:
        distance = 0
        y = [0]*705
        #calculate a new trajectory until distance travelled fits within these desired values (25th-75th percentile)
        while (distance < 5.5) or (distance > 7.8):
            coefficient1 = random.randint(1,5)
            coefficient2 = random.randint(1,5)
            coefficient3 = random.randint(1,5)
            y = list(((np.sin(coefficient1*x) + np.sin(coefficient2*x) + np.sin(coefficient3*x)) / 3) * heightOfScreen)
            
            #calculate the difference between each point in list "y" and sum up the total distance travelled
            differenceList = np.diff(y)
            differenceList = np.absolute(differenceList)
            distance = np.sum(differenceList)
            #print(distance)

        #add 50 frames to the end of the position array that match the last position, then add list to locArrays
        for frameN in range(702,750):
            y.append(y[701])
        #print("added")
        locArrays.append(y)





#initialize trial, run, correct answer, location array, and color array columns
df["corrAns"] = corrAnsArrays
df["locArr"] = locArrays
df["colorArr"] = colorArrays
df["colorsChosen"] = colorsChosenArrays

# save
df.to_csv(outfn,index=False)
