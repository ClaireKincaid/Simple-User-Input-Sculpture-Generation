"""
A set of classes to define and transform shapes on a 2D coordinate axis,
designed for easy use with SolidPython.

Authors: Coleman Ellis, Claire Kincaid, Maximillian Schommer

SoftDes Spring 2016
"""

from numpy import pi
import numpy as np
from math import sqrt

class Point(object):
    """Represents a single point on a plane.

    Attributes: coordinates (a two-element tuple)
    """

    def __init__(self, coordinates = (0,0)):
        self.coordinates = coordinates

    def __str__(self):
        #Prints as a list for the sake of SolidPython
        return "[%.10f,%.10f]" % (self.coordinates[0],self.coordinates[1])

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        total_x = self.coordinates[0] + other.coordinates[0]
        total_y = self.coordinates[1] + other.coordinates[1]
        return Point((total_x,total_y))

    def __radd__(self,other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other):
        total_x = self.coordinates[0] - other.coordinates[0]
        total_y = self.coordinates[1] - other.coordinates[1]
        return Point((total_x,total_y))

    def __mul__(self,other):
        #Note! Only multiply scalars.
        new_x = self.coordinates[0] * other
        new_y = self.coordinates[1] * other
        return Point((new_x,new_y))

    def __div__(self,other):
        return self.__mul__(1.0/other)

class Polygon(object):
    """Represents a polygon on a plane.

    Attributes: points (a list of Point objects)
    """

    def __init__(self, points=[Point((0,0))]):
        self.points = points
        self.find_center()

    def __str__(self):
        return str(self.points)

    def __repr__(self):
        return self.__str__()

    def __add__(self,other):
        #You can add a point to a polygon, not a polygon to a polygon
        new_points = []
        for point in self.points:
            new_points.append(point+other)
        return Polygon(new_points)

    def find_center(self):
        sum_point = sum(self.points)
        centroid = sum_point/len(self.points)
        self.center = centroid

class n_Sided_Polygon(Polygon):
    """Generates a regular n sided polygon

    Attributes: points (a list of Point objects)
    """

    def __init__(self, N = 3, radius = 1, center = Point(0,0), angle = 0):
        points = []
        for n in range(N):
            x_coord = radius * np.cos(2*pi*n/N + angle) + center.coordinates[0]
            y_coord = radius * np.sin(2*pi*n/N + angle) + center.coordinates[1]
            points.append(Point((x_coord,y_coord)))
        super(n_Sided_Polygon,self).__init__(points)

class Square(n_Sided_Polygon):
    """Generates a square of side length l.

    Attributes: points (a list of Point objects)
    """

    def __init__(self, l = 2, center = Point(0,0), angle = pi/4):
        super(Square,self).__init__(4,sqrt(2)*l/2.0,center,angle)


"""Transformations"""

class Transformation(object):
    """A transformation that can be applied to a shape

    A transformation consists of an initial translation, a
    matrix multiplication, then the reverse of the initial translation
    (ex. rotating about a specific point)

    Attributes: trans_mat (the transformation matrix)
    """

    def __init__(self, trans_mat = [[1,0],[0,1]], center = None):
        #Center needs to be a Point
        self.trans_mat = trans_mat
        if center:
            self.center = center
        else:
            self.center = None

    def __str__(self):
        return str(self.trans_mat[0]) + "\n" + str(self.trans_mat[1])

    def __repr__(self):
        return self.__str__()

    def transform(self, polygon):
        """Applies the transformation to a given Polygon, and return a new Polygon
        """
        if not self.center:
            temp_center = polygon.center
        else:
            temp_center = self.center

        new_points = []
        for point in polygon.points:
            new_point = point - temp_center
            new_point = np.dot(self.trans_mat,new_point.coordinates).tolist()
            new_point = Point(tuple(new_point))
            new_point = new_point + temp_center
            new_points.append(new_point)

        return Polygon(new_points)