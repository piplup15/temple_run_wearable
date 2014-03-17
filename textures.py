import OpenGL 
OpenGL.ERROR_ON_COPY = True 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import PIL.Image
import numpy

from PIL import Image
from PIL import ImageFont, ImageDraw

def loadTexture(name):

	im = PIL.Image.open(name)
	try:
		ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
	except SystemError:
		ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)

	pix = im.load()
	lst = []
	for i in range(im.size[0]):
		lst.append([])
		for j in range(im.size[1]):
			lst[i].append([])
			for k in range(3):
				lst[i][j].append(0)

	for i in range(im.size[0]):
		for j in range(im.size[1]):
			for k in range(3):
				lst[i][j][k] = pix[(i, im.size[1] - 1 - j)][k]

	image = numpy.array(lst, 'B')

	id = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, id)
	glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
	return id

def loadFont():
	textHash = {}
	characters = ['0','1','2','3','4','5','6','7','8','9','S','C','O','R','E','U','N']
	characters += [' ','gF','gA','gS','gT','gE','gR','g.', 'rR', 'oA', 'yI', 'gN', 'cB', 'bO', 'pW']
	characters += ['T','A','G','M','V']
	for char in characters:
		im = Image.new("RGBA", (98, 98), (100,100,100,0))
		usr_font = ImageFont.truetype("yoshisst.ttf", 120)
		d_usr = ImageDraw.Draw(im)
		d_usr.fontmode = "1"
		ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
		if len(char) == 2 and char[0] == 'r':
			d_usr.text((10,0), char[1], (255,50,50, 200), font=usr_font)
		elif len(char) == 2 and char[0] == 'o':
			d_usr.text((10,0), char[1], (255,125,50, 200), font=usr_font)
		elif len(char) == 2 and char[0] == 'y':
			d_usr.text((10,0), char[1], (255,255,50, 200), font=usr_font)
		elif len(char) == 2 and char[0] == 'g':
			d_usr.text((10,0), char[1], (50,255,50, 200), font=usr_font)
		elif len(char) == 2 and char[0] == 'c':
			d_usr.text((10,0), char[1], (50,255,255, 200), font=usr_font)
		elif len(char) == 2 and char[0] == 'b':
			d_usr.text((10,0), char[1], (50,150,150, 200), font=usr_font)
		elif len(char) == 2 and char[0] == 'p':
			d_usr.text((10,0), char[1], (50,50,255, 200), font=usr_font)
		else:
			d_usr.text((10,0), char, (200,200,200, 255), font=usr_font)
		pix = im.load()
		lst = []
		for i in range(im.size[0]):
			lst.append([])
			for j in range(im.size[1]):
				lst[i].append([])
				for k in range(4):
					lst[i][j].append(0)

		for i in range(im.size[0]):
			for j in range(im.size[1]):
				for k in range(4):
					lst[i][j][k] = pix[(im.size[0] - 1 - i, j)][k]

		image = numpy.array(lst, 'B')

		id = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, id)
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
		textHash[char] = id
	return textHash