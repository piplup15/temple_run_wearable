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

class Diamond():
	def __init__(self, row, column):
		self.row = row
		self.column = column
		self.rotateangle = 0
		self.stp = random.random()*5 + 7.5

		val = random.random()
		if val < 0.02:
			self.re = 0.55
			self.be = 0.55
			self.ge = 0.55		
			self.rd = 0.55
			self.bd = 0.55
			self.gd = 0.55
			self.rs = 0.55
			self.bs = 0.55
			self.gs = 0.55
			self.value = 10000			
		elif val < 0.1:
			self.re = 0.8
			self.be = 0.2
			self.ge = 0.25		
			self.rd = 0.8
			self.bd = 0.3
			self.gd = 0.4
			self.rs = 0.8
			self.bs = 0.3
			self.gs = 0.4
			self.value = 5000
		else:
			self.re = 0.2
			self.be = 0.5
			self.ge = 0.3		
			self.rd = 0.2
			self.bd = 0.5
			self.gd = 0.3
			self.rs = 0.2
			self.bs = 0.5
			self.gs = 0.3
			self.value = 1000

	def update(self):
		self.rotateangle += self.stp

	def draw(self, ambient, diffuse, specular, emission, shininess):

		glPushMatrix()
		glUniform4fv(ambient, 1, numpy.array([0.0, 0.0, 0.0, 0.0], numpy.float32))
		glUniform4fv(emission, 1, numpy.array([self.re, self.ge, self.be, 0.7], numpy.float32))
		glUniform4fv(diffuse, 1, numpy.array([self.rd, self.gd, self.bd, 0.7], numpy.float32))
		glUniform4fv(specular, 1, numpy.array([self.rs, self.gs, self.bs, 0.7], numpy.float32))
		glUniform1f(shininess, 4)

		glPopMatrix()

		glPushMatrix()
		glTranslatef(self.row-0.5, -0.2 + self.column*0.2, 0.25)
		glRotatef(self.rotateangle, 0, 0 ,1)
		glScalef(1, .7, 1)
		glRotatef(45, 1, 0 ,0)
		glScalef(0.05, 0.05, 0.05)
		glScalef(.2, 1, 1)
		#glScalef(1, 2, 1)
		#glScalef(1, 1, 1)
		glutSolidCube(3)

		glPopMatrix()