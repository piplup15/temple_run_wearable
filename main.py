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
from controls import *

# Window Dimensions
screenW = 960
screenH = 960

# Direction + Color of Light
lightColor = numpy.array([0.9,0.9,0.9,1], numpy.float32)
lightPosn = numpy.array([0.5, 0.5, -1, 0], numpy.float32)

# Camera Parameters
visField = 85

def initGL(w, h):
	global grassTex, platformTex, program
	glClearColor(skyR, skyG, skyB, skyA)
	glClearDepth(1.0)
	glDepthFunc(GL_LESS)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(visField, float(w)/float(h), 0.1, 700.0)
	glMatrixMode(GL_MODELVIEW)
	glEnable(GL_DEPTH_TEST)

	grassTex = loadTexture("images/grass.jpg")
	platformTex = loadTexture("images/helicopter_landing.jpg")

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
	global program, x, y, z, qx, qy, qz, qw, t, camera_degrees
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glLoadIdentity()

	gluLookAt(-5*zoom*cos(radians(camera_degrees)) + x, 5*zoom*sin(radians(camera_degrees)) + y, -2*zoom + z, x, y, z, 0, 0, -1)
	
	enablelighting = glGetUniformLocation(program, "enablelighting")
	glUniform1f(enablelighting, 1)
	numused = glGetUniformLocation(program, "numused")
	glUniform1i(numused, 1)
	lightposn = glGetUniformLocation(program, "lightposn")
	glUniform4fv(lightposn, 1, lightPosn)
	lightcol = glGetUniformLocation(program, "lightcolor")
	glUniform4fv(lightcol, 1, lightColor)

	isTex = glGetUniformLocation(program, "isTex")
	glUniform1i(isTex, 1)
	createGround(grassTex, params["z_start"])
	createPlatform(platformTex, params["z_start"])
	glUniform1i(isTex, 0)

	data = [x, y, z, qx, qy, qz, qw]
	createHelicopter(program, data)
	animateHelicopter(helicopterTime, pause)
	glutSwapBuffers()

#keyHash is a parameter in controls.py
def keyPressed(*args):
	global camera_degrees, zoom, speed, pause
	if args[0].lower() == keyHash['quit']:
		sys.exit()
	if args[0].lower() == keyHash['left']:
		camera_degrees -= 3
	if args[0].lower() == keyHash['right']:
		camera_degrees += 3
	if args[0].lower() == keyHash['zoomout']:
		zoom += 0.02
		if zoom > max_zoom: zoom = max_zoom
	if args[0].lower() == keyHash['zoomin']:
		zoom -= 0.02
		if zoom < min_zoom: zoom = min_zoom
	if args[0].lower() == keyHash['speed']:
		speed = (2*speed) % 31
	if args[0].lower() == keyHash['help']:
		printHelp()
	if args[0].lower() == keyHash['pause']:
		pause = not pause

def idleFunc():
	glutPostRedisplay()

def main():
	global datafile, zoom, max_zoom, min_zoom

	glutInit(sys.argv[0:1])

	if len(sys.argv) == 1:
		print "You must specify a file as input data for the visualizer. The command is: python main.py -f <filename> -p <params_filename>."
		exit(1)

	i = 1
	while i < len(sys.argv):
		paramsfilename = "default_params.txt"
		if sys.argv[i] == "-f" :
			try:
				datafilename = sys.argv[i+1]
				datafile = open(datafilename)
			except IndexError:
				print "You must specify a file as input data for the visualizer. The command is: python main.py -f <filename> -p <params_filename>."
				exit(1)
			except IOError:
				print "Unable to open file: " + sys.argv[i+1] + "."
				exit(1)
		elif sys.argv[i] == "-p" :
			try:
				paramsfilename = sys.argv[i+1]
				tmpFile = open(paramsfilename)
				tmpFile.close()
			except IndexError:
				print "You must specify a params file as the parameter for the -p flag. The command is: python main.py -f <filename> -p <params_filename>."
				exit(1)
			except IOError:
				print "Unable to open file: " + sys.argv[i+1] + "."
				exit(1)
		else:
			print "Illegal flag option; only -f <filename> and -p <params_filename> allowed."
			exit(1)
		i += 2

	print "Opened flight data file: " + datafilename + "."
	print "Opened params file: " + paramsfilename + "."
	print ""
	parseParams(paramsfilename)

	loadKeys()
	printHelp()

	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(screenW, screenH)
	glutInitWindowPosition(0, 0)
	window = glutCreateWindow("Helicopter Visualization")

	glutDisplayFunc(display)
	glutIdleFunc(idleFunc)
	glutReshapeFunc(resize)
	glutKeyboardFunc(keyPressed)
	initGL(screenW, screenH)
	glUseProgram(program)  
	glutMainLoop()

if __name__ == "__main__":
	main()