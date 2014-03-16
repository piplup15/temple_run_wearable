import OpenGL 
OpenGL.ERROR_ON_COPY = True 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 
from OpenGL.GL.shaders import *
from math import *

import PIL.Image
import numpy
import time
import sys

from shaders import *
from textures import *
import controls
import road
import mapGrid
import star_background
import planets
import character
import serial
import threading
from serial import SerialException

WEARABLE = False
if WEARABLE:
	#Port
	port = "/dev/cu.usbmodem1411"
	#Serial
	serial = serial.Serial(port, 50000)

isDone = False

# Window Dimensions
screenW = 960
screenH = 720

# Direction + Color of Light
numLights = 1
lightColor = numpy.array([0.9,0.9,0.9,1], numpy.float32)
lightPosn = numpy.array([0, 0, 2, 0], numpy.float32)

# Camera Parameters
visField = 85

# Global textures
starrySkyTex = None

#Map Parameters
ROWS = 25
COLUMNS = 3
mapG = None

char = None
speed = 0.1
speed_update = 0.1 

currentTime = None
score = 0

textHash = None
shouldDisplaySpeedMessage = False
speedTextSequenceIndex = 0
speedTextHash = {}

def initGL(w, h):
	global program, starrySkyTex, mapG, char, currentTime, textHash
	glClearColor(0.0,0.0,0.0,1)
	glClearDepth(1.0)
	glDepthFunc(GL_LESS)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(visField, float(w)/float(h), 0.1, 700.0)
	glMatrixMode(GL_MODELVIEW)
	glEnable(GL_DEPTH_TEST)

	starrySkyTex = loadTexture("images/starry_sky.png")
	mapG = mapGrid.MapGrid(ROWS, COLUMNS)
	char = character.Character(mapG)
	currentTime = time.time()

	textHash = loadFont()
	loadSpeedTextHash()
	## TEMP

	if not glUseProgram:
		print 'Missing Shader Objects!'
		sys.exit(1)

	program = generateShaders()

def resize(w, h):
	global screenW, screenH
	if h < 700:  h = 700
	if w < 700:  w = 700
	screenW = w
	screenH = h
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(visField, float(w)/float(h), 0.1, 700.0)
	glMatrixMode(GL_MODELVIEW)

def display():
	global program, currentTime, score, screenH, screenW, speed, speed_update, shouldDisplaySpeedMessage
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	gluOrtho2D(0.0, screenW, 0.0, screenH)
	drawText(score)
	displaySpeedMessage()
	glPopMatrix()

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	updateOkay = False

	# aim for about 30 fps
	if (currentTime + 0.03 < time.time()):
		if speed != speed_update:
			speed = min(speed + 0.01, speed_update)
		char.update(speed)
		score += char.checkForDiamondCollision()
		if char.lastHundred < int(char.distXTraveled/(speed*10)) /100:
			char.lastHundred = int(char.distXTraveled/(speed*10)) /100
			speed_update = speed_update + 0.02
			shouldDisplaySpeedMessage = True
		currentTime = time.time()
		if not char.stopAnimation:
			score += 10
		updateOkay = True

	gluLookAt(-0.3+char.distXTraveled,0,0.7, 0+char.distXTraveled+1, 0, 0, 0, 0, 1)

	ambient = glGetUniformLocation(program, "ambient")
	diffuse = glGetUniformLocation(program, "diffuse")
	specular = glGetUniformLocation(program, "specular")
	emission = glGetUniformLocation(program, "emission")
	shininess = glGetUniformLocation(program, "shininess")

	enablelighting = glGetUniformLocation(program, "enablelighting")
	glUniform1f(enablelighting, 1)
	numused = glGetUniformLocation(program, "numused")
	glUniform1i(numused, numLights)
	lightposn = glGetUniformLocation(program, "lightposn")
	glUniform4fv(lightposn, 1, lightPosn)
	lightcol = glGetUniformLocation(program, "lightcolor")
	glUniform4fv(lightcol, 1, lightColor)

	glPushMatrix()
	glUniform4fv(ambient, 1, numpy.array([0.3, 0.3, 0.4, 1.0], numpy.float32))
	glUniform4fv(emission, 1, numpy.array([0.0, 0.0, 0.0, 1.0], numpy.float32))
	glUniform4fv(diffuse, 1, numpy.array([0.2, 0.2, 0.5, 1.0], numpy.float32))
	glUniform4fv(specular, 1, numpy.array([0.5, 0.5, 0.5, 1.0], numpy.float32))
	glUniform1f(shininess, 1)

	isTex = glGetUniformLocation(program, "isTex")

	star_background.display(starrySkyTex, isTex, char.distXTraveled)


	road.display(ambient, diffuse, specular, emission, shininess, ROWS, COLUMNS, mapG, char.distXTraveled, updateOkay)
	planets.drawPlanetLoop(ambient, diffuse, specular, emission, shininess, char.distXTraveled, speed)
	char.draw(ambient,diffuse,specular,emission,shininess)	
	glPopMatrix()

	glutSwapBuffers()

def drawText(score):
	global textHash
	val = score
	digits = []
	numDigits = 8
	isTex = glGetUniformLocation(program, "isTex")
	glUniform1i(isTex, 1)
	glEnable(GL_TEXTURE_2D)

	xIndex = 0

	for i in ['S','C','O','R','E',' ']:
		id = textHash[i]
		setupTex(id)

		glBegin(GL_QUADS);
		glTexCoord2f(1.0, 0.0); glVertex2f(xIndex+48, screenH-48)
		glTexCoord2f(1.0, 1.0); glVertex2f(xIndex, screenH-48)
		glTexCoord2f(0.0, 1.0); glVertex2f(xIndex, screenH)
		glTexCoord2f(0.0, 0.0); glVertex2f(xIndex+48, screenH)
		glEnd()

		xIndex += 48

	for i in range(0,numDigits+1):
		digits.append(val % 10)
		val = val / 10

	digits.reverse()
	for digit in digits:
		id = textHash[str(digit)]
		setupTex(id)

		glBegin(GL_QUADS);
		glTexCoord2f(1.0, 0.0); glVertex2f(xIndex+48, screenH-48)
		glTexCoord2f(1.0, 1.0); glVertex2f(xIndex, screenH-48)
		glTexCoord2f(0.0, 1.0); glVertex2f(xIndex, screenH)
		glTexCoord2f(0.0, 0.0); glVertex2f(xIndex+48, screenH)
		glEnd()

		xIndex += 48

	glDisable(GL_TEXTURE_2D)
	glUniform1i(isTex, 0)

def setupTex(id):
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) 
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) 
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) 
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) 
	glBindTexture(GL_TEXTURE_2D, id)

def displaySpeedMessage():
	global shouldDisplaySpeedMessage, speedTextHash, speedTextSequenceIndex
	if shouldDisplaySpeedMessage:
		isTex = glGetUniformLocation(program, "isTex")
		glUniform1i(isTex, 1)
		glEnable(GL_TEXTURE_2D)
		startY = speedTextHash[speedTextSequenceIndex]
		yIndex = 0
		for char in 'FASTER...':
			id = textHash['g'+char]
			setupTex(id)

			glBegin(GL_QUADS);
			glTexCoord2f(1.0, 0.0); glVertex2f(screenW-10, startY-48-yIndex)
			glTexCoord2f(1.0, 1.0); glVertex2f(screenW-58, startY-48-yIndex)
			glTexCoord2f(0.0, 1.0); glVertex2f(screenW-58, startY-yIndex)
			glTexCoord2f(0.0, 0.0); glVertex2f(screenW-10, startY-yIndex)
			glEnd()
			yIndex += 48

		glDisable(GL_TEXTURE_2D)
		glUniform1i(isTex, 0)
		speedTextSequenceIndex += 1
		if speedTextSequenceIndex not in speedTextHash.keys():
			shouldDisplaySpeedMessage = False
			speedTextSequenceIndex = 0

def loadSpeedTextHash():
	for i in range(0,10):
		speedTextHash[i] = (screenH*3/4)*i/10
	for i in range(0,100):
		speedTextHash[i+10] = screenH*3/4
	for i in range(0,10):
		speedTextHash[i+110] = (screenH*3/4) + (screenH*3/4)*i/10

#keyHash is a parameter in controls.py
def keyPressed(*args):
	global char, isDone
	if args[0].lower() == 'q':
		isDone = True
		sys.exit()
	if args[0].lower() == 'j':
		char.updateComm('left')
	if args[0].lower() == 'k':
		char.updateComm('right')
	if args[0].lower() == 'v':
		char.updateComm('jump')

def serial_read():
	global port, serial, isDone
	while not isDone:
		try:
			value = serial.read()
			#print value
			#if value == 'j':
			#	char.updateComm('jump')
			if value == 'r':
				char.updateComm('right')
			if value == 'l':
				char.updateComm('left')	
		except:
			continue

def idleFunc():
	glutPostRedisplay()

def main():
	global WEARABLE
	glutInit(sys.argv[0:1])

	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(screenW, screenH)
	glutInitWindowPosition(0, 0)
	window = glutCreateWindow("Wearable Temple Run")

	glutDisplayFunc(display)
	glutIdleFunc(idleFunc)
	glutReshapeFunc(resize)
	glutKeyboardFunc(keyPressed)
	initGL(screenW, screenH)
	glUseProgram(program)
	if WEARABLE:
		t1 = threading.Thread(target = serial_read)
		t1.start() 
	glutMainLoop()

if __name__ == "__main__":
	main()