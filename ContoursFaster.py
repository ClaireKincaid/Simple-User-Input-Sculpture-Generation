from stl import mesh
import time
import pickle
import os
from skimage import measure
from noise import pnoise3, snoise3
import numpy as np
import cv2
import pyglet
from mayavi import mlab
from solid_extrude import solid_extrude
from bloby_extrude import bloby_extrude
import math

def create_iso_surface(volume_data):
	width = len(volume_data)
	src = mlab.pipeline.scalar_field(volume_data)
	mlab.pipeline.iso_surface(src, contours=[volume_data.min()+0.4*volume_data.ptp(), ])
	mlab.show()

	solid = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
	for i, f in enumerate(faces):
		for j in range(3):
			solid.vectors[i][j] = verts[f[j],:]

	
	solid.save(name)

def three_d_print(volume_data):
	b =  raw_input('What resolution? (enter an int between 0 and 6, where 0 is highest resolution):\n')
	name = raw_input('What should the filename be?') + '.stl'
	

	verts, faces = measure.marching_cubes(volume_data, 0)

	solid = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
	for i, f in enumerate(faces):
		for j in range(3):
			solid.vectors[i][j] = verts[f[j],:]

	
	solid.save(name)

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

def bool_ops(perlin_noise, image, width, para_func):
	"""Allows the user to write mathmatical definitions for solids and use boolian operations on them."""
	start = time.time()
	x = np.zeros((width, width, width))
	v = np.fromfunction(para_func, (width, width, width))
	v = x + v
	v = np.lib.pad(v, ((1,1),(1,1),(1,1)), 'constant') #This padds the z axis with zero's arrays so that a closed shape is produced by marching cubes.
	return v


def test_solid(x,y,z):
	x = (x-center_u[0])/scale_u
	y = (y-center_u[1])/scale_u
	z = (z-center_u[2])/scale_u
	a = (x-y+z > .1)
	b = (x+y-z < .3)

	print "x:{}\ny:{}\nz:{}".format(x.shape, y.shape, z.shape)

	c = (x-.2)**2+np.cos(x-.2)*y**2+z**2 + 2*z*y*x < .8
	d = x**2+y**2+z**2 < 2
	e = (x+y-z > .7)
	f = (x+y-z < .8)
	return np.logical_and(np.logical_or(np.logical_and(np.logical_or(np.logical_and(a, b), c), d), np.logical_and(e,f)), d)

def post_process_solid():
	pass

def create_image_matrix(image, perlin_noise, degrees=180):
	"""This creates a 3d matrix of an image with rotations acting in the xy plane"""
	width = len(image)
	rows,cols = image.shape
	v = np.zeros((width, width, width))

	
	for z in range(width):
		# M = cv2.getRotationMatrix2D((cols/2,rows/2),z*degrees/width,1)
		dyn_img = cv2.resize(image, (int(np.cos(z/width)*width+10), width-z+10))
		# dst = cv2.warpAffine(dyn_img, M,(cols/2,rows/2))

		v[:][z][:] += cv2.warpAffine(dyn_img,M,(cols,rows)) 

	v = np.lib.pad(v, ((1,1),(1,1),(1,1)), 'constant') #This padds the z axis with zero's arrays so that a closed shape is produced by create_iso_surface.
	return v




def create_sculpture(user_filename='Circle.png', times_compressed=1, noise_filename='loaded_noise.p', matrix_width=240, ans_print=False, letter='b'):
	"""Creates a matrix that is then rendered which represents the sculpture"""

	#First we define the resolution of perlin noise, how much to compress the sculpture, and we do the same to the image
	resolution = 6/float(matrix_width) #This is a reasonable resolution I found for the Perlin Noise
	factor = 2**times_compressed
	img = cv2.imread(user_filename, 0)
	img = cv2.resize(img, (matrix_width/factor, matrix_width/factor))
	
	perlin_noise = compress_noise(load_noise(noise_filename, matrix_width, resolution), times_compressed)

	width = len(perlin_noise)

	real_scale = 1.0
	scale_u = width/(3*real_scale)
	center_u = [width/2, width/2, width/2]
	global scale_u, center_u

	if ans_print == False:

		a = raw_input('What type of operation would you like to do?(b - bloby_extrude, s - solid_extrude, i - create_image_matrix, c - bool_ops :\n')
		global a
		if a == 'b':
			return bloby_extrude(img, perlin_noise)
		elif a == 's':
			return solid_extrude(img, width)
		elif a == 'i':
			return create_image_matrix(img, perlin_noise, 360)
		elif a == 'c':
			return bool_ops(perlin_noise, img, width, test_solid)
	else:
		if a == 'b':
			three_d_print(bloby_extrude(img, perlin_noise))
		elif a == 's':
			three_d_print(solid_extrude(img, width))
		elif a == 'i':
			three_d_print(create_image_matrix(img, perlin_noise, 360))
		elif a == 'c':
			three_d_print(bool_ops(perlin_noise, img, width))

if __name__ == '__main__':

	win = pyglet.window.Window(width=720, height=720, resizable=True, visible=False,
		config=pyglet.gl.Config(sample_buffers=1, samples=4, double_buffer=True, depth_size=24))

	create_iso_surface(create_sculpture('MX.png', 2, 'loaded_noise3.p', 240))

	i = raw_input("Do you want to export this as an stl (y/n)?\n")
	if i == 'y':
		create_sculpture('MX.png', 0, 'loaded_noise3.p', 240, True, 'b')
		