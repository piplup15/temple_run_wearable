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

MAX_LENGTH = 60

colorMap = {
	0: (0.7, 0.2, 0.2),
	1: (0.7, 0.7, 0.2),
	2: (0.2, 0.7, 0.2),
	3: (0.2, 0.7, 0.7),
	4: (0.2, 0.2, 0.7),
}

def display(ambient, diffuse, specular, emission, shininess):
	for i in range(0,MAX_LENGTH):
		r,g,b = colorMap[i % len(colorMap.keys())]
		for j in range(-2,3):
			glPushMatrix()
			glTranslate(-7.5+1.5*i,j,0)
			glScalef(1.5,0.98,0.2)
			glUniform4fv(emission, 1, numpy.array([0.0, 0.0, 0.0, 0.3], numpy.float32))
			glUniform4fv(ambient, 1, numpy.array([r, g, b, 0.3], numpy.float32))
			glUniform4fv(diffuse, 1, numpy.array([r, g, b, 0.3], numpy.float32))
			glUniform4fv(specular, 1, numpy.array([r, g, b, 0.3], numpy.float32))
			glUniform1f(shininess, 1)
			glutSolidCube(1)
			glPopMatrix()
		for k in range(0,6):
			glPushMatrix()
			glTranslate(-7.5+1.5*i,-2.5+k,0)
			glScalef(1.5,0.02,0.24)
			glUniform4fv(emission, 1, numpy.array([0.0, 0.0, 0.0, 0.4], numpy.float32))
			glUniform4fv(ambient, 1, numpy.array([0.4, 0.4, 0.4, 0.4], numpy.float32))
			glUniform4fv(diffuse, 1, numpy.array([0.4, 0.4, 0.4, 0.4], numpy.float32))
			glUniform4fv(specular, 1, numpy.array([0.5, 0.5, 0.5, 0.4], numpy.float32))
			glUniform1f(shininess, 1)
			glutSolidCube(1)
			glPopMatrix()
