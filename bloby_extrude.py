import numpy as np

def bloby_extrude(perlin_noise, image):
	normalized_pixels = np.array(image/255.0)
	print normalized_pixels
	input_with_noise = perlin_noise * np.sqrt(normalized_pixels)  + np.power(normalized_pixels, 6)
	input_with_noise[input_with_noise<0.9] = input_with_noise[input_with_noise<0.9] +0.1
	# input_with_noise[input_with_noise > 1] = 1
	input_with_noise = np.lib.pad(input_with_noise, ((1,1),(1,1),(1,1)), 'constant') #This padds the z axis with zero's arrays so that a closed shape is produced by create_iso_surface.
	return input_with_noise - .9