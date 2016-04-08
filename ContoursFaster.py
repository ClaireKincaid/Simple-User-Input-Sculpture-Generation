from stl import mesh
import time
import pickle
import os
import math
from pyglet.gl import *
import ctypes
import noise
from noise import pnoise3, snoise3
import numpy as np
import cv2
import sys
from mpl_toolkits.mplot3d import Axes3D
import pylab
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure
import sympy




def marching_cubes(volume_data):
	data_size = len(volume_data)

	# Use marching cubes to obtain the surface mesh of the volume data
	verts, faces = measure.marching_cubes(volume_data, 0)
	print faces
	print verts
	# Create the mesh
	solid = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
	for i, f in enumerate(faces):
	    for j in range(3):
	        solid.vectors[i][j] = verts[f[j],:]

	solid.save('solid2.stl')
	print len(verts)

	# Display resulting triangular mesh using Matplotlib. This can also be done
	# with mayavi (see skimage.measure.marching_cubes docstring).
	fig = plt.figure(figsize=(10, 10))
	ax = fig.add_subplot(111, projection='3d')

	# Fancy indexing: `verts[faces]` to generate a collection of triangles
	mesh2 = Poly3DCollection(verts[faces])
	print mesh2
	ax.add_collection3d(mesh2)

	ax.set_xlabel("x-axis: a = 6 per ellipsoid")
	ax.set_ylabel("y-axis: b = 10")
	ax.set_zlabel("z-axis: c = 16")

	ax.set_xlim(0, data_size+2)  # a = 6 (times two for 2nd ellipsoid)
	ax.set_ylim(0, data_size+2)  # b = 10
	ax.set_zlim(0, data_size+2)  # c = 16

	plt.show()





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

def bloby_extrude(perlin_noise, image):
	normalized_pixels = np.array(image/255.0)
	input_with_noise = perlin_noise * np.sqrt(normalized_pixels) + np.power(normalized_pixels, 6)
	input_with_noise[input_with_noise<0.9] = input_with_noise[input_with_noise<0.9] +0
	input_with_noise[input_with_noise > 1] = 1
	input_with_noise = np.lib.pad(input_with_noise, ((1,1),(1,1),(1,1)), 'constant') #This padds the z axis with zero's arrays so that a closed shape is produced by marching cubes.
	return input_with_noise

def sphere(perlin_noise, image, width):
	start = time.time()
	v = np.zeros((width, width, width))
	size = np.linspace(-math.pi,math.pi, 4*width)
	# for t in size:
	# 	for s in size:
	# 		x = math.sin(t)*math.cos(s)
	# 		y = math.sin(t)*math.sin(s)
	# 		z = math.cos(t)
	# 		v[int(width*x)/2+width/2][int(width*y)/2+width/2][int(width*z)/2+width/2] = 1


	# for x in size:
	# 	for y in size:
	# 		for z in size:
	# 			try: 
	#  				if x**2 + x*y + 2*z**2 < 1:
	#  					v[int(width*x)/math.pi+width/2-1][int(width*y)/math.pi+width/2-1][int(width*z)/math.pi+width/2-1] = 1
	#  			except IndexError:
	#  				pass

	v = np.fromfunction(parametric_solid, (width, width, width))
	v = np.lib.pad(v, ((1,1),(1,1),(1,1)), 'constant') #This padds the z axis with zero's arrays so that a closed shape is produced by marching cubes.
	end = time.time()
	print end - start
	return v

def parametric_solid(x,y,z):
	x = (x-center_u[0])/scale_u
	y = (y-center_u[1])/scale_u
	z = (z-center_u[2])/scale_u
	a = (x+y-z > .1)
	b = (x+y-z < .3)
	c = (x-.2)**2+np.sin(x-.2)*y**2+z**2 < .8
	return np.logical_or(np.logical_and(a, b), c)




def solid_extrude(perlin_noise, image, width):
	normalized_pixels = np.array(image/255.0)
	v = np.zeros((width, width, width))
	input_with_noise = v + normalized_pixels
	input_with_noise[input_with_noise > 1] = 1
	input_with_noise = np.lib.pad(input_with_noise, ((1,1),(1,1),(1,1)), 'constant') #This padds the z axis with zero's arrays so that a closed shape is produced by marching cubes.
	return input_with_noise > .4

def create_3d_volume(perlin_noise, scale, image):
	"""Create a grayscale 3d texture map with the specified 
	pixel width on each side and load it into the current texture
	unit. The luminace of each texel is derived using the input 
	function as:

	v = func(x * scale, y * scale, z * scale)
	where x, y, z = 0 in the center texel of the texture.
	func(x, y, z) is assumed to always return a value in the 
	range [-1, 1].
	"""
	data_size = len(perlin_noise)
	zero_flat = np.zeros((data_size, data_size))
	real_scale = 1.0
	
	scale_u = data_size/(3*real_scale)
	print 'scale = '+ str(scale_u)
	center_u = [data_size/2, data_size/2, data_size/2]
	print 'center = '+ str(center_u)
	global scale_u, center_u
	input_with_noise = sphere(perlin_noise, image, data_size)



	
	return input_with_noise > 0.4

def create_sculpture(user_filename='Circle.png', times_compressed=1, noise_filename='loaded_noise.p', matrix_width=240):
	"""Creates a matrix that is then rendered which represents the sculpture"""
	resolution = 6/float(matrix_width) #This is a reasonable resolution I found for the Perlin Noise
	factor = 2**times_compressed
	img = cv2.imread(user_filename, 0)
	img = cv2.resize(img, (matrix_width/factor, matrix_width/factor))
	perlin_noise = compress_noise(load_noise(noise_filename, matrix_width, resolution), times_compressed)
	return create_3d_volume(perlin_noise, resolution, img)

if __name__ == '__main__':

	win = pyglet.window.Window(width=720, height=720, resizable=True, visible=False,
		config=pyglet.gl.Config(sample_buffers=1, samples=4, double_buffer=True, depth_size=24))

	marching_cubes(create_sculpture('MX.png', 1, 'loaded_noise3.p', 240))
	