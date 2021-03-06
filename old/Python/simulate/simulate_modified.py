#!/usr/bin/env python3
# Simulate (a Simon clone)
# Originally by Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import sys, os, pygame as pg
from pygame.locals import *

FLASHSPEED = 500 # in milliseconds
FLASHDELAY = 200 # in milliseconds
BUTTONGAPSIZE = 20
TIMEOUT = 4 # seconds before game over if no button is pushed.

CURRENT_DIR = os.path.dirname(__file__)

#                R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
bgColor = BLACK

TEXTCOLOR = WHITE



def main(sequence, resolution=(540,540), fps=60):
    global BUTTONSIZE, YELLOWRECT, BLUERECT, REDRECT, GREENRECT, XMARGIN, YMARGIN, FPS, FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    BUTTONSIZE = (resolution[0]-40)/2
    
    XMARGIN = int((resolution[0] - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
    YMARGIN = int((resolution[1] - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
    
    # Rect objects for each of the four buttons
    YELLOWRECT = pg.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
    BLUERECT   = pg.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
    REDRECT    = pg.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
    GREENRECT  = pg.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
    
    pg.init()
    FPS = fps
    FPSCLOCK = pg.time.Clock()
    DISPLAYSURF = pg.display.set_mode((resolution[0], resolution[1]))
    pg.display.set_caption('Simulate')

    BASICFONT = pg.font.Font('freesansbold.ttf', 16)

    # load the sound files
    BEEP1 = pg.mixer.Sound(f'{CURRENT_DIR}/sounds/beep1.ogg')
    BEEP2 = pg.mixer.Sound(f'{CURRENT_DIR}/sounds/beep2.ogg')
    BEEP3 = pg.mixer.Sound(f'{CURRENT_DIR}/sounds/beep3.ogg')
    BEEP4 = pg.mixer.Sound(f'{CURRENT_DIR}/sounds/beep4.ogg')

    # Initialize some variables for a new game
    pattern = sequence # PRESET PATTER
    currentStep = 0 # the color the player must push next

    while True: # main game loop
        clickedButton = None # button that was clicked (set to YELLOW, RED, GREEN, or BLUE)
        DISPLAYSURF.fill(bgColor)
        drawButtons()

        checkForQuit()
        for event in pg.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN

        # wait for the player to enter buttons
        if clickedButton and clickedButton == pattern[currentStep]:
            # pushed the correct button
            flashButtonAnimation(clickedButton)
            currentStep += 1

            if currentStep == len(pattern):
                return "You solved it!"

        elif clickedButton and clickedButton != pattern[currentStep]:
            flashButtonAnimation(clickedButton)
            return None # LOSE STATE

        pg.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pg.quit()
    sys.exit()


def checkForQuit():
    for event in pg.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pg.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pg.event.post(event) # put the other KEYUP event objects back


def flashButtonAnimation(color, animationSpeed=50):
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT

    origSurf = DISPLAYSURF.copy()
    flashSurf = pg.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pg.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))


def drawButtons():
    pg.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pg.draw.rect(DISPLAYSURF, BLUE,   BLUERECT)
    pg.draw.rect(DISPLAYSURF, RED,    REDRECT)
    pg.draw.rect(DISPLAYSURF, GREEN,  GREENRECT)


def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint( (x, y) ):
        return YELLOW
    elif BLUERECT.collidepoint( (x, y) ):
        return BLUE
    elif REDRECT.collidepoint( (x, y) ):
        return RED
    elif GREENRECT.collidepoint( (x, y) ):
        return GREEN
    return None


if __name__ == '__main__':
    main()
