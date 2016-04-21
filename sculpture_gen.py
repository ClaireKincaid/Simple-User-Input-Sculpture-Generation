print "Loading libraries..."
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
print "Done"

class Sculpture:
	def __init__(self):
		self.noise_file = 'loaded_noise4.p'
		self.matrix_size = 240
		self.noise_scale = 3/float(240)
		self.noise = self.load_noise()
		self.scale = self.matrix_size/(3)
		
	def load_noise(self):
		"""This function finds out if a filename exists, and if it does, then
		it loads the file and uses that as the matrix of perlin noise. If it doesn't
			exist, it calls the function create_noise"""
		print "Loading noise..."
		filestring = "./" + self.noise_file  #Assuming the file is in the current working directory
		if os.path.exists(filestring):  #This does not check if the file is the right type, but simply if it exists
			noise_open = open(self.noise_file, "rb")
			loaded_noise = pickle.load(noise_open)
		else:
			loaded_noise = self.create_noise()
			noise_open = open(self.noise_file, "wb")
			pickle.dump(loaded_noise, noise_open)
		print "Done"
		return loaded_noise

	def create_noise(self):
		matrix_size = self.matrix_size
		scale = self.noise_scale
		coords = range(matrix_size)

		v = np.zeros((matrix_size, matrix_size, matrix_size))
		for z in coords:
			for y in coords:
				for x in coords:
					v[x][y][z] = (pnoise3(x * scale, y * scale , z * scale, octaves=8, persistence=.25) + 1.0)/2.0
		return v

	def compress_noise(self, times):
		"""This function compresses a 3-d matrix in half by taking every other value."""
		factor = 2**times    
		width = len(self.noise)
		coords = range(width/factor)
		v = np.zeros((width/factor, width/factor, width/factor))
		for z in coords:
			for y in coords:
				for x in coords:
					v[x][y][z] = self.noise[factor*x][factor*y][factor*z]
		return v

	def create_transform_matrix(self):
		"""This function creates a transformation 3d matrix based on user text input"""
		width = len(image)

	
		for z in range(self.matrix_size):
			M = cv2.getRotationMatrix2D((self.matrix_size/2,self.matrix_size/2),z*degrees/self.matrix_size,1)

			dyn_img = cv2.resize(image, (int(np.cos(z/width)*width+10), width-z+10))
			dst = cv2.warpAffine(dyn_img, M,(self.matrix_size/2,self.matrix_size/2))

			v[:][z][:] += cv2.warpAffine(dyn_img,M,(cols,rows))

	def bool_ops(self):
		"""Allows the user to write mathmatical definitions for solids and use boolian operations on them."""
		x = np.zeros((self.matrix_size, self.matrix_size, self.matrix_size))
		v = np.fromfunction(self.test_solid, (self.matrix_size, self.matrix_size, self.matrix_size))
		v = x + v
		v = np.lib.pad(v, ((1,1),(1,1),(1,1)), 'constant') #This padds the z axis with zero's arrays so that a closed shape is produced by marching cubes.
		return v


	def test_solid(self, x,y,z):
		x = (x-self.matrix_size/2)/self.scale
		y = (y-self.matrix_size/2)/self.scale
		z = (z-self.matrix_size/2)/self.scale
		a = eval(self.user_text)
		return a

	def bloby_extrude(self):
		normalized_pixels = np.array(my_sculpture.img/255.0)
		input_with_noise = self.noise * np.sqrt(normalized_pixels)  + np.power(normalized_pixels, 6)
		input_with_noise[input_with_noise<0.9] = input_with_noise[input_with_noise<0.9] +0.1
		# input_with_noise[input_with_noise > 1] = 1
		input_with_noise = np.lib.pad(input_with_noise, ((1,1),(1,1),(1,1)), 'constant') #This padds the z axis with zero's arrays so that a closed shape is produced by create_iso_surface.
		return input_with_noise - .9

	def interpret_input(self):
		"""Intreprets the user input and returns a lambda function that will generate a transformation matrix \
		based on the input"""
		pass

	def create_iso_surface(self, threshold):
		volume_data = self.volume_data
		width = len(volume_data)
		src = mlab.pipeline.scalar_field(volume_data)
		mlab.pipeline.iso_surface(src, contours=[volume_data.min()+threshold*volume_data.ptp(), ])
		mlab.show()


	def get_input(self, filename=False, sculp_res=False, operation=False, update_noise=False):
		"""This grabs user input, and returns the value of that input based on what input was requested."""

		if filename:
			res = raw_input('What should the filename be(input a string)?\n') + '.stl'

		if sculp_res:
			res = int(raw_input('What resolution of model would you like?\n(0 = 240x240x240, 1 = 120x120x120, 2 = 60x60x60, etc.)\n'))

		if operation:
			res = raw_input('Enter the mode of operation you would like to use:\n \
				m = mathmatically defined sculpture, uses boolean operations. \n \
				i = creates a sculpture based on an image and transformations called by the user. \n \
				b = creates a bloby sculpture by taking user images and creating an organic sculpture \
				inspired by the input images.')

		if update_noise:
			ans = raw_input('Enter a new resolution of noise, or press d for default. \n \
				(resolution is a value between 0.5 and 20)')
			if ans == 'd':
				res = self.noise_scale
			else:
				res = ans
		return res

	def update(self):
		"""Updates the information in the sculpture class"""
		


my_sculpture = Sculpture()
my_sculpture.noise_file = 'test_noise.p'
my_sculpture.small_noise = my_sculpture.compress_noise(1)
my_sculpture.volume_data = np.lib.pad(my_sculpture.small_noise, ((1,1),(1,1),(1,1)), 'constant')

while True:
	
	a = raw_input("Would you like to play a game?")
	if a == 'y':
		res = my_sculpture.get_input(operation=True)
		if res == 'm':
			while True:
				res = raw_input("Enter a functional definition of a volume (x**2+y**2+z**2 < 1) \n")
				my_sculpture.user_text = res
				my_sculpture.volume_data = my_sculpture.bool_ops()
				my_sculpture.create_iso_surface(.7)
				res = raw_input("Enter a boolean operation to do with the previous solid (a = and, o = or, n = not, x = xor):\n")
				if res == "a":
					my_sculpture.volume_data = 0+ np.logical_and(my_sculpture.volume_data, my_sculpture.bool_ops())
				elif res == "o":
					my_sculpture.volume_data = 0+ np.logical_or(my_sculpture.volume_data, my_sculpture.bool_ops())
				elif res == "n":
					my_sculpture.volume_data = 0+ np.logical_not(my_sculpture.volume_data, my_sculpture.bool_ops())
				elif res == "x":
					my_sculpture.volume_data = 0+ np.logical_xor(my_sculpture.volume_data, my_sculpture.bool_ops())
		if res == 'b':
			user_filename = raw_input("Enter an image filename to be inspired by. \n")
			my_img = cv2.imread(user_filename, 0)
			my_sculpture.img = cv2.resize(my_img, (my_sculpture.matrix_size, my_sculpture.matrix_size))
			my_sculpture.volume_data = my_sculpture.bloby_extrude()
			my_sculpture.create_iso_surface(.7)
			
	else:
		break