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
from types import *

class Polygon(object):
    """Represents a polygon on a plane.

    Attributes: points (a list of Point objects)
    """

    def __init__(self, points=[(0,0)]):
        self.points = np.array(points)
        self.find_center()

    def __str__(self):
        return str(self.points)

    def __repr__(self):
        return self.__str__()

    def __add__(self,other):
        return Polygon(self.points + other)

    def __mul__(self,other):
        return Polygon(self.points * other)

    def find_center(self):
        sum_point = sum(self.points)
        centroid = sum_point/len(self.points)
        self.center = centroid

class n_Sided_Polygon(Polygon):
    """Generates a regular n sided polygon

    Attributes: points (a list of Point objects)
    """

    def __init__(self, N = 3, radius = 1, center = (0,0), angle = 0):
        points = []
        for n in range(N):
            x_coord = radius * np.cos(2*pi*n/N + angle) + center[0]
            y_coord = radius * np.sin(2*pi*n/N + angle) + center[1]
            points.append((x_coord,y_coord))
        super(n_Sided_Polygon,self).__init__(points)

class Square(n_Sided_Polygon):
    """Generates a square of side length l.

    Attributes: points (a list of Point objects)
    """

    def __init__(self, l = 2, center = (0,0), angle = pi/4):
        super(Square,self).__init__(4,sqrt(2)*l/2.0,center,angle)


"""Transformations"""

class Rotation(object):
    """A transformation that rotates a shape theta degrees about a given point

    Attributes: theta, center
    """

    def __init__(self,theta = 0, center = None, depth = 500):
        theta = theta * pi / 180.0
        trans_mat = [[[np.cos(theta/depth * i),-np.sin(theta/depth * i)],[np.sin(theta/depth * i),np.cos(theta/depth * i)]] for i in range(depth+1)]
        self.trans_mat = np.array(trans_mat)

        if center:
            self.center = np.array(center)
        else:
            self.center = None

class Dilation(object):
    """A transformation that scales a shape by a given factor

    Attributes: scale_factor
    """

    def __init__(self, scale_factor = 1, depth = 500):
        scale_factor = float(scale_factor)
        if scale_factor > 1:
            self.trans_mat = [1 + i*scale_factor/depth for i in range(depth+1)]
        else:
            scale_factor = 1-scale_factor
            self.trans_mat = [1 - i*scale_factor/depth for i in range(depth+1)]

class Animation(object):
    """A collection of polygons and transformations, that can be exported
    to an openscad file

    """

    def __init__(self, polygon = Square(), transformations = [Rotation()]):
        self.shapes = {}
        self.shapes[polygon] = list(transformations)

    def add_shape(self, polygon = Square(), transformations = [Rotation()]):
        self.shapes[polygon] = list(transformations)

    def render_shapes(self, filename = 'test.scad'):
        final_shapes = []

        for shape, transformations in self.shapes.items():
            if type(transformations[0].center) is not NoneType:
                new_shape = shape.points - transformations[0].center
                new_shape = np.dot(transformations[0].trans_mat,new_shape.T)
                new_shape = new_shape + transformations[0].center.reshape(2,1)
            else:
                new_shape = np.dot(transformations[0].trans_mat,shape.points.transpose())

            if len(transformations) > 1:
                for transformation in transformations[1:]:
                    if type(transformation.center) is not NoneType:
                        new_shape = new_shape - transformation.center.reshape(2,1)
                        new_shape = np.dot(transformation.trans_mat,new_shape)
                        new_shape = new_shape + transformation.center.reshape(2,1)
                    else:
                        new_shape = np.dot(transformation.trans_mat,new_shape)

            final_shapes.append(new_shape)

        shapes_to_export = []

        for shape in final_shapes:
            solid_shapes = []
            for i in range(501):
                solid_shape = shape[i].T.tolist()
                solid_shapes.append(sp.polygon(solid_shape))
                solid_shapes[i] = sp.linear_extrude(.21)(solid_shapes[i])
                solid_shapes[i] = up(i/5.0)(solid_shapes[i])
            shapes_to_export.append(solid_shapes)

        final_export = union()(shapes_to_export)
        scad_render_to_file(final_export,filename)


if __name__ == '__main__':
    square1 = Square(10, (5,5))
    square2 = Square(10, (-2.5,-2.5))
    square3 = Square(7.5, (-1,2))
    square4 = Square(7.5, (1,-2))

    rot = Rotation(720)

    anim = Animation(square1,[rot])
    anim.add_shape(square2,[rot])
    anim.add_shape(square3,[rot])
    anim.add_shape(square4,[rot])
    anim.render_shapes()