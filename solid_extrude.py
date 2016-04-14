import numpy as np

def solid_extrude(image, width):
	"""This 'extrudes' an input image and creates a 3d matrix"""
	v = np.zeros((width, width, width)) #We initialize our 3d matrix.
	normalized_pixels = np.array(image/255.0) #This makes all image values between 0 and 1
	
	output = v + normalized_pixels 
	
	output = np.lib.pad(output, ((1,1),(1,1),(1,1)), 'constant') #This padds the z axis with zero's arrays so that a closed shape is produced by create_iso_surface.
	return output