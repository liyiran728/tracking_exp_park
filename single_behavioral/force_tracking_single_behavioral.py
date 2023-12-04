# This version is adapted from a dual-task version
# Made by Yiran Li and Erin Proctor from the CoCoA Lab

from psychopy.hardware import joystick
from psychopy import visual, event, core, monitors, gui, misc
import numpy as np
import pandas as pd
import csv
import time
import sys
import os
import ast
import random

# functions below are for calibrations and calculating the location of crosshair on screen
def unitscale(vals,minVal,maxVal):
    return(min((vals - minVal) / (0.3*(maxVal - minVal)),1))

def locCalc(vals, minVal, maxVal):
    return(unitscale(vals,minVal,maxVal) * ((1 - 0.075) * 2) + (-0.925))

def loc(ypos, minVal, maxVal):
    if  unitscale(ypos,minVal,maxVal) < .05:
        loc = [0,-0.925]
    else:
        loc = [0,locCalc(ypos,minVal,maxVal)]
    return loc

# ====================================================
# Intro-dialogue. Get subject-id and other variables.
# ====================================================
# Save input variables
expName = 'force_tracking_single_behavioral'
expInfo = {'Subject ID':'', 'Day':'', 'TMS Site':'', 'Hand':'', 'Run':''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)

if not dlg.OK:
    sys.exit(0)
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
curr_run_num = int(expInfo['Run'])
trialfn = 'trial_info_files/%s_Day%s_trialinfo.csv' % (expInfo['Subject ID'], expInfo['Day'])
outfn = 'output_files/%s_Day%s_%s_%s_Run%s.csv' % (expInfo['Subject ID'], expInfo['Day'],
        expInfo['TMS Site'], expInfo['Hand'], expInfo['Run'])

# check if session/run already exists
if os.path.exists(outfn):
    resp = input('%s already exists! Continue? [y/n]: ' % (outfn))
    if resp == 'y':
        pass
    else:
        sys.exit(0)

# =================
# trial parameters
# =================
# read in the original csv file with the timings
fileInfo = pd.read_csv(trialfn)
# select the information for the current run
trialInfo = fileInfo[fileInfo.run == curr_run_num]
# reindex the dataframe so the indexes starts from 0
trialInfo.reset_index(drop=True,inplace=True)

equalNum = 2 # number of scanner input before experiment starts
numTrials = max(trialInfo['trial'])
speed = .01
radius = .125

# ==================
# create trial list
# ==================
trialList = []
for ii in range(numTrials):
    trialList.append({'run': trialInfo['run'][ii],
                      'trial': trialInfo['trial'][ii],
                      'locArr': ast.literal_eval(trialInfo['locArr'][ii]),
                      'trackingStart': trialInfo['trackingStart'][ii],
                      'trackingBegin':0,
                      'trackingEnd':0,
                      'ypos_track_vals': [],
                      'totalFrames': 0,
                      'numFramesInTarget' : 0,
                      'pctFramesInTarget' : 0,
                      'arrFramesInTarget' : [],
                      'maxVal' : 0, 'minVal' : 0,
                      'distFromTarget': [],
                      'sumSquared': 0,'RMSE': 0,
                      'avgDistFromTarget': 0
                      })

# ===========
# timing info
# ===========
timeInst = 1.3
timePrepare = 1.3
timeTrack = 11.7

# ==========================
# window and joystick setup
# ==========================
red = [1,-1,-1]
black = [-1,-1,-1]
blue = [-1,-1,1]
grey = [0.15,0.15,0.15]
joystick.backend = 'pygame'
testingRoomMonitor = monitors.Monitor('testing_room',distance = 66, width = 52)
testingRoomMonitor.setSizePix((1920,1080))
win = visual.Window(size=[1000, 1000], fullscr=False, screen=0, allowGUI=True, allowStencil=False,
                    monitor='testMonitor', color=black, colorSpace='rgb', blendMode='avg', useFBO=True)
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0
joystick.backend = 'pyglet'
nJoys = joystick.getNumJoysticks()
joy = joystick.Joystick(0)

# =================
# stimulus objects
# =================
calibrationStartText = visual.TextStim(win,'Press <space> to begin calibration', pos = (0,0),height = 0.2)
calibration_text = visual.TextStim(win,"Release grip fully", height = 0.2, pos = [0,-0.15])
countdownText = visual.TextStim(win,'5',pos = (0,0.5),height = 0.2)
startText = visual.TextStim(win,'Press <space> to begin experiment', pos = (0,0),height = 0.2)
target = visual.Circle(win=win, name='target', units='norm', radius=.125,
	fillColor='red', fillColorSpace='rgb', opacity=1, depth=-1.0, interpolate=True)
crosshair = visual.Circle(win=win, name='crosshair', units='norm', radius=.075,
	fillColor='grey', fillColorSpace='rgb', opacity=1, depth=0.0, interpolate=True)
fixCross = visual.ShapeStim(win=win, name='polygon', vertices='cross',
	size=(0.1, 0.1), ori=0, pos=(0, 0), lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
	fillColor='white', fillColorSpace='rgb', opacity=1, depth=0.0, interpolate=True)
endText = visual.TextStim(win=win, text="End of Experiment\n\nEsc to exit", pos = (0,0), height=.2)
inputText = visual.TextStim(win=win, text="Waiting for input from scanner", pos = (0,0.45), height=.2)

# ==================
# create output file
# ==================
with open(outfn,'w',newline="") as f:
    w = csv.DictWriter(f,trialList[0].keys())
    w.writeheader()

# ======================
# stimulus presentation
# ======================
# wait for <space> to begin calibration
calibrationStartText.draw()
win.flip()
event.clearEvents()
while True:
    keys = event.getKeys(keyList = ['space', 'escape'])
    if 'space' in keys:
        break
    if 'escape' in keys:
        win.close()
        core.quit()
        win.flip()

# create timers
experimentTimer = core.Clock()
timer = core.CountdownTimer()

#calibration
timer.reset(3)
force_vals = np.array([])
while timer.getTime() > 0:
    force_vals = np.append(force_vals,joy.getY())
    countdownText.text = '%d' % int(np.ceil(timer.getTime()))
    countdownText.draw()
    calibration_text.draw()
    win.flip()

timer.reset(3)
calibration_text.text = "Now squeeze sensor as hard as you can"
while timer.getTime() > 0:
    force_vals = np.append(force_vals,joy.getY())
    countdownText.text = '%d' % int(np.ceil(timer.getTime()))
    countdownText.draw()
    calibration_text.draw()
    win.flip()
maxVal = np.max(force_vals[force_vals != 0.0])
minVal = np.min(force_vals[force_vals != 0.0])

# wait for <space> to begin experiment
startText.draw()
win.flip()
event.clearEvents()
while True:
    keys = event.getKeys(keyList = ['space', 'escape'])
    if 'space' in keys:
        break
    if 'escape' in keys:
        win.close()
        core.quit()
        win.flip()


# Reset the timer
experimentTimer.reset()

# Trial Loop
for idx, trial in enumerate(trialList):
    # Fixation before tracking
    while experimentTimer.getTime() < trial['trackingStart']:
        fixCross.draw()
        win.flip()

    #Prepare screen (1.3 seconds of fixed target before it starts moving)
    timer.reset(timePrepare)
    trial['trackingBegin'] = experimentTimer.getTime()
    #target.setColor(trial['colorArr'][0])
    while timer.getTime() > 0:
        target.setPos((0, trial['locArr'][0]))
        target.draw()
        crosshair.pos = loc(joy.getY(), minVal, maxVal)
        crosshair.draw()
        win.flip()

    # Target starts moving, tracking begins
    frameN = 0
    timer.reset(timeTrack)
    while timer.getTime() > 0:
        # change the location of target every frame
        target.setPos((0, trial['locArr'][frameN]))
        #target.setColor(trial['colorArr'][frameN])
        target.draw()
        # change the location of crosshair every frame
        crosshair.pos = loc(joy.getY(), minVal, maxVal)
        crosshair.draw()
        win.flip()
        # Record crosshair position by frame
        trial['ypos_track_vals'].append(crosshair.pos[1])
        # Record distance from target to crosshair by frame
        dist = target.pos[1] - crosshair.pos[1]
        trial['distFromTarget'].append(dist)
        # Calculate frames in target
        # The crosshair is in target if its center is in target
        if abs(dist) <= radius:
            trial['arrFramesInTarget'].append(1)
            trial['numFramesInTarget'] += 1
        else:
            trial['arrFramesInTarget'].append(0)
        # calculate the percentage of frames in target
        trial['pctFramesInTarget'] = (trial['numFramesInTarget']/(frameN+1))*100
        frameN += 1
    trial['trackingEnd'] = experimentTimer.getTime() # should be 26.3 for first trial
    trial['totalFrames'] = frameN + 1
    frameN = 0
    chyPos = (0,0)

    #append max value and min value from calibration
    trial['maxVal'] = maxVal
    trial['minVal'] = minVal
    #calcualte average distance from target for each trial in trial list, using the
    #distance from target in each frame. Update mean every time the distance from a new frame is added.
    #Also, collect the number of frames the crosshair is in target *to do
    distFromTargetSum = 0
    totalFrames = 0
    for idx2, dist in enumerate(trial['distFromTarget']):
        distFromTargetSum += abs(dist)
        distFromTargetSquared = dist**2
        trial['sumSquared'] += distFromTargetSquared
        totalFrames = idx2 + 1
    trial['avgDistFromTarget'] = distFromTargetSum/totalFrames
    trial['RMSE'] = np.sqrt(trial['sumSquared']/totalFrames)

    with open(outfn,'a',newline="") as f:
        w = csv.DictWriter(f,trial.keys())
        w.writerow(trial)
    # check for escape key

# add 5 seconds of fixation at the end
timer.reset(5)
while timer.getTime() > 0:
    fixCross.draw()
    win.flip()

endText.draw()
win.flip()
event.clearEvents()
while True:
    keys = event.getKeys(keyList = ['escape'])
    if 'escape' in keys:
        win.close()
        core.quit()
        win.flip()
