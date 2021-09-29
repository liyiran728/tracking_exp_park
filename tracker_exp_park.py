#tracker.py
#grip sensor version post gsfix
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.90.2),
    on September 17, 2018, at 15:28
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy.hardware import joystick
from psychopy import locale_setup, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, STOPPED, FINISHED, PRESSED)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
import pandas as pd

# read in csv file that has experiment parameters
# ExpDetails = pd.read_csv('path_to_file.csv')
# ExpDetails['dualtask'][blocknum]

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'tracking'  # from the Builder filename that created this script
expInfo = {'session': '001', 'participant': '000'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_ses-%s_%s_%s' % (expInfo['participant'], expInfo['session'], expName, expInfo['date'])

# save a log file for detail verbose info
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# flag for 'escape' or other condition => quit the exp
endExpNow = False

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# Setup the Window
win = visual.Window(size=[650, 650], fullscr=False, screen=0, allowGUI=True, allowStencil=False,
                    monitor='testMonitor', color=[0,0,0], colorSpace='rgb', blendMode='avg', useFBO=True)

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "trial"
trialClock = core.Clock()
x, y = [None, None]
target = visual.Circle(win=win, name='target', units='norm', radius=.125,
	fillColor='red', fillColorSpace='rgb', opacity=1, depth=-1.0, interpolate=True)
crosshair = visual.Circle(win=win, name='crosshair', units='norm', radius=.075,
	#size=(0.075, 0.075), ori=0, pos=(0, 0), lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
	fillColor='black', fillColorSpace='rgb', opacity=1, depth=0.0, interpolate=True)

# set up joystick
joystick.backend = 'pyglet'
nJoys = joystick.getNumJoysticks()
joy = joystick.Joystick(0)
joy.status = NOT_STARTED

# setup some python lists for storing info about the mouse-- NOTE: distance measures from crosshair center to closest edge of target!
mousey, targetx, targety, distance, yDistance, onTarget, rmse, trialList, blockList, subject, onTargetPercent, pctYOff, numFramesInTarget = ([] for i in range(13))

# variables
numTrials = 128
trialTime = 600 # frames, about 10s
speed = .01
radius = .125
dual = False
locArr = [-0.875, -0.865, -0.855, -0.845, -0.835, -0.825, -0.815, -0.805, -0.795, -0.785, -0.775, -0.765, -0.755, -0.745, -0.735, -0.725, -0.715, -0.705, -0.695, -0.685, -0.675, -0.665, -0.655, -0.645, -0.635, -0.625, -0.615, -0.605, -0.595, -0.585, -0.575, -0.565, -0.555, -0.545, -0.535, -0.525, -0.515, -0.505, -0.495, -0.485, -0.475, -0.465, -0.455, -0.445, -0.435, -0.425, -0.415, -0.405, -0.395, -0.385, -0.375, -0.365, -0.355, -0.345, -0.335, -0.325, -0.315, -0.305, -0.295, -0.285, -0.275, -0.265, -0.255, -0.245, -0.235, -0.225, -0.215, -0.205, -0.195, -0.185, -0.175, -0.165, -0.155, -0.145, -0.135, -0.125, -0.115, -0.105, -0.095, -0.085, -0.075, -0.065, -0.055, -0.045, -0.035, -0.025, -0.015, -0.005, 0.005, 0.015, 0.025, 0.035, 0.045, 0.055, 0.065, 0.075, 0.085, 0.095, 0.105, 0.115, 0.125, 0.135, 0.145, 0.155, 0.165, 0.175, 0.185, 0.195, 0.205, 0.215, 0.225, 0.235, 0.245, 0.255, 0.265, 0.275, 0.285, 0.295, 0.305, 0.315, 0.325, 0.335, 0.345, 0.355, 0.365, 0.375, 0.385, 0.395, 0.405, 0.415, 0.425, 0.435, 0.445, 0.455, 0.465, 0.475, 0.485, 0.495, 0.505, 0.515, 0.525, 0.535, 0.545, 0.555, 0.565, 0.575, 0.585, 0.595, 0.605, 0.615, 0.625, 0.635, 0.645, 0.655, 0.665, 0.675, 0.685, 0.695, 0.705, 0.715, 0.725, 0.735, 0.745, 0.755, 0.765, 0.775, 0.785, 0.795, 0.805, 0.815, 0.825, 0.835, 0.845, 0.855, 0.865, 0.875, 0.865, 0.855, 0.845, 0.835, 0.825, 0.815, 0.805, 0.795, 0.785, 0.775, 0.765, 0.755, 0.745, 0.735, 0.725, 0.715, 0.705, 0.695, 0.685, 0.675, 0.665, 0.655, 0.645, 0.635, 0.625, 0.615, 0.605, 0.595, 0.585, 0.575, 0.565, 0.555, 0.545, 0.535, 0.525, 0.515, 0.505, 0.495, 0.485, 0.475, 0.465, 0.455, 0.445, 0.435, 0.425, 0.415, 0.405, 0.395, 0.385, 0.375, 0.365, 0.355, 0.345, 0.335, 0.325, 0.315, 0.305, 0.295, 0.285, 0.275, 0.265, 0.255, 0.245, 0.235, 0.225, 0.215, 0.205, 0.195, 0.185, 0.175, 0.165, 0.155, 0.145, 0.135, 0.125, 0.115, 0.105, 0.095, 0.085, 0.075, 0.065, 0.055, 0.045, 0.035, 0.025, 0.015, 0.005, -0.005, -0.015, -0.025, -0.035, -0.045, -0.055, -0.065, -0.075, -0.085, -0.095, -0.105, -0.115, -0.125, -0.135, -0.145, -0.155, -0.165, -0.175, -0.185, -0.195, -0.205, -0.215, -0.225, -0.235, -0.245, -0.255, -0.265, -0.275, -0.285, -0.295, -0.305, -0.315, -0.325, -0.335, -0.345, -0.355, -0.365, -0.375, -0.385, -0.395, -0.405, -0.415, -0.425, -0.435, -0.445, -0.455, -0.465, -0.475, -0.485, -0.495, -0.505, -0.515, -0.525, -0.535, -0.545, -0.555, -0.565, -0.575, -0.585, -0.595, -0.605, -0.615, -0.625, -0.635, -0.645, -0.655, -0.665, -0.675, -0.685, -0.695, -0.705, -0.715, -0.725, -0.735, -0.745, -0.755, -0.765, -0.775, -0.785, -0.795, -0.805, -0.815, -0.825, -0.835, -0.845, -0.855, -0.865, -0.875, -0.865, -0.855, -0.845, -0.835, -0.825, -0.815, -0.805, -0.795, -0.785, -0.775, -0.765, -0.755, -0.745, -0.735, -0.725, -0.715, -0.705, -0.695, -0.685, -0.675, -0.665, -0.655, -0.645, -0.635, -0.625, -0.615, -0.605, -0.595, -0.585, -0.575, -0.565, -0.555, -0.545, -0.535, -0.525, -0.515, -0.505, -0.495, -0.485, -0.475, -0.465, -0.455, -0.445, -0.435, -0.425, -0.415, -0.405, -0.395, -0.385, -0.375, -0.365, -0.355, -0.345, -0.335, -0.325, -0.315, -0.305, -0.295, -0.285, -0.275, -0.265, -0.255, -0.245, -0.235, -0.225, -0.215, -0.205, -0.195, -0.185, -0.175, -0.165, -0.155, -0.145, -0.135, -0.125, -0.115, -0.105, -0.095, -0.085, -0.075, -0.065, -0.055, -0.045, -0.035, -0.025, -0.015, -0.005, 0.005, 0.015, 0.025, 0.035, 0.045, 0.055, 0.065, 0.075, 0.085, 0.095, 0.105, 0.115, 0.125, 0.135, 0.145, 0.155, 0.165, 0.175, 0.185, 0.195, 0.205, 0.215, 0.225, 0.235, 0.245, 0.255, 0.265, 0.275, 0.285, 0.295, 0.305, 0.315, 0.325, 0.335, 0.345, 0.355, 0.365, 0.375, 0.385, 0.395, 0.405, 0.415, 0.425, 0.435, 0.445, 0.455, 0.465, 0.475, 0.485, 0.495, 0.505, 0.515, 0.525, 0.535, 0.545, 0.555, 0.565, 0.575, 0.585, 0.595, 0.605, 0.615, 0.625, 0.635, 0.645, 0.655, 0.665, 0.675, 0.685, 0.695, 0.705, 0.715, 0.725, 0.735, 0.745, 0.755, 0.765, 0.775, 0.785, 0.795, 0.805, 0.815, 0.825, 0.835, 0.845, 0.855, 0.865, 0.875, 0.865, 0.855, 0.845, 0.835, 0.825, 0.815, 0.805, 0.795, 0.785, 0.775, 0.765, 0.755, 0.745, 0.735, 0.725, 0.715, 0.705, 0.695, 0.685, 0.675, 0.665, 0.655, 0.645, 0.635, 0.625, 0.615, 0.605, 0.595, 0.585, 0.575, 0.565, 0.555, 0.545, 0.535, 0.525, 0.515, 0.505, 0.495, 0.485, 0.475, 0.465, 0.455, 0.445, 0.435, 0.425, 0.415, 0.405, 0.395, 0.385, 0.375, 0.365, 0.355, 0.345, 0.335, 0.325, 0.315, 0.305, 0.295, 0.285, 0.275, 0.265, 0.255, 0.245, 0.235, 0.225, 0.215, 0.205, 0.195, 0.185, 0.175, 0.165, 0.155, 0.145, 0.135]
colorArr = ["red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red", "red"]

#add RMEs
def jsCalc(joyPos, val):
    CORNER = .99
    val = 0.9*(val+1) - 1 #relax the grip a bit
    scaleFactor = 2*CORNER / (val+1)
    pos = (abs(joyPos+1)*scaleFactor) - CORNER
    #magic num 2.75 is what fits the screen box; joyPos ranges between -1 and val; pos should range between -CORNER and CORNER
    if pos < -CORNER:
        pos = -CORNER
    if pos > CORNER:
        pos = CORNER
    return pos

def caliScreen():
    spacebar = event.BuilderKeyResponse()

    # calibration
    continueRoutine = True
    force_vals = np.array([])
    calibration_text = visual.TextStim(win=win,text="Squeeze the Left sensor as hard as you comfortably can\nPress Space bar when done",
                                   height = 0.1)
    while continueRoutine:
        force_vals = np.append(force_vals,joy.getX())
        calibration_text.draw()
        keysPressed = event.getKeys(keyList=['space'])
        if len(keysPressed) > 0:
            continueRoutine = False
        win.flip()
    xval = np.max(force_vals[force_vals != 0.0])

    continueRoutine = True
    force_vals = np.array([])
    calibration_text.text = "Now squeeze the Right sensor as hard as you comfortably can\nPress Space bar when done"
    while continueRoutine:
        force_vals = np.append(force_vals,joy.getY())
        calibration_text.draw()
        keysPressed = event.getKeys(keyList=['space'])
        if len(keysPressed) > 0:
            continueRoutine = False
        win.flip()
    yval = np.max(force_vals[force_vals != 0.0])

    return xval, yval

def responseScreen():
    #text = visual.TextStim(win=win, text=display, height=.075)
    #text.setAutoDraw(True)
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    fourcircle = visual.Circle(win=win, name='target', units='norm', radius=.125,
    	fillColor='red', fillColorSpace='rgb', opacity=.5, depth=-1.0, pos = (0,0.675), interpolate=True)
    threecircle = visual.Circle(win=win, name='target', units='norm', radius=.125,
    	fillColor='red', fillColorSpace='rgb', opacity=.5, depth=-1.0, pos = (0,0.225), interpolate=True)
    twocircle = visual.Circle(win=win, name='target', units='norm', radius=.125,
    	fillColor='red', fillColorSpace='rgb', opacity=.5, depth=-1.0, pos = (0,-0.225), interpolate=True)
    onecircle = visual.Circle(win=win, name='target', units='norm', radius=.125,
    	fillColor='red', fillColorSpace='rgb', opacity=.5, depth=-1.0, pos = (0,-0.675), interpolate=True)
    onetext = visual.TextStim(win=win, text="1", pos = (0,-0.675), height=.125)
    twotext = visual.TextStim(win=win, text="2", pos = (0,-0.225), height=.125)
    threetext = visual.TextStim(win=win, text="3", pos = (0,0.225), height=.125)
    fourtext = visual.TextStim(win=win, text="4", pos = (0,0.675), height=.125)
    # keep track of which components have finished
    trialComponents = [joy]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    timer = clock.CountdownTimer(3)
    while timer.getTime() > 0:
        # crosshair updates
        chyPos = jsCalc(joy.getY(), yval)
        crosshair.setPos((0, chyPos))
        crosshair.setAutoDraw(True)
        onecircle.setAutoDraw(True)
        twocircle.setAutoDraw(True)
        threecircle.setAutoDraw(True)
        fourcircle.setAutoDraw(True)
        onetext.setAutoDraw(True)
        twotext.setAutoDraw(True)
        threetext.setAutoDraw(True)
        fourtext.setAutoDraw(True)
        win.flip()
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
    #calculate answer
    chyPos = jsCalc(joy.getY(), yval)
    dualAns = ""
    if chyPos >= -0.8 and chyPos <= -0.55:
        dualAns = "1"
    elif chyPos >= -0.35 and chyPos <= -0.1:
        dualAns = "2"
    elif chyPos >= 0.1 and chyPos <= 0.35:
        dualAns = "3"
    elif chyPos >= 0.55 and chyPos <= 0.8:
        dualAns = "4"

    crosshair.setAutoDraw(False)
    onecircle.setAutoDraw(False)
    twocircle.setAutoDraw(False)
    threecircle.setAutoDraw(False)
    fourcircle.setAutoDraw(False)
    onetext.setAutoDraw(False)
    twotext.setAutoDraw(False)
    threetext.setAutoDraw(False)
    fourtext.setAutoDraw(False)
    win.flip()

def holdScreen(display):
    text = visual.TextStim(win=win, text=display, height=.075)
    text.setAutoDraw(True)
    crosshair.setAutoDraw(True)
    spacebar = event.BuilderKeyResponse()
    continueRoutine = True

    # keep track of which components have finished
    trialComponents = [text, joy, spacebar]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    while continueRoutine:
        # crosshair updates
        chyPos = jsCalc(joy.getY(), yval)
        crosshair.setPos((0, chyPos))
        keysPressed = event.getKeys(keyList=['space'])
        win.flip()
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        if len(keysPressed) > 0:
            continueRoutine = False

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

    text.setAutoDraw(False)
    crosshair.setAutoDraw(False)
    win.flip()

def infoScreen(display):
    text = visual.TextStim(win=win, text=display, height=.075)
    text.setAutoDraw(True)
    endExpNow = False  # flag for 'escape' or other condition => quit the exp

    # keep track of which components have finished
    trialComponents = [text, joy]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    timer = clock.CountdownTimer(3)
    while timer.getTime() > 0:
        # crosshair updates
        chyPos = jsCalc(joy.getY(), yval)
        crosshair.setPos((0, chyPos))
        crosshair.setAutoDraw(True)
        win.flip()
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
    text.setAutoDraw(False)
    crosshair.setAutoDraw(False)
    win.flip()

def trialScreen(trialNum, dual, startPos):
    endExpNow = False  # flag for 'escape' or other condition => quit the exp

    #create visual objects
    #might change in the future
    if dual == False:
        trialText = "Single"
    else:
        trialText = "Dual"
    text = visual.TextStim(win=win, text=trialText, height=0.075)
    #***replace it with target***
    copy = visual.Circle(win=win, name='copy', units='norm', radius=.125,
    	fillColor='red', fillColorSpace='rgb', opacity=1, depth=-1.0, interpolate=True)
    copy.setPos((0, startPos))
    copy.setAutoDraw(True)
    crosshair.setAutoDraw(True)

    t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # keep track of which components have finished
    trialComponents = [text, joy]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

# -------Start Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is 1st frame)

        if frameN > 120:
            copy.setAutoDraw(False)
            continueRoutine = False

        # *text* updates
        if t >= 0.0 and text.status == NOT_STARTED:
            text.setAutoDraw(True)

        # crosshair updates
        chyPos = jsCalc(joy.getY(), yval)
        crosshair.setPos((0, chyPos))
        crosshair.setAutoDraw(True)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            text.setAutoDraw(False)
            win.flip()
            break

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if routine is over or you get a blank screen
            win.flip()

def runTrial(trialNum, locArr, colorArr, dual):
    # ------Prepare to start Routine "trial"-------
    #set up some variables
    trialDist = []

    continueRoutine = True
    framesInTarget = 0
    target.setAutoDraw(True)

    # -------Start Routine "trial"-------
    for frameN in range(0,trialTime):
        # crosshair updates
        chyPos = jsCalc(joy.getY(), yval)
        crosshair.setPos((0, chyPos))
        crosshair.setAutoDraw(True)
        # x position is always 0, y updates to the next value in the array
        currX = 0
        currY = locArr[frameN]
        target.setPos((currX, currY))
        if dual == True:
            target.setColor(colorArr[frameN])


        # save frame information
        trialList.append(trialNum)
        mousey.append(chyPos)
        subject.append(expInfo['participant'])
        yDist = chyPos - currY
        #hypotenuse = sqrt( abs(xDist*xDist) + abs(yDist*yDist) )
        yDistance.append(yDist)
        #distance.append(hypotenuse-radius)  #this will be included in the csv output
        #trialDist.append(hypotenuse)    #this is used to compute RMSE
        if abs(yDist) <= radius:
            framesInTarget += 1
            onTarget.append(1)
        else:
            onTarget.append(0)

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #presents trial feedback
    pct = (framesInTarget/(frameN+1))*100
    residual2Sum = 0
    pctX = 0 # this is % NOT in target
    pctY = 0 # this is % NOT in target
    # what is residual2Sum measuring
    #for num in zip(xDistance[-1*trialTime:], yDistance[-1*trialTime:], trialDist[-1*trialTime:]):
    #    residual2Sum += num[2]*num[2]
    #    if abs(num[0]) > radius:
    #        pctX += 1
    #    if abs(num[1]) > radius:
    #        pctY += 1
    #pctX = (pctX/(frameN+1))*100 # LEFT HAND
    #pctY = (pctY/(frameN+1))*100 # RIGHT HAND
    #rootMeanSquaredError = sqrt(residual2Sum)
    target.setAutoDraw(False)

    for i in range(0, frameN+1):
        onTargetPercent.append(pct)
        #pctXOff.append(pctX)
        pctYOff.append(pctY)
        #rmse.append(rootMeanSquaredError)
        numFramesInTarget.append(framesInTarget)

def offScreen(offTime):
    fixCross = visual.ShapeStim(win=win, name='polygon', vertices='cross',
	size=(0.05, 0.05), ori=0, pos=(0, 0), lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
	fillColor='black', fillColorSpace='rgb', opacity=1, depth=0.0, interpolate=True)
    fixCross.setAutoDraw(True)
    crosshair.setAutoDraw(False)
    timer = clock.CountdownTimer(offTime)
    while timer.getTime() > 0:
        win.flip()
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
    fixCross.setAutoDraw(False)
    crosshair.setAutoDraw(True)


def runExp():
    for trialNum in range (1,numTrials+1):
        # Determine the type of task: single or dual
        if trialNum%2 == 1:
            dual = False
        else:
            dual = True
        trialScreen(trialNum, dual, locArr[0])
        runTrial(trialNum, locArr, colorArr, dual)
        responseScreen()
        offScreen(13)

def main():
    # variables
    numTrials = 128
    trialTime = 600 # frames, about 10s
    speed = .01
    radius = .125

    # sandbox happens first
    holdScreen('Use this screen to experiment with moving the crosshairs.')

    # then experiment blocks
    infoScreen('EXPERIMENT TRIALS')
    runExp()

    # Data structure-- NOTE: distance measures from crosshair center to closest edge of target!
    data = pd.DataFrame({'mouseX': mousex, 'mouseY': mousey, 'targetX': targetx, 'targetY': targety,
                        'distance': distance, 'yDist': yDistance,
                        'onTarget': onTarget, 'onTargetPercent': onTargetPercent, 'rmse': rmse,
                        'framesInTarget': numFramesInTarget, 'pctY': pctYOff,
                        'trialList': trialList, 'blockList': blockList,
                        'subject': subject})
    data.to_csv(filename + '.csv')

    # final screen and quit
    holdScreen('You have completed the experiment.\nPlease notify the experimenter.')
    logging.flush()
    win.close()
    core.quit()

# calibrate the movement of the crosshair
xval, yval = caliScreen()
print(xval, yval)
# run the experiment
main()
