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

transx = 0
transy = 0
transz = 2
rotAngley = 0
rotAnglex = 0
rotAnglez = 0
rotaterightleg = 0
rotateleftleg = 0

rotaterightarmtop = 0
rotateleftarm = 0

stp = 2.5
lstp = -2.5

ratop = 1.5
latop = -1.5

class Character():
	def __init__(self, mapGrid):
		self.positionZ = 0
		self.positionY = 0
		self.distXTraveled = 0.5
		self.column = 0
		self.velocityZ = 0
		self.mapGrid = mapGrid
		self.command = []
		self.targetCol = None

	def draw(self, ambient, diffuse, specular, emission, shininess):
		global rotaterightleg, rotateleftleg, stp, lstp, rotaterightarmtop, rotateleftarm, ratop, latop
		
		glPushMatrix()

		if (rotaterightleg > 15):
			stp = -3.5
		if (rotaterightleg < -15):
			stp = 3.5

		if (rotateleftleg < -15):
			lstp = 3.5
		if (rotateleftleg > 15):
			lstp = -3.5
		rotateleftleg += lstp	
		rotaterightleg += stp

		if (rotaterightarmtop > 25):
			ratop = -5.5
		if (rotaterightarmtop < -25):
			ratop = 5.5
		if (rotateleftarm < -25):
			latop = 5.5
		if (rotateleftarm > 25):
			latop = -5.5

		rotaterightarmtop += ratop
		rotateleftarm += latop

		glUniform4fv(emission, 1, numpy.array([0.0, 0.0, 0.0, 0.4], numpy.float32))
		glUniform4fv(ambient, 1, numpy.array([0.3, 0.3, 0.8, 0.4], numpy.float32))
		glUniform4fv(diffuse, 1, numpy.array([0.3, 0.3, 0.8, 0.4], numpy.float32))
		glUniform4fv(specular, 1, numpy.array([0.3, 0.3, 0.8, 0.4], numpy.float32))
		glUniform1f(shininess, 1)
		glTranslatef(self.distXTraveled, 0.2*self.positionY, 0.2 + self.positionZ)
		glTranslatef(0,-0.0314,0.05)
		glScalef(0.03,0.03,0.03)
		glRotatef(90,0,0,1)

		####CHARACTER STARTS ####
		glPushMatrix()
		glTranslatef(0, 1,1.5)
		# Left Ear
		glutSolidSphere(.5,20,20)

		glPopMatrix()

		glPushMatrix()
		glTranslatef(1, 1,1)	
		#Head
		glutSolidSphere(1,20,20)
		
		
		glPopMatrix()

		glPushMatrix()
		glTranslatef(2, 1,1.5)
		#Right Ear
		glutSolidSphere(.5, 20, 20)
		
		
		glPopMatrix()
		glPushMatrix()
		
		#rotations translations
		#glScalef(0.0, 0.0, 0.0)
		glScalef(1.0, 1.0, 1.5)
		glTranslatef(1, .85, -1)
		#glScalef(0.0, 0.0, 0.0)
		glutSolidCube(2);
		
		#Right Leg
		glPopMatrix()
		glPushMatrix()
		glRotatef(rotaterightleg, 1, 0, 0)
		glTranslatef(.5, .5, -5)
		obj = gluNewQuadric();
		gluCylinder(obj, .25, .5, 3, 40, 40);
		

		#Left Leg
		glPopMatrix()
		glPushMatrix()
		glRotatef(rotateleftleg, 1, 0, 0)
		glTranslatef(1.5, .5, -5)
		obj = gluNewQuadric();
		gluCylinder(obj, .25, .5, 3, 40, 40);

		#Right arm 
		glPopMatrix()
		glPushMatrix()

		glTranslate(0, 0, 1.5)
		glRotatef(15, 0, 1, 0)
		glScalef(1, 1, .5)
		glTranslatef(0, 1, -3)


		#Arm animation
		glRotatef(rotaterightarmtop, 1, 0, 0)
		glTranslate(.5, 0, -3)

		obj = gluNewQuadric();
		gluCylinder(obj, .25, .5, 3, 40, 40);
		
		#glTranslatef(0, 0, 0)
		glRotatef(45, 1, 0, 0)
		obj = gluNewQuadric();
		gluCylinder(obj, .25, .25, 2, 40, 40);

		glTranslatef(0, 0, 2)
		glutSolidSphere(.3, 20, 20)



		#Left arm 
		glPopMatrix()
		glPushMatrix()

		glTranslate(1.10, 0, 1.25)
		glRotatef(-15, 0, 1, 0)
		glScalef(1, 1, .5)
		glTranslatef(0, 1, -3)


		#Arm animation
		glRotatef(rotateleftarm, 1, 0, 0)
		glTranslate(.5, 0, -3)

		obj = gluNewQuadric();
		gluCylinder(obj, .25, .5, 3, 40, 40);
		
		#glTranslatef(0, 0, 0)
		glRotatef(45, 1, 0, 0)
		obj = gluNewQuadric();
		gluCylinder(obj, .25, .25, 2, 40, 40);

		glTranslatef(0, 0, 2)
		glutSolidSphere(.3, 20, 20)

		
		glPopMatrix()
		glPopMatrix()

	def updateComm(self,param):
		valid = len(self.command) == 0
		valid = valid or (len(self.command) > 0 and "jump" in self.command and param != "jump")
		valid = valid or (len(self.command) > 0 and "right" in self.command and param == "jump")
		valid = valid or (len(self.command) > 0 and "left" in self.command and param == "jump")
		if valid:
			if param == 'left':
				if 'left' not in self.command:
					self.command += ['left']
				self.targetCol = min(1, self.column+1)
			if param == 'right':
				if 'right' not in self.command:
					self.command += ['right']
				self.targetCol = max(-1, self.column-1)
			if param == 'jump':
				if 'jump' not in self.command:
					self.command += ['jump']
				self.velocityZ = 0.04
				self.positionZ += self.velocityZ 

	def update(self):
		print self.command
		if len(self.command) > 0 and 'jump' in self.command:
			self.velocityZ -= 0.005
			self.positionZ += self.velocityZ
			print self.positionZ
			if abs(self.positionZ - 0) < 0.001:
				self.positionZ = 0
				self.velocityZ = 0
				self.command.remove("jump")
		elif self.positionZ != 0 or (self.positionZ == 0 and self.mapGrid.mapGrid[int(self.distXTraveled+1)][self.column+1] == 0 and len(self.command) == 0):
			self.velocityZ -= 0.01
			self.positionZ += self.velocityZ
			self.command = ["fall"]
		if len(self.command) > 0 and 'left' in self.command:
			self.positionY = min(self.targetCol, self.positionY + 0.25)
			if self.positionY == self.targetCol:
				self.column = self.targetCol
				self.command.remove("left")
		if len(self.command) > 0 and 'right' in self.command:
			self.positionY = max(self.targetCol, self.positionY - 0.25)
			if self.positionY == self.targetCol:
				self.column = self.targetCol
				self.command.remove("right")
		self.distXTraveled += 0.1
		self.positionZ += self.velocityZ