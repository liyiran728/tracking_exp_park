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
win = visual.Window(size=[550, 550], fullscr=False, screen=0, allowGUI=True, allowStencil=False,
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
	size=(0.025, 0.025), ori=0, pos=(0, 0), lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
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

internalInst = "Make sure to pay attention to how hard you grip the sensors.\n\nNote whether you are squeezing too hard/little with each of your hands."
externalInst = "Make sure to pay attention to the location of your crosshair.\n\nNote whether you are off in the vertical or horizontal direction more often"

# Even subjects are external
external = False
if int(expInfo["participant"])%2 == 0:
    external = True

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

def setIndicator(origin, direction):
    UP = 270
    DOWN = 90
    LEFT = 180
    RIGHT = 0
    NW = 225
    NE = 315
    SE = 45
    SW = 135

    if origin == 1:
        pos = (0,.75)
        if direction == 'CW':
            ori = SE
        elif direction == 'CC':
            ori = SW
        elif direction == 'VT':
            ori = DOWN

    if origin == 2:
        pos = (.75,0)
        if direction == 'CW':
            ori = SW
        elif direction == 'CC':
            ori = NW
        elif direction == 'HZ':
            ori = LEFT

    if origin == 3:
        pos = (0,-.75)
        if direction == 'CW':
            ori = NW
        elif direction == 'CC':
            ori = NE
        elif direction == 'VT':
            ori = UP

    if origin == 4:
        pos = (-.75,0)
        if direction == 'CW':
            ori = NE
        elif direction == 'CC':
            ori = SE
        elif direction == 'HZ':
            ori = RIGHT

    return pos, ori

def trialScreen(trialNum, origin, direction):
    endExpNow = False  # flag for 'escape' or other condition => quit the exp

    #create visual objects
    indicator = visual.TextStim(win=win, text='>', height=.25)
    trialName = 'Trial ' + str(trialNum)
    if trialNum > 800:
        trialName = 'Training Trial ' + str(trialNum%10)
    text = visual.TextStim(win=win, text=trialName, height=0.075)
    copy = visual.Circle(win=win, units='norm', radius=.125, fillColor=[1,-1,-1],
        fillColorSpace='rgb', opacity=0, depth=-1.0, interpolate=True)
    indicator.pos, indicator.ori = setIndicator(origin, direction)

    t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # keep track of which components have finished
    trialComponents = [text, indicator, joy]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is 1st frame)

        # *text* updates
        if t >= 0.0 and text.status == NOT_STARTED:
            text.setAutoDraw(True)

        # *indicator* updates
        if t >= 0.0 and indicator.status == NOT_STARTED:
            indicator.setAutoDraw(True)

        # crosshair updates
        chxPos = jsCalc(joy.getX(), xval)
        chyPos = jsCalc(joy.getY(), yval)
        crosshair.setPos((chxPos, chyPos))
        crosshair.setAutoDraw(True)

        #check for crosshair positioning
        copy.pos = indicator.pos
        if crosshair.overlaps(copy):
            continueRoutine = False

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            text.setAutoDraw(False)
            indicator.setAutoDraw(False)
            win.flip()
            break

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if routine is over or you get a blank screen
            win.flip()

def runTraining():
    #movement:
    # _______________
    # |      1      |
    # |             |
    # |  4       2  |
    # |             |
    # |      3      |
    # |_____________|
    #CW is clockwise
    #CC is counter-clockwise
    #VT is vertical (training only)
    #HZ is horizontal (training only)

    if external:
        holdScreen(externalInst)
    else:
        holdScreen(internalInst)
    #bottom VT
    trialScreen(901, 3, 'VT')
    pctX, pctY = runTrial(901, 3, 'VT', 0, external)
    displayFeedback(external, pctX, pctY)
    #left HZ
    trialScreen(902, 4, 'HZ')
    runTrial(902, 4, 'HZ', 0, external)
    
    if external:
        infoScreen(externalInst)
    else:
        infoScreen(internalInst)
    #top VT
    trialScreen(803, 1, 'VT')
    pctX, pctY = runTrial(803, 1, 'VT', 0, external)
    displayFeedback(external, pctX, pctY)
    #right HZ
    trialScreen(804, 2, 'HZ')
    runTrial(804, 2, 'HZ', 0, external)
    
    if external:
        infoScreen(externalInst)
    else:
        infoScreen(internalInst)
    #top CW
    trialScreen(905, 1, 'CW')
    pctX, pctY = runTrial(905, 1, 'CW', 0, external)
    displayFeedback(external, pctX, pctY)
    #left CC
    trialScreen(906, 4, 'CC')
    runTrial(906, 4, 'CC', 0, external)
    
    if external:
        infoScreen(externalInst)
    else:
        infoScreen(internalInst)
    #bottom CW
    trialScreen(807, 3, 'CW')
    pctX, pctY = runTrial(807, 3, 'CW', 0, external)
    displayFeedback(external, pctX, pctY)
    #right CC
    trialScreen(808, 2, 'CC')
    runTrial(808, 2, 'CC', 0, external)

def runMiniBlock(miniBlock, external, blockNum):
    infoScreen("Block {}".format(blockNum))

    if external:
        infoScreen(externalInst)
    else:
        infoScreen(internalInst)

    totalX = 0
    totalY = 0
    for i, trial in enumerate(miniBlock):
        trialScreen((blockNum*4)+i-3, trial['ori'], trial['dir'])
        pctX, pctY = runTrial((blockNum*4)+i-3, trial['ori'], trial['dir'], blockNum, external)
        totalX += pctX
        totalY += pctY
    
    displayFeedback(external, totalX/4, totalY/4)

def displayFeedback(external, pctX, pctY):
    perfect = False
    if pctX > pctY:
        hand = "Your LEFT hand was"
        vH = "the HORIZONTAL direction"
        pctOff = pctX
    elif pctY > pctX:
        hand = "Your RIGHT hand was"
        vH = "the VERTICAL direction"
        pctOff = pctY
    else:
        if pctX == 0 and pctY == 0:
            perfect = True
        hand = "Both your hands were"
        vH = "both directions"
        pctOff = pctX
    pctOff = round(pctOff)
    if pctOff == 0:
        pctOff = "<1"

    if external:
        if perfect:
            tendency = visual.TextStim(win=win, text = "The crosshair stayed in the target the whole time!")
        else:
            tendency = visual.TextStim(win=win, text = "You were off {}% of the time in {}.".format(pctOff, vH))
    else:
        if perfect:
            tendency = visual.TextStim(win=win, text = "Both your hands squeezed the perfect amount!")
        else:
            tendency = visual.TextStim(win=win, text = "{} off {}% of the time".format(hand, pctOff))

    tendency.setAutoDraw(True)
    timer = clock.CountdownTimer(5)
    while timer.getTime() > 0:
        win.flip()
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
    tendency.setAutoDraw(False)

def runExp():
    params = []
    for num in range(1,5):
        params.append({'ori':num, 'dir':'CW'})
        params.append({'ori':num, 'dir':'CC'})

    #setup TrialHandler
    trials = data.TrialHandler(params, int(numTrials/8), method='random') #this 8 is the number of params

    miniBlocks = []
    blockNum = 1

    for i, trial in enumerate(trials):
        miniBlocks.append(trial)
        if len(miniBlocks) % 4 == 0:
            runMiniBlock(miniBlocks, external, blockNum)
            miniBlocks = []
            blockNum += 1

def setTargetMotion(origin, direction):
    moveRight = True
    moveUp = True
    currX = 0
    currY = 0
    prevX = 0
    prevY = 0

    #set origin and direction
    #top
    if origin == 1:
        moveUp = False
        currY = 1
        prevY = 1 - radius
        if direction == 'CW':
            moveUp = False
        if direction == 'CC':
            moveRight = False
            moveUp = False
        if direction == 'VT':
            moveUp = False

    #right
    if origin == 2:
        currX = 1
        prevX = 1 - radius
        if direction == 'CW':
            moveRight = False
            moveUp = False
        if direction == 'CC':
            moveRight = False
        if direction == 'HZ':
            moveRight = False

    #bottom
    if origin == 3:
        currY = -1
        prevY = -1 + radius
        if direction == 'CW':
            moveRight = False
        if direction == 'CC':
            moveUp = False

    #left
    if origin == 4:
        currX = -1
        prevX = -1 + radius
        if direction == 'CC':
            moveUp = False

    return moveRight, moveUp, currX, currY, prevX, prevY

def runTrial(trialNum, origin, direction, blockNum, external):
    # ------Prepare to start Routine "trial"-------
    #set up some variables
    trialDist = []

    continueRoutine = True
    framesInTarget = 0

    moveRight, moveUp, currX, currY, prevX, prevY = setTargetMotion(origin, direction)

    # -------Start Routine "trial"-------
    for frameN in range(0,trialTime):
        target.setAutoDraw(True)

        # crosshair updates
        chxPos = jsCalc(joy.getX(), xval)
        chyPos = jsCalc(joy.getY(), yval)
        crosshair.setPos((chxPos, chyPos))
        crosshair.setAutoDraw(True)

        #currX, currY set the general motion of the target
        #i.e. moves down, moves diagonally up and right, etc.
        #sets horizontal motion (all motion patterns EXCEPT VT)
        if direction != 'VT':
            if moveRight:
                currX = currX + speed
            else:
                currX = currX - speed

        #sets vertical motion (all motion patterns EXCEPT HZ)
        if direction != 'HZ':
            if moveUp:
                currY = currY + speed
            else:
                currY = currY - speed

        #changing curr to new makes the motion smooth
        newX = sin(currX)
        newY = sin(currY)

        # prevents target from going off the screen
        if newX < -1 + radius:
            moveRight = True
        if newX > 1 - radius:
            moveRight = False
        if newY < -1 + radius:
            moveUp = True
        if newY > 1 - radius:
            moveUp = False

        target.setPos((newX, newY))

        # save frame information
        blockList.append(blockNum)
        condList.append(external)
        trialList.append(trialNum)
        ori.append(origin)
        dir.append(direction)
        mousex.append(chxPos)
        mousey.append(chyPos)
        subject.append(expInfo['participant'])
        xDist = chxPos - prevX
        yDist = chyPos - prevY
        hypotenuse = sqrt( abs(xDist*xDist) + abs(yDist*yDist) )
        xDistance.append(xDist)
        yDistance.append(yDist)
        distance.append(hypotenuse-radius)  #this will be included in the csv output
        trialDist.append(hypotenuse)    #this is used to compute RMSE
        if max(abs(xDist),abs(yDist)) <= radius:
            framesInTarget += 1
            onTarget.append(1)
        else:
            onTarget.append(0)
        targetx.append(prevX)
        targety.append(prevY)
        prevX = newX
        prevY = newY

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #presents trial feedback
    pct = (framesInTarget/(frameN+1))*100
    feedback = visual.TextStim(win=win, text = str(round(pct)) + '% in target.')
    residual2Sum = 0
    pctX = 0 # this is % NOT in target
    pctY = 0 # this is % NOT in target
    for num in zip(xDistance[-1*trialTime:], yDistance[-1*trialTime:], trialDist[-1*trialTime:]):
        residual2Sum += num[2]*num[2]
        if abs(num[0]) > radius:
            pctX += 1
        if abs(num[1]) > radius:
            pctY += 1
    pctX = (pctX/(frameN+1))*100 # LEFT HAND
    pctY = (pctY/(frameN+1))*100 # RIGHT HAND
    rootMeanSquaredError = sqrt(residual2Sum)
    #rmseDisp = visual.TextStim(win=win, text = str(round(rootMeanSquaredError, 1)) + '% off-center')
    #rmseDisp.setAutoDraw(True)
    feedback.setAutoDraw(True)
    target.setAutoDraw(False)
    crosshair.setAutoDraw(False)

    for i in range(0, frameN+1):
        onTargetPercent.append(pct)
        pctXOff.append(pctX)
        pctYOff.append(pctY)
        rmse.append(rootMeanSquaredError)
        numFramesInTarget.append(framesInTarget)

    timer = clock.CountdownTimer(3)
    while timer.getTime() > 0:
        win.flip()
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

    feedback.setAutoDraw(False)
    #rmseDisp.setAutoDraw(False)
    crosshair.setAutoDraw(True)
    return pctX, pctY

def main():
    # sandbox happens first
    holdScreen('Use this screen to experiment with moving the crosshairs.')

    # then training
    infoScreen('TRAINING TRIALS')
    runTraining()
    holdScreen('You have completed the training portion of this experiment.\nPlease notify the experimenter.')

    # then experiment blocks
    infoScreen('EXPERIMENT TRIALS')
    runExp()

    # Data structure-- NOTE: distance measures from crosshair center to closest edge of target!
    data = pd.DataFrame({'mouseX': mousex, 'mouseY': mousey, 'targetX': targetx, 'targetY': targety,
                        'distance': distance,'xDist': xDistance, 'yDist': yDistance,
                        'onTarget': onTarget, 'onTargetPercent': onTargetPercent, 'rmse': rmse,
                        'framesInTarget': numFramesInTarget, 'pctX': pctXOff, 'pctY': pctYOff,
                        'origin': ori, 'direction': dir, 'trialList': trialList, 'blockList': blockList,
                        'externalCond': condList, 'subject': subject})
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
