#tracker.py
#crosshairs are covered by target
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
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
import pandas as pd

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'tracking'  # from the Builder filename that created this script
expInfo = {'session': '001', 'participant': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# save a log file for detail verbose info
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# flag for 'escape' or other condition => quit the exp
endExpNow = False

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# Setup the Window
win = visual.Window(size=[1100, 1100], fullscr=False, screen=0, allowGUI=True, allowStencil=False, 
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
buttonPress = joy
buttonPress.status = NOT_STARTED

# setup some python lists for storing info about the mouse
mousex = []
mousey = []
targetx = []
targety = []
distance = []
xDistance = []
yDistance = []
onTarget = []
ori = []
dir = []
trialList = []
subject = []
onTargetPercent = []
numFramesInTarget = []

def infoScreen(display):
    text = visual.TextStim(win=win, text=display, height=.075)
	text.setAutoDraw(True)
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    trialComponents = [text, buttonPress]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
    
        # *mouse* updates
        if t >= 0.0 and buttonPress.status == NOT_STARTED:
            # keep track of start time/frame for later
            buttonPress.tStart = t
            buttonPress.frameNStart = frameN  # exact frame index
            buttonPress.status = STARTED
            prevButtonState = buttonPress.getButton(0)  # if button is down already this ISN'T a new click
        if buttonPress.status == STARTED:  # only update if started and not stopped!
            buttons = buttonPress.getButton(0)
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if buttons:  # state changed to a new click
                    # abort routine on response
                    continueRoutine = False

		#crosshair updates 
        crosshair.setPos((buttonPress.getX(), -1*buttonPress.getY()))
        crosshair.setAutoDraw(True)
        crosshair.setAutoLog(False)
    
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            text.setAutoDraw(False)
            win.flip()
            break
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
    
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

def trialScreen(trialNum, origin, direction):
    intInstr = ["Focus on your hands squeezing the sensors.", 
                "Think about the right amount of force to use.", 
                "Pay attention to how you grip the sensors."]
    extInstr = ["Focus on the distance from your cursor to the target.", 
                "Think about how the target moves around the screen.", 
                "Pay attention to where you want to move your cursor."]
    if (int(expInfo['participant']) % 2) == 0:
        text = visual.TextStim(win=win, text=intInstr[int(trialNum*10)%3])
    else:
        text = visual.TextStim(win=win, text=extInstr[int(trialNum*10)%3])

    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    timer = clock.CountdownTimer(3)
    while timer.getTime() > 0:
        text.draw()
        win.flip()
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
    
    indicator = visual.TextStim(win=win, text='Target\nappears\nhere.', height=.075)
    dirInd = visual.TextStim(win=win, text='>', height=.1)
    
    trialName = 'Trial ' + str(trialNum) + '\nClick to begin.'
    if trialNum < 1:
        trialName = 'Training Trial ' + str(int(trialNum*10)) + '\nClick to begin.'
    text = visual.TextStim(win=win, text=trialName, height=0.075)
    
    UP = 270
    DOWN = 90
    LEFT = 180
    RIGHT = 0
    NW = 225
    NE = 315
    SE = 45
    SW = 135
    
    if origin == 1:
        indicator.pos = (0,.75)
        dirInd.pos = (0,.5)
        if direction == 'CW':
            dirInd.ori = SE
        elif direction == 'CC':
            dirInd.ori = SW
        elif direction == 'VT':
            dirInd.ori = DOWN
            
    if origin == 2:
        indicator.pos = (.75,0)
        dirInd.pos = (.5,0)
        if direction == 'CW':
            dirInd.ori = SW
        elif direction == 'CC':
            dirInd.ori = NW
        elif direction == 'HZ':
            dirInd.ori = LEFT
            
    if origin == 3:
        indicator.pos = (0,-.75)
        dirInd.pos = (0,-.5)
        if direction == 'CW':
            dirInd.ori = NW
        elif direction == 'CC':
            dirInd.ori = NE
        elif direction == 'VT':
            dirInd.ori = UP
            
    if origin == 4:
        indicator.pos = (-.75,0)
        dirInd.pos = (-.5,0)
        if direction == 'CW':
            dirInd.ori = NE
        elif direction == 'CC':
            dirInd.ori = SE
        elif direction == 'HZ':
            dirInd.ori = RIGHT

	t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    trialComponents = [text, indicator, dirInd, buttonPress]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
    
        # *text* updates
        if t >= 0.0 and text.status == NOT_STARTED:
            # keep track of start time/frame for later
            text.tStart = t
            text.frameNStart = frameN  # exact frame index
            text.setAutoDraw(True)
            text.setAutoLog(False)
        
        # *indicator* updates
        if t >= 0.0 and indicator.status == NOT_STARTED:
            # keep track of start time/frame for later
            indicator.tStart = t
            indicator.frameNStart = frameN  # exact frame index
            indicator.setAutoDraw(True)
            indicator.setAutoLog(False)
		
		# *arrow (dirInd)* updates
        if t >= 0.0 and dirInd.status == NOT_STARTED:
            # keep track of start time/frame for later
            dirInd.tStart = t
            dirInd.frameNStart = frameN  # exact frame index
            dirInd.setAutoDraw(True)
            dirInd.setAutoLog(False)  
			
        # *mouse* updates
        if t >= 0.0 and buttonPress.status == NOT_STARTED:
            # keep track of start time/frame for later
            buttonPress.tStart = t
            buttonPress.frameNStart = frameN  # exact frame index
            buttonPress.status = STARTED
            prevButtonState = buttonPress.getButton(0)  # if button is down already this ISN'T a new click
        if buttonPress.status == STARTED:  # only update if started and not stopped!
            buttons = buttonPress.getButton(0)
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if buttons:  # state changed to a new click
                    # abort routine on response
                    continueRoutine = False
                    
		#crosshair updates
        crosshair.setPos((buttonPress.getX(), -1*buttonPress.getY()))
        crosshair.setAutoDraw(True)
        crosshair.setAutoLog(False)
    
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            text.setAutoDraw(False)
            indicator.setAutoDraw(False)
            dirInd.setAutoDraw(False)
            win.flip()
            break
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
    
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

def runTraining():
    #movement: 
    #1 is top
    #2 is right 
    #3 is bottom
    #4 is left
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
    
    #add free motion screen, end on spacebar?
    
    #bottom VT
    trialScreen(0.1, 3, 'VT')
    runTrial(0.1, 3, 'VT')
    #left HZ
    trialScreen(.2, 4, 'HZ')
    runTrial(.2, 4, 'HZ')
    #top VT
    trialScreen(.3, 1, 'VT')
    runTrial(.3, 1, 'VT')
    #right HZ
    trialScreen(.4, 2, 'HZ')
    runTrial(.4, 2, 'HZ')
    #top CW
    trialScreen(.5, 1, 'CW')
    runTrial(.5, 1, 'CW')
    #left CC
    trialScreen(.6, 4, 'CC')
    runTrial(.6, 4, 'CC')
    #bottom CW
    trialScreen(.7, 3, 'CW')
    runTrial(.7, 3, 'CW')
    #right CC
    trialScreen(.8, 2, 'CC')
    runTrial(.8, 2, 'CC')
    
    infoScreen("You have completed the training portion of this experiment.\nPlease notify the experimenter.")

def runExp():
    params = []
    for num in range(1,5):
        params.append({'ori':num, 'dir':'CW'})
        params.append({'ori':num, 'dir':'CC'})

    #setup TrialHandler
    numTrials = 16
    trials = data.TrialHandler(params, numTrials, method='random')
    trialNum = 1
    
    for trial in trials:
        trialScreen(trialNum, trial['ori'], trial['dir'])
        runTrial(trialNum, trial['ori'], trial['dir'])
        trialNum = trialNum + 1

def runTrial(trialNum, origin, direction):
    # ------Prepare to start Routine "trial"-------
    #set up some useful variables
    RADIUS = .125
    MOTION = .01
    length = 1200 # about 20 sec
    if trialNum < 1:
        length = 600 # about 10 sec
    
    continueRoutine = True
    framesInTarget = 0
    
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
        prevY = 1 - RADIUS
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
        prevX = 1 - RADIUS
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
        prevY = -1 + RADIUS
        if direction == 'CW':
            moveRight = False
        if direction == 'CC':
            moveUp = False
    
    #left
    if origin == 4:
        currX = -1
        prevX = -1 + RADIUS
        if direction == 'CC':
            moveUp = False


    # -------Start Routine "trial"-------
    for frameN in range(0,length):
        target.setAutoDraw(True)
        
		# crosshair updates
        crosshair.setPos((buttonPress.getX(), -1*buttonPress.getY()))
        crosshair.setAutoDraw(True)
        crosshair.setAutoLog(False)
		
        #calculates and stores distance from mouse to target center
        x = joy.getX()
        y = -1*joy.getY()
        xDist = abs(x - prevX)
        yDist = abs(y - prevY)
        hypotenuse = sqrt( (xDist*xDist) + (yDist*yDist) )
        xDistance.append(xDist)
        yDistance.append(yDist)
        distance.append(hypotenuse)
        if max(abs(xDist),abs(yDist)) <= RADIUS:
            framesInTarget += 1
            onTarget.append(1)
        else:
            onTarget.append(0)
        
        #currX, currY set the general motion of the target
        #i.e. moves down, moves diagonally up and right, etc.
        #sets horizontal motion (all motion patterns EXCEPT VT)
        if direction != 'VT':
            if moveRight:
                currX = currX + MOTION
            else:
                currX = currX - MOTION
        
        #sets vertical motion
        if direction != 'HZ':
            if moveUp:
                currY = currY + MOTION
            else:
                currY = currY - MOTION
        
        #changing curr to new makes the motion smooth
        newX = sin(currX)
        newY = sin(currY)
        
        # prevents target from going off the screen
        if newX < -1 + RADIUS:
            moveRight = True
        if newX > 1 - RADIUS:
            moveRight = False
        if newY < -1 + RADIUS:
            moveUp = True
        if newY > 1 - RADIUS:
            moveUp = False
        
        target.setPos((newX, newY))
    
        #save target pos each frame
        targetx.append(prevX)
        targety.append(prevY)
        prevX = newX
        prevY = newY
        
        # save mouse positions each frame
        mousex.append(joy.getX())
        mousey.append(-1*joy.getY())
        subject.append(expInfo['participant'])
        
        # save trial
        trialList.append(trialNum)
        ori.append(origin)
        dir.append(direction)
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
            
    #presents trial feedback
    feedback = visual.TextStim(win=win, text = "You were within the target for " + str(framesInTarget) + "/" + str(frameN+1) + " frames")
    pct = (framesInTarget/(frameN+1))*100
    percent =  visual.TextStim(win=win, text = str(round(pct)) + '%', pos=((0, .5)))
    percent.setAutoDraw(True)
    feedback.setAutoDraw(True)
    target.setAutoDraw(False)
    for i in range(0, frameN+1):
        onTargetPercent.append(pct)
        numFramesInTarget.append(framesInTarget)
    timer = clock.CountdownTimer(3)
    while timer.getTime() > 0:
        win.flip()
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
    feedback.setAutoDraw(False)
    percent.setAutoDraw(False)

def main():
	# training happens first
    infoScreen('PRACTICE TRIALS\nCLICK TO START')
    #runTraining() #training trials are listed as 0.1, 0.2, etc.

    # then experiment blocks
    infoScreen('EXPERIMENT TRIALS\nCLICK TO START')
    runExp()
    
    # Data structure
    data = pd.DataFrame({'mouseX': mousex, 'mouseY': mousey, 'targetX': targetx, 'targetY': targety, 'distance': distance, 
                        'xDist': xDistance, 'yDist': yDistance, 'onTarget': onTarget, 'onTargetPercent': onTargetPercent, 
                        'framesInTarget': numFramesInTarget, 'origin': ori, 'direction': dir,'trialList': trialList, 'subject': subject})
    data.to_csv(filename + '.csv')

    # final screen and quit
    infoScreen('You have completed the experiment.\nPlease notify the experimenter.')
    logging.flush()
    win.close()
    core.quit()

main()