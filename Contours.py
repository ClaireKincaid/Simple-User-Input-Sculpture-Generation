import time
import pickle
import os
import math
import pyglet
from pyglet.gl import *
import ctypes
import noise
from noise import pnoise3, snoise3
import numpy as np
import cv2
import sys
global xrot, yrot, d

mywidth = 240


x = np.zeros((2, 3))
x[1][1] = 2
print x


def create_noise(width=240, scale=1.0/48):
	coords = range(width)
	v = np.zeros((width, width, width))
	for z in coords:
		for y in coords:
			for x in coords:
				v[x][y][z] = (pnoise3(x * scale, y * scale , z * scale, octaves=8, persistence=.25) + 1.0)/2.0
	return v

def compress_noise(big_noise, times):
	factor = 2**times
	width = len(big_noise)
	coords = range(width/factor)
	v = np.zeros((width/factor, width/factor, width/factor))
	for z in coords:
		for y in coords:
			for x in coords:
				v[x][y][z] = big_noise[factor*x][factor*y][factor*z]
	return v

def load_noise(filename, matrix_width, resolution):
	"""This function finds out if a filename exists, and if it does, then
	it loads the file and uses that as the matrix of perlin noise. If it doesn'try:
		exist, it calls the function create_noise"""

	filestring = "./" + filename  #Assuming the file is in the current working directory
	if os.path.exists(filestring):  #This does not check if the file is the right type, but simply if it exists
		noise_file = open(filename, "rb")
		loaded_noise = pickle.load(noise_file)
	else:
		loaded_noise = create_noise(matrix_width, resolution)
		noise_file = open(filename, "wb")
		pickle.dump(loaded_noise, noise_file)
	return loaded_noise


def create_3d_texture(perlin_noise, scale, image):
	"""Create a grayscale 3d texture map with the specified 
	pixel width on each side and load it into the current texture
	unit. The luminace of each texel is derived using the input 
	function as:

	v = func(x * scale, y * scale, z * scale)
	where x, y, z = 0 in the center texel of the texture.
	func(x, y, z) is assumed to always return a value in the 
	range [-1, 1].
	"""
	start = time.time()
	
	width = len(perlin_noise)
	coords = range(width)
	texel = (ctypes.c_byte * width**3)()
	half = 0 #width * scale / 2.0 
	
	for z in coords:
		for y in coords:
			for x in coords:
				v = (perlin_noise[x][y][z])# + 1.0)/2.0

				# v = v #* math.sqrt(imagenumber) # + imagenumber**6
				# texel[x + (y * width) + (z * width**2)] = int(v * 127.0)
				imagenumber = int(image[y][x])/255.0
				# if imagenumber > .7:
				# 	print imagenumber
				v = v * math.sqrt(imagenumber) + imagenumber**6
				if v < .9:
					v = v + .1
				elif v > 1:
					v = 1
				if v > .4:
					texel[x + (y * width) + (z * width**2)] = 127
				else: 
					texel[x + (y * width) + (z * width**2)] = 0
		
	glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
	glTexImage3D(GL_TEXTURE_3D, 0, GL_LUMINANCE, width, width, width, 0, 
		GL_LUMINANCE, GL_BYTE, ctypes.byref(texel))
	end = time.time()
	print end - start
	return texel

def create_sculpture(user_filename='MX.png', times_compressed=1, noise_filename='loaded_noise.p', matrix_width=240):
	"""Creates a matrix that is then rendered which represents the sculpture"""
	resolution = 6/float(matrix_width) #This is a reasonable resolution I found for the Perlin Noise

	factor = 2**times_compressed
	img = cv2.imread(user_filename, 0)
	img = cv2.resize(img, (matrix_width/factor, matrix_width/factor))
	perlin_noise = compress_noise(load_noise(noise_filename, matrix_width, resolution), times_compressed)
	return create_3d_texture(perlin_noise, resolution, img)

if __name__ == '__main__':

	win = pyglet.window.Window(width=720, height=720, resizable=True, visible=False,
		config=pyglet.gl.Config(sample_buffers=1, samples=4, double_buffer=True, depth_size=24))
	create_sculpture('MX.png', 1, 'loaded_noise.p', 240)
	glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glEnable(GL_TEXTURE_3D)
	xrot = yrot = d = 0

	def on_resize(width, height):
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(70, 1.0*width/height, 0.1, 1000.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
	win.on_resize = on_resize

	@win.event
	def on_mouse_motion(x, y, dx, dy):
		global xrot, yrot
		yrot += dx * 0.3
		xrot += dy * 0.3

	@win.event
	def on_draw():
		global xrot, yrot, d
		glClear(GL_COLOR_BUFFER_BIT)
		glLoadIdentity()
		glTranslatef(0, 0, -1.5)
		glRotatef(xrot, 1.0, 0.0, 0.0)
		glRotatef(yrot, 0.0, 1.0, 0.0)
		glBegin(GL_QUADS)
		glTexCoord3f(0.0, 0.0, d)
		glVertex3f(1, -1, 0)
		glTexCoord3f(0.0, 1.0, d)
		glVertex3f(1, 1, 0)
		glTexCoord3f(1.0, 1.0, d)
		glVertex3f(-1, 1, 0)
		glTexCoord3f(1.0, 0.0, d)
		glVertex3f(-1, -1, 0)
		glEnd()

	def update(dt):
		global d
		d += dt * 0.1
		if d > 1.0:
			d -= 1.0

	pyglet.clock.schedule_interval(update, 1/30.0)

	win.set_visible()
	win.set_exclusive_mouse()
	pyglet.app.run()


cv2.waitKey(0)
cv2.destroyAllWindows()