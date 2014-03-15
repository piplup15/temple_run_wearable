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

boxSize = 200
textureRepeatSize = 10

def display(starrySkyTex, isTex):

	glUniform1i(isTex, 1)

	glPushMatrix()
	glEnable(GL_TEXTURE_2D)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) 
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) 
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) 
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) 
	glBindTexture(GL_TEXTURE_2D, starrySkyTex)

	glBegin(GL_QUADS);
	glTexCoord2f(0.0, textureRepeatSize); glVertex3f(boxSize, -boxSize, -boxSize)
	glTexCoord2f(textureRepeatSize, textureRepeatSize); glVertex3f(boxSize, -boxSize, boxSize)
	glTexCoord2f(textureRepeatSize, 0.0); glVertex3f(boxSize, boxSize, boxSize)
	glTexCoord2f(0.0, 0.0); glVertex3f(boxSize, boxSize, -boxSize)
	glEnd()

	glBegin(GL_QUADS);
	glTexCoord2f(0.0, textureRepeatSize); glVertex3f(-boxSize, -boxSize, -boxSize)
	glTexCoord2f(textureRepeatSize, textureRepeatSize); glVertex3f(-boxSize, -boxSize, boxSize)
	glTexCoord2f(textureRepeatSize, 0.0); glVertex3f(-boxSize, boxSize, boxSize)
	glTexCoord2f(0.0, 0.0); glVertex3f(-boxSize, boxSize, -boxSize)
	glEnd()

	glBegin(GL_QUADS);
	glTexCoord2f(0.0, textureRepeatSize); glVertex3f(-boxSize, boxSize, -boxSize)
	glTexCoord2f(textureRepeatSize, textureRepeatSize); glVertex3f(-boxSize, boxSize, boxSize)
	glTexCoord2f(textureRepeatSize, 0.0); glVertex3f(boxSize, boxSize, boxSize)
	glTexCoord2f(0.0, 0.0); glVertex3f(boxSize, boxSize, -boxSize)
	glEnd()

	glBegin(GL_QUADS);
	glTexCoord2f(0.0, textureRepeatSize); glVertex3f(-boxSize, -boxSize, -boxSize)
	glTexCoord2f(textureRepeatSize, textureRepeatSize); glVertex3f(-boxSize, -boxSize, boxSize)
	glTexCoord2f(textureRepeatSize, 0.0); glVertex3f(boxSize, -boxSize, boxSize)
	glTexCoord2f(0.0, 0.0); glVertex3f(boxSize, -boxSize, -boxSize)
	glEnd()

	glBegin(GL_QUADS);
	glTexCoord2f(0.0, textureRepeatSize); glVertex3f(-boxSize, -boxSize, boxSize)
	glTexCoord2f(textureRepeatSize, textureRepeatSize); glVertex3f(boxSize, -boxSize, boxSize)
	glTexCoord2f(textureRepeatSize, 0.0); glVertex3f(boxSize, boxSize, boxSize)
	glTexCoord2f(0.0, 0.0); glVertex3f(-boxSize, boxSize, boxSize)
	glEnd()

	glBegin(GL_QUADS);
	glTexCoord2f(0.0, textureRepeatSize); glVertex3f(-boxSize, -boxSize, -boxSize)
	glTexCoord2f(textureRepeatSize, textureRepeatSize); glVertex3f(boxSize, -boxSize, -boxSize)
	glTexCoord2f(textureRepeatSize, 0.0); glVertex3f(boxSize, boxSize, -boxSize)
	glTexCoord2f(0.0, 0.0); glVertex3f(-boxSize, boxSize, -boxSize)
	glEnd()

	glDisable(GL_TEXTURE_2D)
	glPopMatrix()

	glUniform1i(isTex, 0)