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
# the timing file will be chosen based on subject ID mod 8
# this means that each subject will use the same timing file for every sesssion
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
# get number of runs and trials
nRuns = max(df['run'])
nTrials = max(df['trial'])
trials = range(nTrials) # for iteration
runs = range(nRuns) # for iteration
dual = df["dual"]


# ============================================
#     color
# ============================================
#10 quadrants of the tracking time available for a color switch. Choose 5-9 random
# of the quadrants (excluding quadrant 0) to switch the color of the target, and save these selected
# quadrants into divisionsChosen array
framesInEachDivision = int(np.floor(framesTracking/10))
tenDivisions = [1,2,3,4,5,6,7,8,9]

colors = ["orange", "yellow", "green", "lawngreen", "skyblue", "blue", "blueviolet", "violet", "white"]
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
        # if the current trial is dual
        if dual[run*8+trial]:
            divisionsChosen = sorted(list(np.random.choice(tenDivisions, numSwitches, replace=False)))
            # change colors from default to new array depending on number of numSwitches
            for n in range(numSwitches):
                for frameN in range(divisionsChosen[n]*framesInEachDivision, framesTracking):
                    colorArr[frameN] = colorsChosen[n]
            for frameN in range(702,750):
                colorArr[frameN] = colorArr[701]
        colorArrays.append(colorArr)



# ============================================
#     location
# ============================================
locArrays = []
for run in runs:
    for trial in trials:
        # combine three sine waves
        coefficient1 = random.randint(1,5)
        coefficient2 = random.randint(1,5)
        coefficient3 = random.randint(1,5)
        y = list(((np.sin(coefficient1*x) + np.sin(coefficient2*x) + np.sin(coefficient3*x)) / 3) * heightOfScreen)
        # add filler after 702 frames (so that it does not crash due to indexing out of range)
        for frameN in range(702,750):
            y.append(y[701])
        locArrays.append(y)





# set correct answer, location array, color array, and colors chosen columns
# we record colors chosen for the response stage of the experiment
df["corrAns"] = corrAnsArrays
df["locArr"] = locArrays
df["colorArr"] = colorArrays
df["colorsChosen"] = colorsChosenArrays


# outdated code
# the dual-task used to be counting the number of flashes
'''
    # set a random number between 1 and 4 as the correct answer
    correct = random.randrange(1,5)
    df["corrAns"][trial] = correct
    print(df["dual"][trial])
    if df["dual"][trial] == True:
        currColorArr = defaultColorArr
        interval = framesTracking / correct
        for i in range(correct):
            startFlash = random.randrange(interval * i + frameRate,
                                          interval * (i+1) - frameRate)
            for ii in range(framesFlash):
                currColorArr[startFlash + ii] = "blue"
                print(currColorArr)
'''

# save
df.to_csv(outfn,index=False)
