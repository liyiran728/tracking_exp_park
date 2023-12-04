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
expName = 'park_TMS'
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
                      #'dual': trialInfo['dual'][ii],
                      'corrAns': trialInfo['corrAns'][ii],
                      'locArr': ast.literal_eval(trialInfo['locArr'][ii]),
                      #'colorArr': ast.literal_eval(trialInfo['colorArr'][ii]),
                      'cueStart': trialInfo['cueStart'][ii],
                      'cueBegin':0,
                      'cueEnd':0,
                      'trackingStart': trialInfo['trackingStart'][ii],
                      'trackingBegin':0,
                      'trackingEnd':0,
                      'respStart': trialInfo['respStart'][ii],
                      'respBegin':0,
                      'respEnd':0,
                      #'colorsChosen': ast.literal_eval(trialInfo['colorsChosen'][ii]),
                      'ypos_track_vals': [],
                      'totalFrames': 0,
                      'numFramesInTarget' : 0,
                      'pctFramesInTarget' : 0,
                      'arrFramesInTarget' : [],
                      #'ypos_resp_vals': [],
                      'maxVal' : 0, 'minVal' : 0,
                      #'resp': 0, 'correct': 0,
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
timeResponse = 3.25
timeOff = 13.0

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
#win = visual.Window([1000,1000],winType = 'pygame',monitor = testingRoomMonitor,
#                    units = 'norm',fullscr=False,color = grey)
win = visual.Window(size=[650, 650], fullscr=False, screen=0, allowGUI=True, allowStencil=False,
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
#singleText = visual.TextStim(win=win, text="Single", pos = (0,0), height=.2)
#dualText = visual.TextStim(win=win, text="Dual", pos = (0,0), height=.2)
'''
fourCircle = visual.Circle(win=win, name='target', units='norm', radius=.125,
	fillColor='red', fillColorSpace='rgb', opacity=1, depth=-1.0, pos = (0,0.675), interpolate=True)
threeCircle = visual.Circle(win=win, name='target', units='norm', radius=.125,
	fillColor='red', fillColorSpace='rgb', opacity=1, depth=-1.0, pos = (0,0.225), interpolate=True)
twoCircle = visual.Circle(win=win, name='target', units='norm', radius=.125,
	fillColor='red', fillColorSpace='rgb', opacity=1, depth=-1.0, pos = (0,-0.225), interpolate=True)
oneCircle = visual.Circle(win=win, name='target', units='norm', radius=.125,
	fillColor='red', fillColorSpace='rgb', opacity=1, depth=-1.0, pos = (0,-0.675), interpolate=True)
choiceCircle = visual.Circle(win=win, name='target', units='norm', radius=.1,
	fillColor='red', fillColorSpace='rgb', opacity=1, depth=-1.0, pos = (0.6,-0.25), interpolate=True)
#oneText = visual.TextStim(win=win, text="1", pos = (0,-0.675), height=.15)
#twoText = visual.TextStim(win=win, text="2", pos = (0,-0.225), height=.15)
#threeText = visual.TextStim(win=win, text="3", pos = (0,0.225), height=.15)
#fourText = visual.TextStim(win=win, text="4", pos = (0,0.675), height=.15)
moveText = visual.TextStim(win=win, text="Move to", pos = (0.6,0), height=.2)
reportText = visual.TextStim(win=win, text="2-back\ncolor\n?", pos = (0.6,0), height=.2)
'''
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


# wait for equalNum ttl pulses from scan(=)
# wait for the next ttl pulse to reset timer and start experiment
for i in range(equalNum+1):
    startText.text = str(equalNum + 1 - i)
    startText.draw()
    inputText.draw()
    win.flip()
    while True:
        keys = event.getKeys(keyList = ['equal', 'escape'])
        if 'equal' in keys:
            break
        if 'escape' in keys:
            win.close()
            core.quit()
            win.flip()
# Reset the timer
experimentTimer.reset()

# Trial Loop
for idx, trial in enumerate(trialList):
    # Fixation before cue
    while experimentTimer.getTime() < trial['cueStart']:
        fixCross.draw()
        win.flip()
    #Instruction (cue) screen (for this single-task version, this will be fixation)
    timer.reset(timeInst)
    trial['cueBegin'] = experimentTimer.getTime()
    while timer.getTime() > 0:
        '''
        if trial['dual'] == True:
            dualText.draw()
            win.flip()
        else:

        singleText.draw()
        win.flip()
        '''
        fixCross.draw()
        win.flip()
    trial['cueEnd'] = experimentTimer.getTime() # should be ~9.3 for first trial

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

    # Fixation before response
    while experimentTimer.getTime() < trial['respStart']:
        fixCross.draw()
        win.flip()

    # Response screen (in this version, this part will be fixation)
    '''
    colors = []
    timer.reset(timeResponse)
    trial['respBegin'] = experimentTimer.getTime()
    # the color choices will be the last four colors presented
    for n in range(-4,0):
        colors.append(trial['colorsChosen'][n])
    # shuffle the order of the color
    random.shuffle(colors)
    while timer.getTime() > 0:
        oneCircle.setColor(colors[0])
        oneCircle.draw()
        twoCircle.setColor(colors[1])
        twoCircle.draw()
        threeCircle.setColor(colors[2])
        threeCircle.draw()
        fourCircle.setColor(colors[3])
        fourCircle.draw()
        #oneText.draw()
        #twoText.draw()
        #threeText.draw()
        #fourText.draw()
        crosshair.pos = loc(joy.getY(), minVal, maxVal)
        chyPos = crosshair.pos[1]
        trial['ypos_resp_vals'].append(locCalc(joy.getY(),minVal,maxVal))
        crosshair.draw()
        # if dual task, say "2-back color?"
        if trial['dual'] == True:
            reportText.draw()
        # if single task, say "Move to", and then show one of the four colors on screen
        else:
            moveText.draw()
            choiceCircle.setColor(trial['corrAns'])
            choiceCircle.draw()
        win.flip()
    '''
    timer.reset(timeResponse)
    #this line is duplicated from commented out code above
    #record the time that response actually began
    trial['respBegin'] = experimentTimer.getTime()
    # show fixation cross
    while timer.getTime() > 0:
        fixCross.draw()
        win.flip()

    trial['respEnd'] = experimentTimer.getTime() # should be ~31.25 for the first trial
    # record the answer
    '''
    if chyPos >= -1 and chyPos <= -0.5:
        trial['resp'] = colors[0]
    elif chyPos > -0.5 and chyPos <= 0:
        trial['resp'] = colors[1]
    elif chyPos > 0 and chyPos <= 0.5:
        trial['resp'] = colors[2]
    elif chyPos > 0.5 and chyPos <= 1:
        trial['resp'] = colors[3]
    # Check correctness
    if trial['resp'] == trial['corrAns']:
        trial['correct'] = 1
    '''
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
endText.draw()
win.flip()
event.clearEvents()
while True:
    keys = event.getKeys(keyList = ['escape'])
    if 'escape' in keys:
        win.close()
        core.quit()
        win.flip()

'''
#calcualte RMSE for each trial in trial list, using the distance from target in each frame
#for idx, trial in enumerate(trialList):
#    for idx2, dist in enumerate(distFromTarget):
#        distFromTargetSquared = dist**2
#        trial['sumSquared'] += distFromTargetSquared
#    trialList[idx]['RMSE'] = sqrt(trial['sumSquared']/idx)

for idx, trial in enumerate(trialList):
    trial['maxVal'] = maxVal
    trial['minVal'] = minVal
    distFromTargetSum = 0
    for idx2, dist in enumerate(trial['distFromTarget']):
        distFromTargetSum += abs(dist)
        trial['avgDistFromTarget'] = distFromTargetSum/(idx2+1)
'''
