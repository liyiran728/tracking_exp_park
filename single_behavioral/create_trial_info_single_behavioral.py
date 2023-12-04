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
trialfn = 'trial_info_files/trial_info_single.csv'
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

df["locArr"] = locArrays


# save
df.to_csv(outfn,index=False)
