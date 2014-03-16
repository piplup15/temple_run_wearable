import OpenGL 
OpenGL.ERROR_ON_COPY = True 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
 
from OpenGL.GL.shaders import *
from math import *
import time, sys

import PIL.Image
import numpy
import time
import sys
import random

class Planet():
	def __init__(self, size, location, color, has_rings, tilt):
		self.location = location
		self.size = size
		self.has_rings = has_rings
		self.color = color
		self.tilt = tilt

	def drawPlanet(self,ambient, diffuse, specular, emission, shininess):
		glUniform4fv(emission, 1, numpy.array([0.0, 0.0, 0.0, 0.3], numpy.float32))
		glUniform4fv(ambient, 1, numpy.array(self.color, numpy.float32))
		glUniform4fv(diffuse, 1, numpy.array(self.color, numpy.float32))
		glUniform4fv(specular, 1, numpy.array(self.color, numpy.float32))
		glUniform1f(shininess, 1)
		glPushMatrix()
		glTranslatef(self.location[0], self.location[1], self.location[2])
		glScalef(self.size, self.size, self.size)
		glutSolidSphere(1, 20, 20)
		if self.has_rings:
			quadric = gluNewQuadric()
			glRotatef(self.tilt[0], 1,0,0)
			glRotatef(self.tilt[1], 0,1,0)
			glRotatef(self.tilt[2], 0,0,1)
			gluDisk(quadric, 1.2, 2, 50, 50)
		glPopMatrix()

	def update(self, speed):
		x,y,z = self.location
		self.location = (x-10*speed, y, z)


planets = []
cooldowns = {'L':0, 'R':0}
def drawPlanetLoop(ambient, diffuse, specular, emission, shininess, characterTransformX, speed):
	cleanup(characterTransformX)
	for planet in planets:
		planet.update(speed)
		planet.drawPlanet(ambient, diffuse, specular, emission, shininess)
	if not cooldowns['L']:
		spawn('L', characterTransformX)
	if not cooldowns['R']:
		spawn('R', characterTransformX)
	for cooldown in cooldowns.keys():
		cooldowns[cooldown] = max(0, cooldowns[cooldown]-1)

def cleanup(characterTransformX):
	for planet in list(planets):
		if planet.location[0] < characterTransformX - 2:
			planets.pop(0)
		else:
			return

def spawn(side, characterTransformX):
	should_spawn = random.random() < 0.1
	if should_spawn:
		size = (random.random()*0.99) + 2
		if side == 'L':
			locationY = (random.random()*10) -20
		elif side == 'R':
			locationY = (random.random()*10) +10

		locationZ = (random.random()*40) -20
		locationX = 100 + characterTransformX
		location = (locationX, locationY, locationZ)

		colorR = random.random()*0.3 + 0.3
		colorG = random.random()*0.3 + 0.3
		colorB = random.random()*0.3 + 0.3
		colorA = 0.5
		color = [colorR, colorG, colorB, colorA]
		if random.random() > 0.5:
			has_rings = True
			tiltX = random.random()*360
			tiltY = random.random()*360
			tiltZ = random.random()*360
			tilt = (tiltX, tiltY, tiltZ)
		else:
			has_rings = False
			tilt = None
		planets.append(Planet(size, location, color, has_rings, tilt))
		cooldowns[side] = int(random.random()*10)+10