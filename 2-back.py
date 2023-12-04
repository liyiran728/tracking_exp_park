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

# ====================================================
# Intro-dialogue. Get subject-id and other variables.
# ====================================================
# Save input variables
expName = 'N_Back'
expInfo = {'Subject ID':'', 'Day':'', 'TMS Site':''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)

if not dlg.OK:
    sys.exit(0)
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
outfn = 'output_files_n_back/%s_Day%s_%s.csv' % (expInfo['Subject ID'], expInfo['Day'], expInfo['TMS Site'])

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
numTrials = 16
numColors = 12
colors = ["red", "yellow", "blue", "green"]

# ==================
# create trial list
# ==================
colorAll = []
answerAll = []
for i in range(numTrials):
    colorArray = []
    last = -1
    for ii in range(numColors):
        num = random.randint(0, 3)
        while (num == last):
            num = random.randint(0, 3)
        colorArray.append(colors[num])
        last = num
    compareArray = ["",""]
    for j in range(numColors-2):
        compareArray.append(colorArray[j])
    answerArray = []
    for k in range(numColors):
        if(colorArray[k] == compareArray[k]):
            answerArray.append(1)
        else:
            answerArray.append(0)
    colorAll += colorArray
    answerAll += answerArray
print(colorAll)
print(answerAll)

trialList = []
for i in range(numTrials):
    for j in range(numColors):
        trialList.append({'trial': i+1,
                          'stim': j+1,
                          'color': colorAll[i*numColors+j],
                          'answer':answerAll[i*numColors+j],
                          'response_L':0,
                          'response_R':0,
                          'correct':0,
                          'reactionTime':0
                          })
# ===========
# timing info
# ===========
timeOn = 12
timeOff = 6

# ==========================
# window and grip sensor setup
# ==========================
red = [1,-1,-1]
black = [-1,-1,-1]
blue = [-1,-1,1]
grey = [0.15,0.15,0.15]
joystick.backend = 'pygame'
testingRoomMonitor = monitors.Monitor('testing_room',distance = 66, width = 52)
testingRoomMonitor.setSizePix((1920,1080))
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
fixCross = visual.ShapeStim(win=win, name='polygon', vertices='cross',
	size=(0.1, 0.1), ori=0, pos=(0, 0), lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
	fillColor='white', fillColorSpace='rgb', opacity=1, depth=0.0, interpolate=True)
yesText = visual.TextStim(win=win, text="Yes", pos = (-0.6,0), height=.2)
noText = visual.TextStim(win=win, text="No", pos = (0.6,0), height=.2)
endText = visual.TextStim(win=win, text="End of Experiment\n\nEsc to exit", pos = (0,0), height=.2)


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
force_vals_x = np.array([])
force_vals_y = np.array([])
while timer.getTime() > 0:
    force_vals_x = np.append(force_vals_x,joy.getX())
    force_vals_y = np.append(force_vals_y,joy.getY())
    countdownText.text = '%d' % int(np.ceil(timer.getTime()))
    countdownText.draw()
    calibration_text.draw()
    win.flip()

timer.reset(3)
calibration_text.text = "Now squeeze sensors as hard as you can"
while timer.getTime() > 0:
    force_vals_x = np.append(force_vals_x,joy.getX())
    force_vals_y = np.append(force_vals_y,joy.getY())
    countdownText.text = '%d' % int(np.ceil(timer.getTime()))
    countdownText.draw()
    calibration_text.draw()
    win.flip()
maxVal_y = np.max(force_vals_y[force_vals_y != 0.0])
minVal_y = np.min(force_vals_y[force_vals_y != 0.0])
maxVal_x = np.max(force_vals_x[force_vals_x != 0.0])
minVal_x = np.min(force_vals_x[force_vals_x != 0.0])

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
for trialn in range(numTrials):
    timer.reset(timeOff)
    while timer.getTime() > 0:
        fixCross.draw()
        win.flip()
    for stim in range(numColors):
        index = trialn*numColors + stim
        trial = trialList[index]
        #x = trial['answer']
        target.setColor(colorAll[index])
        timer.reset(1)
        target.draw()
        yesText.draw()
        noText.draw()
        win.flip()
        while timer.getTime() > 0:
            if (joy.getX() > (maxVal_x - minVal_x)*0.1) and (trial['reactionTime'] == 0):
                # set yes for left
                trial['response_L'] = 1
                #record reaction time 1-get time
                trial['reactionTime'] = 1-timer.getTime()
                target.draw()
                yesText.draw()
                win.flip()
            if (joy.getY() > (maxVal_y - minVal_y)*0.1) and (trial['reactionTime'] == 0):
                # set yes for right
                trial['response_R'] = 1
                #record reaction time 1-get time
                trial['reactionTime'] = 1-timer.getTime()
                target.draw()
                noText.draw()
                win.flip()
        if (trial['response_L'] == 1 and trial['response_R'] == 0 and trial['answer'] == 1):
            trial['correct'] = 1
        elif (trial['response_L'] == 0 and trial['response_R'] == 1 and trial['answer'] == 0):
            trial['correct'] = 1

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
