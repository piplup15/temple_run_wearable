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
import star_background

# Window Dimensions
screenW = 960
screenH = 960

# Direction + Color of Light
numLights = 1
lightColor = numpy.array([0.9,0.9,0.9,1], numpy.float32)
lightPosn = numpy.array([0, 0, 2, 0], numpy.float32)

# Camera Parameters
visField = 85

# Global textures
starrySkyTex = None

def initGL(w, h):
	global program, starrySkyTex
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

	if not glUseProgram:
		print 'Missing Shader Objects!'
		sys.exit(1)

	program = generateShaders()

def resize(w, h):
	global screenW, screenH
	if h < 400:  h = 400
	if w < 400:  w = 400
	screenW = w
	screenH = h
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(visField, float(w)/float(h), 0.1, 700.0)
	glMatrixMode(GL_MODELVIEW)
 
def glutPrint(x, y, font, text, r, g, b):
	glColor3f(r,g,b)
	glRasterPos2f(x,y)
	for ch in text:
		glutBitmapCharacter(font, ord(ch))

def display():
	global program
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	gluLookAt(-3,0,1.5, 0, 0, 0, 0, 0, 1)

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

	star_background.display(starrySkyTex, isTex)
	road.display(ambient, diffuse, specular, emission, shininess)

	glPopMatrix()

	glutSwapBuffers()

#keyHash is a parameter in controls.py
def keyPressed(*args):
	if args[0].lower() == 'q':
		sys.exit()


def idleFunc():
	glutPostRedisplay()

def main():
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
	glutMainLoop()

if __name__ == "__main__":
	main()