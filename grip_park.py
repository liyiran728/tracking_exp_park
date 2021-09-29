from psychopy.hardware import joystick
from psychopy import visual, event, core, monitors, gui, misc
import numpy as np
import pandas as pd
import csv
import time
import sys
import os

# ====================================================
# Intro-dialogue. Get subject-id and other variables.
# ====================================================
# Save input variables
V = {'Subject ID':''}
dlg = gui.DlgFromDict(V)
if not dlg.OK:
    sys.exit(0)
# trialfn = os.path.join('trial_info_files',
#                        ''.join((time.strftime('%y%m%d'),V['Subject ID'],'_trialinfo.csv')))
trialfn = os.path.join('trial_info_files',
                       ''.join((V['Subject ID'],'_trialinfo.csv')))
outdir = os.path.join('output_files',''.join((V['Subject ID'],'_',time.strftime('%y%m%d'))))
if not os.path.exists(outdir):
    os.mkdir(outdir)
outfn = os.path.join(outdir,
                     ''.join((V['Subject ID'],'_',time.strftime('%y%m%d'),'.csv')))
effortfn = os.path.join(outdir,
                            ''.join((V['Subject ID'],'_',time.strftime('%y%m%d'),'_effort.csv')))

# check if trial info has been generated
if not os.path.isfile(trialfn):
    print('%s does not exist! Please run create_trial_info.py before running experiment' % trialfn)
    sys.exit(0)

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
#trialInfo = pd.read_csv(trialfn)
numTrials = 10
trialTime = 600 # frames, about 10s
speed = .01
radius = .125
dual = False

locArr = [-0.875, -0.865, -0.855, -0.845, -0.835, -0.825, -0.815, -0.805, -0.795, -0.785, -0.775, -0.765, -0.755, -0.745, -0.735, -0.725, -0.715, -0.705, -0.695, -0.685, -0.675, -0.665, -0.655, -0.645, -0.635, -0.625, -0.615, -0.605, -0.595, -0.585, -0.575, -0.565, -0.555, -0.545, -0.535, -0.525, -0.515, -0.505, -0.495, -0.485, -0.475, -0.465, -0.455, -0.445, -0.435, -0.425, -0.415, -0.405, -0.395, -0.385, -0.375, -0.365, -0.355, -0.345, -0.335, -0.325, -0.315, -0.305, -0.295, -0.285, -0.275, -0.265, -0.255, -0.245, -0.235, -0.225, -0.215, -0.205, -0.195, -0.185, -0.175, -0.165, -0.155, -0.145, -0.135, -0.125, -0.115, -0.105, -0.095, -0.085, -0.075, -0.065, -0.055, -0.045, -0.035, -0.025, -0.015, -0.005, 0.005, 0.015, 0.025, 0.035, 0.045, 0.055, 0.065, 0.075, 0.085, 0.095, 0.105, 0.115, 0.125, 0.135, 0.145, 0.155, 0.165, 0.175, 0.185, 0.195, 0.205, 0.215, 0.225, 0.235, 0.245, 0.255, 0.265, 0.275, 0.285, 0.295, 0.305, 0.315, 0.325, 0.335, 0.345, 0.355, 0.365, 0.375, 0.385, 0.395, 0.405, 0.415, 0.425, 0.435, 0.445, 0.455, 0.465, 0.475, 0.485, 0.495, 0.505, 0.515, 0.525, 0.535, 0.545, 0.555, 0.565, 0.575, 0.585, 0.595, 0.605, 0.615, 0.625, 0.635, 0.645, 0.655, 0.665, 0.675, 0.685, 0.695, 0.705, 0.715, 0.725, 0.735, 0.745, 0.755, 0.765, 0.775, 0.785, 0.795, 0.805, 0.815, 0.825, 0.835, 0.845, 0.855, 0.865, 0.875, 0.865, 0.855, 0.845, 0.835, 0.825, 0.815, 0.805, 0.795, 0.785, 0.775, 0.765, 0.755, 0.745, 0.735, 0.725, 0.715, 0.705, 0.695, 0.685, 0.675, 0.665, 0.655, 0.645, 0.635, 0.625, 0.615, 0.605, 0.595, 0.585, 0.575, 0.565, 0.555, 0.545, 0.535, 0.525, 0.515, 0.505, 0.495, 0.485, 0.475, 0.465, 0.455, 0.445, 0.435, 0.425, 0.415, 0.405, 0.395, 0.385, 0.375, 0.365, 0.355, 0.345, 0.335, 0.325, 0.315, 0.305, 0.295, 0.285, 0.275, 0.265, 0.255, 0.245, 0.235, 0.225, 0.215, 0.205, 0.195, 0.185, 0.175, 0.165, 0.155, 0.145, 0.135, 0.125, 0.115, 0.105, 0.095, 0.085, 0.075, 0.065, 0.055, 0.045, 0.035, 0.025, 0.015, 0.005, -0.005, -0.015, -0.025, -0.035, -0.045, -0.055, -0.065, -0.075, -0.085, -0.095, -0.105, -0.115, -0.125, -0.135, -0.145, -0.155, -0.165, -0.175, -0.185, -0.195, -0.205, -0.215, -0.225, -0.235, -0.245, -0.255, -0.265, -0.275, -0.285, -0.295, -0.305, -0.315, -0.325, -0.335, -0.345, -0.355, -0.365, -0.375, -0.385, -0.395, -0.405, -0.415, -0.425, -0.435, -0.445, -0.455, -0.465, -0.475, -0.485, -0.495, -0.505, -0.515, -0.525, -0.535, -0.545, -0.555, -0.565, -0.575, -0.585, -0.595, -0.605, -0.615, -0.625, -0.635, -0.645, -0.655, -0.665, -0.675, -0.685, -0.695, -0.705, -0.715, -0.725, -0.735, -0.745, -0.755, -0.765, -0.775, -0.785, -0.795, -0.805, -0.815, -0.825, -0.835, -0.845, -0.855, -0.865, -0.875, -0.865, -0.855, -0.845, -0.835, -0.825, -0.815, -0.805, -0.795, -0.785, -0.775, -0.765, -0.755, -0.745, -0.735, -0.725, -0.715, -0.705, -0.695, -0.685, -0.675, -0.665, -0.655, -0.645, -0.635, -0.625, -0.615, -0.605, -0.595, -0.585, -0.575, -0.565, -0.555, -0.545, -0.535, -0.525, -0.515, -0.505, -0.495, -0.485, -0.475, -0.465, -0.455, -0.445, -0.435, -0.425, -0.415, -0.405, -0.395, -0.385, -0.375, -0.365, -0.355, -0.345, -0.335, -0.325, -0.315, -0.305, -0.295, -0.285, -0.275, -0.265, -0.255, -0.245, -0.235, -0.225, -0.215, -0.205, -0.195, -0.185, -0.175, -0.165, -0.155, -0.145, -0.135, -0.125, -0.115, -0.105, -0.095, -0.085, -0.075, -0.065, -0.055, -0.045, -0.035, -0.025, -0.015, -0.005, 0.005, 0.015, 0.025, 0.035, 0.045, 0.055, 0.065, 0.075, 0.085, 0.095, 0.105, 0.115, 0.125, 0.135, 0.145, 0.155, 0.165, 0.175, 0.185, 0.195, 0.205, 0.215, 0.225, 0.235, 0.245, 0.255, 0.265, 0.275, 0.285, 0.295, 0.305, 0.315, 0.325, 0.335, 0.345, 0.355, 0.365, 0.375, 0.385, 0.395, 0.405, 0.415, 0.425, 0.435, 0.445, 0.455, 0.465, 0.475, 0.485, 0.495, 0.505, 0.515, 0.525, 0.535, 0.545, 0.555, 0.565, 0.575, 0.585, 0.595, 0.605, 0.615, 0.625, 0.635, 0.645, 0.655, 0.665, 0.675, 0.685, 0.695, 0.705, 0.715, 0.725, 0.735, 0.745, 0.755, 0.765, 0.775, 0.785, 0.795, 0.805, 0.815, 0.825, 0.835, 0.845, 0.855, 0.865, 0.875, 0.865, 0.855, 0.845, 0.835, 0.825, 0.815, 0.805, 0.795, 0.785, 0.775, 0.765, 0.755, 0.745, 0.735, 0.725, 0.715, 0.705, 0.695, 0.685, 0.675, 0.665, 0.655, 0.645, 0.635, 0.625, 0.615, 0.605, 0.595, 0.585, 0.575, 0.565, 0.555, 0.545, 0.535, 0.525, 0.515, 0.505, 0.495, 0.485, 0.475, 0.465, 0.455, 0.445, 0.435, 0.425, 0.415, 0.405, 0.395, 0.385, 0.375, 0.365, 0.355, 0.345, 0.335, 0.325, 0.315, 0.305, 0.295, 0.285, 0.275, 0.265, 0.255, 0.245, 0.235, 0.225, 0.215, 0.205, 0.195, 0.185, 0.175, 0.165, 0.155, 0.145, 0.135]
colorArr = ["red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red"]

# ==================
# create trial list
# ==================
#trialList = []
#for ii in range(nTrials):
#    trialList.append({'reward': trialInfo['reward'][ii],
#                      'effort': trialInfo['effort'][ii],
#                      'timeToGoal': np.NaN,
#                      'goalReached': 0,
#                      'pctOfGoal': 0,
#                      'amountEarned': np.NaN,
#                      'blockNum': int(trialInfo['block'][ii]),
#                      'startDelay': startDelay[ii]
#                      })

# ===========
# timing info
# ===========
preFix = 1.0
postFix = 1.0
timePrepare = 2.0
timeTrack = 10.0
timeResponse = 3.0
timeOff = 13.0

# ==========================
# window and joystick setup
# ==========================
red = [1,-1,-1]
black = [-1,-1,-1]
blue = [-1,-1,1]
joystick.backend = 'pygame'
testingRoomMonitor = monitors.Monitor('testing_room',distance = 66, width = 52)
testingRoomMonitor.setSizePix((1920,1080))
win = visual.Window([1000,1000],winType = 'pygame',monitor = testingRoomMonitor,
                    units = 'norm',fullscr=False,color = grey)
joy = joystick.Joystick(0)

# =================
# stimulus objects
# =================
target = visual.Circle(win=win, name='target', units='norm', radius=.125,
	fillColor='red', fillColorSpace='rgb', opacity=1, depth=-1.0, interpolate=True)
crosshair = visual.Circle(win=win, name='crosshair', units='norm', radius=.075,
	fillColor='black', fillColorSpace='rgb', opacity=1, depth=0.0, interpolate=True)
fixCross = visual.ShapeStim(win=win, name='polygon', vertices='cross',
	size=(0.05, 0.05), ori=0, pos=(0, 0), lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
	fillColor='black', fillColorSpace='rgb', opacity=1, depth=0.0, interpolate=True)
singleText = visual.TextStim(win=win, text="Single", pos = (0,0), height=.075, color = black)
dualText = visual.TextStim(win=win, text="Dual", pos = (0,0), height=.075, color = black)
startText = visual.TextStim(win=win, text="Experiment Trials", pos = (0,0), height=.075, color = black)
fourCircle = visual.Circle(win=win, name='target', units='norm', radius=.125,
	fillColor='red', fillColorSpace='rgb', opacity=.5, depth=-1.0, pos = (0,0.675), interpolate=True)
threeCircle = visual.Circle(win=win, name='target', units='norm', radius=.125,
	fillColor='red', fillColorSpace='rgb', opacity=.5, depth=-1.0, pos = (0,0.225), interpolate=True)
twoCircle = visual.Circle(win=win, name='target', units='norm', radius=.125,
	fillColor='red', fillColorSpace='rgb', opacity=.5, depth=-1.0, pos = (0,-0.225), interpolate=True)
oneCircle = visual.Circle(win=win, name='target', units='norm', radius=.125,
	fillColor='red', fillColorSpace='rgb', opacity=.5, depth=-1.0, pos = (0,-0.675), interpolate=True)
oneText = visual.TextStim(win=win, text="1", pos = (0,-0.675), height=.125)
twoText = visual.TextStim(win=win, text="2", pos = (0,-0.225), height=.125)
threeText = visual.TextStim(win=win, text="3", pos = (0,0.225), height=.125)
fourText = visual.TextStim(win=win, text="4", pos = (0,0.675), height=.125)

# ======================
# stimulus presentation
# ======================
# create timers
experimentTimer = core.Clock()
timer = core.CountdownTimer()

# Experiment Trial Screen
while experimentTimer.getTime() < 5:
    startText.draw()
    win.flip()

for trialNum in range(1, numTrials+1):
    startTime = experimentTimer.getTIme()
    if trialNum % 2 == 1:
        dual = False
    else:
        dual = True

    if dual == False:
        while experimentTimer.getTime() - startTime < timePrepare:
            target.setPos(0, locArr[0])
            target.draw()
            
