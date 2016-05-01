"""
A set of classes to define and transform shapes on a 2D coordinate axis,
designed for easy use with SolidPython.

Authors: Coleman Ellis, Claire Kincaid, Maximillian Schommer

SoftDes Spring 2016
"""

from numpy import pi
import numpy as np
from math import sqrt
import solid as sp
from solid.utils import *
from types import NoneType
# import cv2
import time
import subprocess32 as subprocess32

class Polygon(object):
    """Represents a polygon on a plane.

    Attributes: points (a list of tuples that represent coordinates)
    """

    def __init__(self, points=[(0,0)]):
        self.points = np.array(points)
        self.find_center()

    def find_center(self):
        sum_point = sum(self.points)
        centroid = sum_point/len(self.points)
        self.center = centroid

    def __str__(self):
        return str(self.points)

    def __repr__(self):
        return self.__str__()

    def __add__(self,other):
        #Add a 2D vector to translate the entire polygon
        return Polygon(self.points + other)

    def __mul__(self,other):
        #Multiply every point by a scalar
        return Polygon(self.points * other)

class n_Sided_Polygon(Polygon):
    """Generates a regular N sided polygon with a defined radius,
    centered at center.
    """

    def __init__(self, N = 3, radius = 1, center = (0,0), angle = 0):
        points = []
        angle = angle
        for n in range(N):
            x_coord = radius * np.cos(2*pi*n/N + angle) + center[0]
            y_coord = radius * np.sin(2*pi*n/N + angle) + center[1]
            points.append((x_coord,y_coord))
        super(n_Sided_Polygon,self).__init__(points)

class Square(n_Sided_Polygon):
    """Generates a square of side length l, centered at center.
    """

    def __init__(self, l = 2, center = (0,0), angle = pi/4):
        super(Square,self).__init__(4,sqrt(2)*l/2.0,center,angle)

class Circle(n_Sided_Polygon):
    """Generates a circle of radius r, centered on center
    """

    def __init__(self, r = 2, center = (0,0)):
        super(Circle,self).__init__(25,r,center,0)

"""Transformations"""
class Transformation(object):
    """As of yet, this just provides the __cmp__ function, which allows
    for sorting transformations.

    """
    def __init__(self):
        self.rank = 0

    def __cmp__(self, other):
        return self.rank-other.rank


class Rotation(Transformation):
    """A transformation that rotates a shape theta degrees about a given point.
    The rotation scales linearly with respect to z position.
    Stored as a 3D matrix, where each entry in the topmost list is a 2x2 rotation matrix.

    Attributes: theta (final angle rotated), center (point to rotate about), depth (number of layers)
    If center is None, rotates about the shape's center
    """

    def __init__(self,theta = 0, center = None, depth = 500):
        theta = theta * pi / 180.0
        trans_mat = [[[np.cos(theta/depth * i),-np.sin(theta/depth * i)],[np.sin(theta/depth * i),np.cos(theta/depth * i)]] for i in range(depth+1)]
        self.trans_mat = np.array(trans_mat)

        if center:
            self.center = np.array(center)
            self.rank = 5
        else:
            self.center = None
            self.rank = 1

class Dilation(Transformation):
    """A transformation that scales a shape by a given factor.
    The dilation scales linearly with respect to z position
    Stored as 3D matrix, where each entry in the topmost list is a 2x2 scaling matrix

    Attributes: scale_factor (the factor to scale to), depth
    """

    def __init__(self, scale_factor = 1, center = None, depth = 500):
        if center:
            self.center = np.array(center)
        else:
            self.center = None

        scale_factor = float(scale_factor)
        if scale_factor > 1:
            self.trans_mat = [[[1 + i*scale_factor/depth,0],[0,1 + i*scale_factor/depth]] for i in range(depth+1)]
        else:
            scale_factor = 1-scale_factor
            self.trans_mat = [[[1 - i*scale_factor/depth,0],[0,1 - i*scale_factor/depth]] for i in range(depth+1)]

        self.rank = 3

class Cosine_Harmonic_Dilation(Transformation):
    """A transformation that scales a shape by a given factor.
    The dilation scales based on a cosine with respect to z position
    Stored as 3D matrix, where each entry in the topmost list is a 2x2 scaling matrix

    Attributes: angle (cosine function runs from 0 to angle), center, depth
    """
    def __init__(self, angle = pi/2, center = None, depth = 500):
        if center:
            self.center = np.array(center)
        else:
            self.center = None

        self.trans_mat = [[[cos(float(i)/depth*angle),0],[0,cos(float(i)/depth*angle)]] for i in range(depth+1)]

        self.rank = 3

class Inward_Harmonic_Dilation(Transformation):
    """A transformation that scales a shape by a given factor.
    The dilation scales inward based on a sine with respect to z position.
    Results in a a shape that bows inward.
    Stored as 3D matrix, where each entry in the topmost list is a 2x2 scaling matrix

    Attributes: scale factor (smallest diameter/largest diameter), center, depth
    """


    def __init__(self, scale_factor = 1, center = None, depth = 500):
        if center:
            self.center = np.array(center)
        else:
            self.center = None

        scale_factor = float(1 - scale_factor)
        self.trans_mat = [[[1 - sin(float(i)/depth*pi)*scale_factor,0],[0,1 - sin(float(i)/depth*pi)*scale_factor]] for i in range(depth+1)]

        self.rank = 3

"""Animations"""
class Animation(object):
    """A collection of polygons and transformations, that can be exported
    to an openscad file or as a series of black and white images (volume data)

    Attributes: shapes (a dictionary whose keys are Polygons, and whose values are lists
    of transformations to apply to that polygon).
    """

    def __init__(self, polygon = Square(), transformations = [Rotation()]):
        self.shapes = {}
        self.shapes[polygon] = transformations
        self.final_shapes = None

    def add_shape(self, polygon = Square(), transformations = [Rotation()]):
        self.shapes[polygon] = transformations

    def render_shapes(self):
        """Inputs: none

        Output: Sets self.final_shapes to a 3D matrix. Each entry in the matrix
        is a matrix of two lists: a list of x coordinates and a list of corresponding
        y-coordinates. These represent all of the points along the edges of all defined
        shapes and their transformations as tored in self.shapes
        """
        
        final_shapes = []

        print "Animating Shapes"

        for shape, transformations in self.shapes.items():

            #Transformations that affect Polygons about their center need to be applied before those that rotate about specific points
            #This is to avoid having to recalculate the centers of shapes
            transformations.sort()
            
            #These matrix multiplications use the power of numpy matrix multiplication to very quickly apply transformations
            #to hundreds of points.

            #transformations[0].center is NoneType if the transformation is centered on the shape's center
            if type(transformations[0].center) is not NoneType:
                new_shape = shape.points - transformations[0].center
                new_shape = np.dot(transformations[0].trans_mat,new_shape.T)
                new_shape = new_shape + transformations[0].center.reshape(2,1)
            else:
                new_shape = shape.points - shape.center
                new_shape = np.dot(transformations[0].trans_mat,new_shape.transpose())
                new_shape = new_shape + shape.center.reshape(2,1)


            if len(transformations) > 1:
                for transformation in transformations[1:]:
                    if type(transformation.center) is not NoneType:
                        new_shape = new_shape - transformation.center.reshape(2,1)
                        new_shape = [np.dot(transformation.trans_mat[i],new_shape[i]) for i in range(len(transformation.trans_mat))]
                        new_shape = new_shape + transformation.center.reshape(2,1)
                    else:
                        new_shape = new_shape - shape.center.reshape(2,1)
                        new_shape = [np.dot(transformation.trans_mat[i],new_shape[i]) for i in range(len(transformation.trans_mat))]
                        new_shape = new_shape + shape.center.reshape(2,1)

            final_shapes.append(new_shape)
        
        self.final_shapes = final_shapes

    def render_points_as_image(self,points,bounds,resolution):
        """Inputs:
        Polygon data: a list of coordinates of points that
        define the corners of a polygon
        Bounds: The top right hand corner of the square inside which all
        of the points in the polygon data will fit (x,x) (these are technically
        coordinates, but they should be the same for the sake of squares)
        Resolution: The resolution of the output image; a single number,
        all output images are square
        Output: a black and white image (stored as a matrix of Booleans)."""

        output_image = np.zeros((resolution,resolution), dtype=bool)

        step_size = bounds[1] * 2.0 / resolution

        #Tack the first point onto the end, to make looping through
        #adjacent pairs of points easier
        points = np.append(points,[points[0]],axis = 0)

        #Make sure all points are positive
        points = points + bounds[1]

        #Scale the points so rounding them to whole numbers will place
        #them within the output resolution
        points = points / step_size

        #Round the points to prevent future rounding errors
        points = np.floor(points)

        for i in range(len(points)-1):
            #For each pair of points
            p1 = points[i]
            p2 = points[i+1]
    
            #Calculate the slope
            slope = (p2[1]-p1[1])/(p2[0]-p1[0])

            #Then for each step (of 1) in the y-direction from p1 to p2
            for y_step in range(int(np.abs(p2[1]-p1[1]))):
                if slope:
                    if p2[1] > p1[1]:
                        #Find which x value corresponds to the new y value (using the slope)
                        new_y = int(p1[1] + y_step)
                        new_x = int(p1[0] + y_step/slope)
                    else:
                        new_y = int(p1[1] - y_step)
                        new_x = int(p1[0] - y_step/slope)
                    #Then invert every pixel to the left of the new point.
                    #This very nicely fills in the shape, regardless of concavity/convexity.
                    output_image[-new_y][0:new_x] = np.logical_xor(True,output_image[-new_y][0:new_x])

        for point in points[:-1]:
            #The above algorithm consistently leaves a couple corners with lines not inverted correctly
            #This for loop fixes that with only a small increase in runtime
            if output_image[-point[1]][0]:
                output_image[-point[1]][0:point[0]] = np.logical_xor(True,output_image[-point[1]][0:point[0]])

        return output_image

    def render_points_as_wires(self,points,bounds,resolution,output_image = None):
        """Inputs:
        Polygon data: a list of coordinates of points that
        define the corners of a polygon

        Bounds: The top right hand corner of the square inside which all
        of the points in the polygon data will fit (x,x) (these are technically
        coordinates, but they should be the same for the sake of squares)

        Resolution: The resolution of the output image; a single number,
        all output images are square

        Output: a black and white image (stored as a matrix of Booleans).
        Stores shapes as wireframes, not filled in."""

        if type(output_image) == NoneType:
            output_image = np.zeros((resolution,resolution), dtype=bool)

        step_size = bounds[1] * 2.0 / resolution

        #Tack the first point onto the end, to make looping through
        #adjacent pairs of points easier
        points = np.append(points,[points[0]],axis = 0)

        #Make sure all points are positive
        points = points + bounds[1]

        #Scale the points so rounding them to whole numbers will place
        #them within the output resolution
        points = points / step_size

        #Round the points to prevent future rounding errors
        points = np.floor(points)

        for i in range(len(points)-1):
            #For each pair of points
            p1 = points[i]
            p2 = points[i+1]
    
            #Calculate the slope
            slope = (p2[1]-p1[1])/(p2[0]-p1[0])

            #If the slope is closer to vertical, step in the y-directions
            if np.abs(slope) > 1:
                #Then for each step (of 1) in the y-direction from p1 to p2
                for y_step in range(int(np.abs(p2[1]-p1[1]))):
                    if slope:
                        if p2[1] > p1[1]:
                            #Find which x value corresponds to the new y value (using the slope)
                            new_y = int(p1[1] + y_step)
                            new_x = int(p1[0] + y_step/slope)
                        else:
                            new_y = int(p1[1] - y_step)
                            new_x = int(p1[0] - y_step/slope)
                        #Make only one pixel true, results in a wireframe
                        output_image[-new_y][new_x] = True
            else:
                #If the slope is more horizontal, do x-steps instead
                for x_step in range(int(np.abs(p2[0]-p1[0]))):
                    if slope:
                        if p2[0] > p1[0]:
                            #Find which x value corresponds to the new y value (using the slope)
                            new_y = int(p1[1] + x_step*slope)
                            new_x = int(p1[0] + x_step)
                        else:
                            new_y = int(p1[1] - x_step*slope)
                            new_x = int(p1[0] - x_step)
                    else:
                        if p1[0] > p2[0]:
                            new_y = p1[1]
                            new_x = p1[0] - x_step
                        else:
                            new_y = p1[1]
                            new_x = p1[0] + x_step
                    output_image[-new_y][new_x-1:new_x+1] = True

        return output_image

    def render_volume_data(self,bounds,resolution,fast = True):
        """Renders the entire animation as volume data using 
        render_points_as_image()
        
        Inputs:

        Bounds: The top right hand corner of the square inside which all
        of the points of all the polygons will fit (x,x) (these are technically
        coordinates, but they should be the same for the sake of squares)

        Resolution: The resolution of each output image; a single number,
        all output images are square

        Fast: Decides whether to render wireframes or filled in shapes (the former for
        previews, because it's fast, and the latter for exports)

        Output: a list of black and white images (stored as a 3D matrix of Booleans)
        """
        if type(self.final_shapes) == NoneType:
            self.render_shapes()

        final_volume = np.zeros((len(self.final_shapes[0]),resolution,resolution), dtype=bool)
        print "Rendering Volume Data"
        if fast:
            for shape in self.final_shapes:

                volume_data = []

                for i in range(len(shape)):
                    image = self.render_points_as_wires(shape[i].T,bounds,resolution,final_volume[i])
                    final_volume[i] = image

        else:
            for shape in self.final_shapes:

                volume_data = []

                for points in shape:
                    image = self.render_points_as_image(points.T,bounds,resolution)
                    volume_data.append(image)

                final_volume = np.logical_or(final_volume,volume_data)

        # for layer in final_volume:
        #     im = layer.astype(int)*255
        #     cv2.imshow('image',im.astype('uint8'))
        #     cv2.waitKey(0)
        
        print "Done"
        return final_volume

    def write_to_scad(self, filename = 'test.scad'):

        if type(self.final_shapes) == NoneType:
            self.render_shapes()

        shapes_to_export = []

        for shape in self.final_shapes:
            solid_shapes = []

            for i in range(len(shape)):
                #For each shape (which is stored as a list of points)...
                solid_shape = shape[i].T.tolist()
                #Represent it as a polygon...
                solid_shapes.append(sp.polygon(solid_shape))
                #Extrude that polygon up .21mm...
                solid_shapes[i] = sp.linear_extrude(.2)(solid_shapes[i])
                #Then translate that extrusion up .2mm...
                solid_shapes[i] = up(i*.21)(solid_shapes[i])
            shapes_to_export.append(solid_shapes)

        #Then union ALL of the extrudes of EVERY shape
        final_export = union()(shapes_to_export)
        scad_render_to_file(final_export,filename)

    def preview_scad(self, filename = 'test.scad', proc = None):

        if proc:
            proc.terminate()
        proc = subprocess32.Popen(["openscad", filename])
        return proc

    def render_scad(self, filename = 'test.scad'):
        output_name = filename.split('.')[0] + '.stl'

        proc = subprocess32.Popen(['openscad','-o',output_name,filename])
        print "Rendering..."
        proc.wait()
        proc.terminate()



if __name__ == '__main__':
    # circle = Circle(5)
    # square1 = Circle(7.5, (10,0))
    # square2 = Circle(7.5, (0,10))
    # square3 = Circle(7.5, (-10,0))
    # square4 = Circle(7.5, (0,-10))

    # rot = Rotation(360,(0,0))
    # rot2 = Rotation(-180,(0,0))
    # di2 = Inward_Harmonic_Dilation(.6,(0,0))

    # anim = Animation(square1,[rot,di2])
    # anim.add_shape(square2,[rot2,di2])
    # anim.add_shape(square3,[rot,di2])
    # anim.add_shape(square4,[rot2,di2])
    # anim.add_shape(circle)

    hex1 = n_Sided_Polygon(6,12.35*8/sqrt(3))
    hex2 = n_Sided_Polygon(6,12.35*8/sqrt(3))

    rot1 = Rotation( 120,None,96)
    rot2 = Rotation(-60,None,96)
    di   = Inward_Harmonic_Dilation(.3,None,96)

    anim = Animation(hex1,[rot1,di])
    anim.add_shape(hex2,[rot2,di])

    anim.write_to_scad()
    # anim.render_volume_data((12,12),240,False)
