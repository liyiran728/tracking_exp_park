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
	fillColor=[1,-1,-1], fillColorSpace='rgb', opacity=.5, depth=-1.0, interpolate=True)
crosshair = visual.ShapeStim(win=win, name='polygon', vertices='cross',
	size=(0.075, 0.075), ori=0, pos=(0, 0), lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
	fillColor=[-1.000,-1.000,-1.000], fillColorSpace='rgb', opacity=1, depth=0.0, interpolate=True)

# set up joystick
joystick.backend = 'pyglet'
nJoys = joystick.getNumJoysticks()
joy = joystick.Joystick(0)
joy.status = NOT_STARTED

# setup some python lists for storing info about the mouse-- NOTE: distance measures from crosshair center to closest edge of target!
mousex, mousey, targetx, targety, distance, xDistance, yDistance, onTarget, rmse, ori, dir, trialList, blockList, condList, subject, onTargetPercent, pctXOff, pctYOff, numFramesInTarget = ([] for i in range(19))

# variables
numTrials = 128
trialTime = 600 # frames, about 10s
speed = .01
radius = .125

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
        chxPos = jsCalc(joy.getX(), xval)
        chyPos = jsCalc(joy.getY(), yval)
        crosshair.setPos((chxPos, chyPos))
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
        chxPos = jsCalc(joy.getX(), xval)
        chyPos = jsCalc(joy.getY(), yval)
        crosshair.setPos((chxPos, chyPos))
        crosshair.setAutoDraw(True)
        win.flip()
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
    text.setAutoDraw(False)
    crosshair.setAutoDraw(False)
    win.flip()

def trialScreen(trialNum, origin, direction):
    endExpNow = False  # flag for 'escape' or other condition => quit the exp

    #create visual objects
    #might change in the future
    trialName = 'Trial ' + str(trialNum)
    if trialNum > 800:
        trialName = 'Training Trial ' + str(trialNum%10)
    text = visual.TextStim(win=win, text=trialName, height=0.075)
    #***replace it with target***
    #copy = visual.Circle(win=win, units='norm', radius=.125, fillColor=[1,-1,-1],
    #    fillColorSpace='rgb', opacity=0, depth=-1.0, interpolate=True)

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
            continueRoutine = False

        # *text* updates
        if t >= 0.0 and text.status == NOT_STARTED:
            text.setAutoDraw(True)

        # crosshair updates
        chxPos = jsCalc(joy.getX(), xval)
        chyPos = jsCalc(joy.getY(), yval)
        crosshair.setPos((chxPos, chyPos))
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
