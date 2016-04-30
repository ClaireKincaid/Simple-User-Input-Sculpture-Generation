print "Loading libraries..."
import threading
import time
import pickle
import os
from skimage import measure
import numpy as np
from stl import mesh
import cv2
import pyglet
from mayavi import mlab
from traits.api import HasTraits, Instance,  Range, on_trait_change
from traitsui.api import View, Item, HGroup
from mayavi.core.ui.api import SceneEditor, MlabSceneModel
from textblob import TextBlob
from noise import pnoise3, snoise3
import random
print "Done"




class Sculpture(HasTraits):
    def __init__(self):
        self.noise_file = 'loaded_noise4.p' #Initializes the noise as a pickled file.
        self.matrix_size = 120  #pixels
        self.noise_scale = 3/float(240)  #the scale perlin noise is generated at.
        self.noise = self.load_noise()
        self.small_noise = self.compress_noise(1)
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
        """If a noise file was not found, this will create a noise file using pnoise3"""

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

    def bloby_extrude(self, threshold):

        self.img_cp = cv2.resize(self.img, (self.matrix_size, self.matrix_size))
        normalized_pixels = np.array(self.img_cp/255.0)
        input_with_noise = self.small_noise * np.sqrt(normalized_pixels)  + np.power(normalized_pixels, 6)
        input_with_noise[input_with_noise<0.9] = input_with_noise[input_with_noise<0.9] +0.1
        # input_with_noise[input_with_noise > 1] = 1
        input_with_noise = np.lib.pad(input_with_noise, ((1,1),(1,1),(1,1)), 'constant') #This padds the z axis with zero's arrays so that a closed shape is produced by create_iso_surface.
        input_with_noise[input_with_noise>threshold] = 1
        return input_with_noise


    def create_iso_surface(self, threshold, second=False):
        volume_data=self.volume_data  #Sets the volume data as that of the sculpture
        if second:   #Checks if this volume is supposed to be the second volume in a boolean operation
            volume_data = self.sec_volume_data  #Sets volume data to that of the second for a boolean opperation

        width = len(volume_data)
        src = mlab.pipeline.scalar_field(volume_data)
        mlab.pipeline.iso_surface(src, contours=[volume_data.min()+threshold*volume_data.ptp(), ])
        mlab.show()


    def get_input(self, filename=False, sculp_res=False, operation=False, update_noise=False):
        """This grabs user input, and returns the value of that input based on what input was requested."""

        if filename:
            res = raw_input('What should the filename be(input a string, ex: my_file)?\n') + '.stl'

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

    def run_ui(self):
        """This runs the overall menu for the user"""
        res = self.get_input(operation=True)  #Checks what menu item the user wants
        if res == 'm':   #This is the mathmatically defined sculpture menu item
            self.m_menu()
                
        if res == 'b':
            self.b_menu()
            
    def m_menu(self):
        """Runs the Mathmatically defined sculpture menu item."""
        sin, cos = np.sin, np.cos
        res = raw_input("Enter a functional definition of a volume (x**2+y**2+z**2 < 1) \n")
        self.user_text = res
        self.volume_data = self.bool_ops()
        self.create_iso_surface(.7)
        
        while True:
            
            res = raw_input("Enter another functional definition of a volume (x**2+y**2+z**2 < 1) \n")
            self.user_text = res
            self.sec_volume_data = self.bool_ops()
            self.create_iso_surface(.7, second=True)
            res = raw_input("Enter a boolean operation to do with the previous solid (a = and, o = or, n = not, x = xor):\n")
            if res == "a":
                self.sec_volume_data = 0+ np.logical_and(my_sculpture.volume_data, my_sculpture.bool_ops())
            elif res == "o":
                self.sec_volume_data = 0+ np.logical_or(my_sculpture.volume_data, my_sculpture.bool_ops())
            elif res == "n":
                self.sec_volume_data = 0+ np.logical_not(my_sculpture.volume_data, my_sculpture.bool_ops())
            elif res == "x":
                self.sec_volume_data = 0+ np.logical_xor(my_sculpture.volume_data, my_sculpture.bool_ops())
            self.create_iso_surface(.7, second=True)

    def b_menu(self):
        """Runs the blobby extrude menu itme."""
        user_filename = raw_input("Enter an image filename to be inspired by. \n")
        my_img = cv2.imread(user_filename, 0)
        self.img = cv2.resize(my_img, (self.matrix_size, self.matrix_size))
        self.volume_data = self.bloby_extrude(.4)
        Visualization().configure_traits()
        self.create_iso_surface(.4)

    # def i_menu(self):
    #     """Runs the image transformation menu item."""
    def transform_matrix(self):
        """Creates a transformation matrix to impose on 3d volume data."""


    def create_image_matrix(self, degrees=180):
        """This creates a 3d matrix of an image with rotations acting in the xy plane"""
        #This code is not yet integrated into the menu, but it works. It needs
        #to be able to take user text input to create transformation matrices that 
        #can act on any volume data.

        width = self.matrix_size
        rows,cols = self.img_cp.shape   #Image cp is the compressed image. 
        v = np.zeros((width, width, width))

        
        for z in range(width):
            M = cv2.getRotationMatrix2D((cols/2,rows/2),z*degrees/width,1)      #This finds the rotation matirx
            dyn_img = cv2.resize(image, (int(np.cos(z/width)*width+10), width-z+10))        #Resizes the image throughout the z axis based on a mathematical function.
            dst = cv2.warpAffine(dyn_img, M,(cols/2,rows/2))                    #This applies the rotation matrix to the image.

            v[:][z][:] += cv2.warpAffine(dyn_img,M,(cols,rows)) 

        v = np.lib.pad(v, ((1,1),(1,1),(1,1)), 'constant') #This padds the z axis with zero's arrays so that a closed shape is produced by create_iso_surface.
        return v



    def three_d_print(self):
        """This will produce a 3d printable stl based on self.volume_data. It is to be used for the final "print" button, and needs to be fed high quality data."""

        name = raw_input('What should the filename be?') + '.stl'
        

        verts, faces = measure.marching_cubes(self.volume_data, 0)   #Marching Cubes algorithm

        solid = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                solid.vectors[i][j] = verts[f[j],:]

        
        solid.save(name)


#Here be UI    


class Visualization(HasTraits):
    threshold = Range(0, 1., .5)
    compression = Range(0,6, 2)

    scene   = Instance(MlabSceneModel, ())

    def __init__(self):
        HasTraits.__init__(self)
        volume_data = my_sculpture.bloby_extrude(self.threshold)
        self.plot = self.scene.mlab.contour3d(volume_data)

    @on_trait_change('threshold,compression')#Add variable you want sliders or other buttons to this string
    def update_plot(self):
        self.scene.mlab.clf()
        my_sculpture.matrix_size = 120/(2**self.compression)    #Modify the value that you called to update
        if len(my_sculpture.small_noise) != my_sculpture.matrix_size:   #Checks if the compression has already been evaluated.
            my_sculpture.small_noise = my_sculpture.compress_noise(self.compression)

        volume_data = my_sculpture.bloby_extrude(self.threshold)    #Sets the new volume data to be evaluated at the new thresholded value
        src = mlab.pipeline.scalar_field(volume_data)
        mlab.pipeline.iso_surface(src, contours=[volume_data.min()+self.threshold*volume_data.ptp(), ])   #Use pipeline to reevaluate the data and replot it.
        # self.plot.mlab_source.set(volume_data=volume_data)


    view = View(Item('scene', height=300, show_label=False,
                    editor=SceneEditor()),
                HGroup('threshold', 'compression'), resizable=True)  #Remember to put in the sliders you want in here.




if __name__ == '__main__':

    my_sculpture = Sculpture()
    my_sculpture.noise_file = 'test_noise.p'
    my_sculpture.noise = my_sculpture.compress_noise(240/my_sculpture.matrix_size - 1)
    my_sculpture.volume_data = np.lib.pad(my_sculpture.noise, ((1,1),(1,1),(1,1)), 'constant')
    
    while True:

        a = raw_input("How do you feel about sculptures?")
        blob = TextBlob(a)
        sentiment = blob.sentiment.polarity  #Performs sentiment analysis on the answer.
        print sentiment
        if sentiment >= 0:
            my_sculpture.run_ui()
        else:
            x = random.choice(range(5))
            if x == 0:
                print "I'm sorry you are so bitter."
            elif x == 1:
                print "I love sculptures. I hope you learn to appreciate them one day."
            elif x == 2:
                print "Wow. I expected better from you."
            elif x == 3:
                print "I guess art is truly dead."
            elif x == 4:
                print "You break my heart."
            break
