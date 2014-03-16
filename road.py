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
import random

import mapGrid

colorMap = {
	0: (0.7, 0.2, 0.2),
	1: (0.7, 0.7, 0.2),
	2: (0.2, 0.7, 0.2),
	3: (0.2, 0.7, 0.7),
	4: (0.2, 0.2, 0.7),
}

gateColor = 0.5
gateLow = 0.5
gateHigh = 1.0
gateDirection = 1

def display(ambient, diffuse, specular, emission, shininess, rows, columns, mapG, characterTranslate):
	global gateColor, gateLow, gateHigh, gateDirection
	if int(characterTranslate + rows) not in mapG.mapGrid.keys():
		if random.random() > 0.15:
			length = int(random.random()*10) + 5
			mapG.addRandomPath(length, characterTranslate)
		else:
			length = int(random.random()*2) + 1
			mapG.addFigureEightPath(length, characterTranslate)

	gateColor += gateDirection*0.01
	if gateColor > gateHigh:
		gateDirection = -1
	if gateColor < gateLow:
		gateDirection = 1

	for i in range(int(characterTranslate),rows+int(characterTranslate)):
		r,g,b = colorMap[i % len(colorMap.keys())]
		glUniform4fv(emission, 1, numpy.array([0.0, 0.0, 0.0, 0.3], numpy.float32))
		glUniform4fv(ambient, 1, numpy.array([r, g, b, 0.3], numpy.float32))
		glUniform4fv(diffuse, 1, numpy.array([r, g, b, 0.3], numpy.float32))
		glUniform4fv(specular, 1, numpy.array([r, g, b, 0.3], numpy.float32))
		glUniform1f(shininess, 1)
		for j in range(0, columns):
			if mapG.mapGrid[i][j] == 1:
				glPushMatrix()
				glTranslatef(-1 + i,0.2*(-((columns-1)/2)+j),0)
				glScalef(1,0.195,0.2)
				glTranslatef(0.5, 0, 0)
				glutSolidCube(1)
				glPopMatrix()

		if (i % 5 == 0):
			glUniform4fv(emission, 1, numpy.array([0.0, 0.0, 0.0, 0.3], numpy.float32))
			glUniform4fv(ambient, 1, numpy.array([gateColor, gateColor, 0.2, 0.3], numpy.float32))
			glUniform4fv(diffuse, 1, numpy.array([gateColor, gateColor, 0.2, 0.3], numpy.float32))
			glUniform4fv(specular, 1, numpy.array([gateColor, gateColor, 0.2, 0.3], numpy.float32))
			glUniform1f(shininess, 1)
			glPushMatrix()
			glTranslatef(-1 + i,-0.15 - 0.2*(-((columns-1)/2)+j),0)
			glScalef(0.1,0.1,0.5)
			glTranslatef(0.5, 0, 0)
			glutSolidCube(1)
			glPopMatrix()
			glPushMatrix()
			glTranslatef(-0.95 + i,-0.15 - 0.2*(-((columns-1)/2)+j),0.3)
			glutSolidSphere(0.05, 40, 40)
			glPopMatrix()
			glPushMatrix()
			glTranslatef(-1 + i, 0.15 + 0.2*(-((columns-1)/2)+j),0)
			glScalef(0.1,0.1,0.5)
			glTranslatef(0.5, 0, 0)
			glutSolidCube(1)
			glPopMatrix()
			glPushMatrix()
			glTranslatef(-0.95 + i,0.15 + 0.2*(-((columns-1)/2)+j),0.3)
			glutSolidSphere(0.05, 40, 40)
			glPopMatrix()


	for k in range(0,columns+1):
		glPushMatrix()
		glTranslatef(-2 + characterTranslate ,0.2*(-(columns*1.0/2)+k),0)
		glScalef(rows,0.01,0.22)
		glTranslatef(0.5, 0, 0)
		glUniform4fv(emission, 1, numpy.array([0.0, 0.0, 0.0, 0.4], numpy.float32))
		glUniform4fv(ambient, 1, numpy.array([0.4, 0.4, 0.4, 0.4], numpy.float32))
		glUniform4fv(diffuse, 1, numpy.array([0.4, 0.4, 0.4, 0.4], numpy.float32))
		glUniform4fv(specular, 1, numpy.array([0.5, 0.5, 0.5, 0.4], numpy.float32))
		glUniform1f(shininess, 1)
		glutSolidCube(1)
		glPopMatrix()

		glUniform4fv(emission, 1, numpy.array([0.0, 0.0, 0.0, 0.3], numpy.float32))
		glUniform4fv(ambient, 1, numpy.array([gateColor, gateColor, 0.2, 0.3], numpy.float32))
		glUniform4fv(diffuse, 1, numpy.array([gateColor, gateColor, 0.2, 0.3], numpy.float32))
		glUniform4fv(specular, 1, numpy.array([gateColor, gateColor, 0.2, 0.3], numpy.float32))
		glUniform1f(shininess, 1)

		glPushMatrix()
		glTranslate(-2 + characterTranslate, -0.13 - 0.2*((columns-1)/2), 0.15 )
		glScalef(rows, 0.02, 0.04)
		glTranslate(0.5,0,0)
		glutSolidCube(1)
		glPopMatrix()

		glPushMatrix()
		glTranslate(-2 + characterTranslate, 0.13 + 0.2*((columns-1)/2), 0.15 )
		glScalef(rows, 0.02, 0.04)
		glTranslate(0.5,0,0)
		glutSolidCube(1)
		glPopMatrix()