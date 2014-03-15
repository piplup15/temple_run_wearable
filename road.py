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

def display(ambient, diffuse, specular, emission, shininess, rows, columns, mapG, characterTranslate):

	if int(characterTranslate + rows) not in mapG.mapGrid.keys():
		mapG.addRandomPath(10, characterTranslate)

	for i in range(int(characterTranslate),rows+int(characterTranslate)):
		r,g,b = colorMap[i % len(colorMap.keys())]
		for j in range(0, columns):
			if mapG.mapGrid[i][j] == 1:
				glPushMatrix()
				glTranslatef(-1 + i,0.2*(-((columns-1)/2)+j),0)
				glScalef(1,0.195,0.2)
				glTranslatef(0.5, 0, 0)
				glUniform4fv(emission, 1, numpy.array([0.0, 0.0, 0.0, 0.3], numpy.float32))
				glUniform4fv(ambient, 1, numpy.array([r, g, b, 0.3], numpy.float32))
				glUniform4fv(diffuse, 1, numpy.array([r, g, b, 0.3], numpy.float32))
				glUniform4fv(specular, 1, numpy.array([r, g, b, 0.3], numpy.float32))
				glUniform1f(shininess, 1)
				glutSolidCube(1)
				glPopMatrix()

	for k in range(0,columns+1):
		glPushMatrix()
		glTranslatef(-1 + characterTranslate ,0.2*(-(columns*1.0/2)+k),0)
		glScalef(rows,0.01,0.22)
		glTranslatef(0.5, 0, 0)
		glUniform4fv(emission, 1, numpy.array([0.0, 0.0, 0.0, 0.4], numpy.float32))
		glUniform4fv(ambient, 1, numpy.array([0.4, 0.4, 0.4, 0.4], numpy.float32))
		glUniform4fv(diffuse, 1, numpy.array([0.4, 0.4, 0.4, 0.4], numpy.float32))
		glUniform4fv(specular, 1, numpy.array([0.5, 0.5, 0.5, 0.4], numpy.float32))
		glUniform1f(shininess, 1)
		glutSolidCube(1)
		glPopMatrix()
