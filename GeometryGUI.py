"""
A set of classes to define and transform shapes on a 2D coordinate axis,
designed for easy use with SolidPython and pyGTK.

Authors: Coleman Ellis, Claire Kincaid, Maximillian Schommer

SoftDes Spring 2016
Required Packages: numpy, solidpython, matplotlib, openscad, opencv, pyGTK 
"""

from numpy import pi
import numpy as np
from math import sqrt
import solid as sp
from solid.utils import *
from types import NoneType
from matplotlib import pylab
import cv2
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


"""Shapes"""

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
        angle = angle
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
        self.center = None

        scale_factor = float(scale_factor)
        if scale_factor > 1:
            self.trans_mat = [[[1 + i*scale_factor/depth,0],[0,1 + i*scale_factor/depth]] for i in range(depth+1)]
        else:
            scale_factor = 1-scale_factor
            self.trans_mat = [[[1 - i*scale_factor/depth,0],[0,1 - i*scale_factor/depth]] for i in range(depth+1)]

"""Animation & Rendering"""

class Animation(object):
    """A collection of polygons and transformations, that can be exported
    to an openscad file

    """

    def __init__(self, polygon = Square(), transformations = [Rotation()]):
        self.shapes = {}
        self.shapes[polygon] = transformations

    def add_shape(self, polygon = Square(), transformations = [Rotation()]):
        self.shapes[polygon] = transformations

    def render_shapes(self, filename = 'test.scad'):
        final_shapes = []

        print "Animating Shapes"

        for shape, transformations in self.shapes.items():

            center_transformations = [transformation for transformation in transformations if type(transformation.center) is NoneType]
            other_transformations  = [transformation for transformation in transformations if transformation not in center_transformations]

            transformations = center_transformations + other_transformations

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

    def render_points_as_image(self,points,bounds,resolution):
        """Inputs:
        Polygon data: a list of coordinates of points that
        define the corners of a polygon

        Bounds: The top right hand corner of the square inside which all
        of the points in the polygon data will fit (x,x) (these are technically
        coordinates, but they should be the same for the sake of squares)

        Resolution: The resolution of the output image; a single number,
        all output images are square

        Output: a black and white image."""

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

        points = np.round(points)

        y_vals = points.T[1]

        for i in range(len(points)-1):
            p1 = points[i]
            p2 = points[i+1]

            slope = (p2[1]-p1[1])/(p2[0]-p1[0])

            for y_step in range(int(np.abs(p2[1]-p1[1]))):
                if slope:
                    if p2[1] > p1[1]:
                        new_y = round(p1[1] + y_step)
                        new_x = round(p1[0] + y_step/slope)
                    else:
                        new_y = round(p1[1] - y_step)
                        new_x = round(p1[0] - y_step/slope)

                    output_image[-new_y][0:new_x] = np.logical_xor(True,output_image[-new_y][0:new_x])

        for point in points[:-1]:
            if output_image[-point[1]][0]:
                output_image[-point[1]][0:point[0]] = np.logical_xor(True,output_image[-point[1]][0:point[0]])

        # im = output_image.astype(int)*255
        # cv2.imshow('image',im.astype('uint8'))
        # cv2.waitKey(0)

        return output_image

    def render_volume_data(self,bounds,resolution):
        final_volume = np.zeros((len(self.final_shapes[0]),resolution,resolution), dtype=bool)
        print "Rendering Volume Data"
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

        return final_volume


"""GUI"""

# if __name__ == '__main__':
square1 = Square(7.5, (5,5))
square2 = Square(7.5, (-5,-5))
square3 = Square(7.5, (-5,5))
square4 = Square(7.5, (5,-5))
square5 = Square(7.5, (0,sqrt(50)))
square6 = Square(7.5, (0,-sqrt(50)))
square7 = Square(7.5, (sqrt(50),0))
square8 = Square(7.5, (-sqrt(50),0))

rot = Rotation(360)
rot2 = Rotation(270,(0,0))

anim = Animation(square1,[rot2,rot])
anim.add_shape(square2,[rot2,rot])
anim.add_shape(square3,[rot2,rot])
anim.add_shape(square4,[rot,rot2])
anim.add_shape(square5,[rot2,rot])
anim.add_shape(square6,[rot2,rot])
anim.add_shape(square7,[rot,rot2])
anim.add_shape(square8,[rot,rot2])
#     anim.render_shapes()

#     anim.render_volume_data((15,15),240)

#main window
class MyWindow(Gtk.Window):  #sub class Gtk window to define my window
    def __init__(self):
        Gtk.Window.__init__(self, title = "Geometry") 
        # self.set_size_request(200,100)

        # self.timeout_id = None

        # vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        # self.add(vbox)

        # self.entry = Gtk.Entry()
        # self.entry.set_text("Values")
        # vbox.pack_start(self.entry, True, True, 0)

        # hbox = Gtk.Box(spacing = 6)
        # vbox.pack_start(hbox, True, True, 0)

        # self.check_length = Gtk.CheckButton("Length")
        # self.check_length.connect("toggled", self.on_length_toggled)
        # self.check_length.set_active(True)
        # hbox.pack_start(self.check_length, True, True, 0)

        # self.check_center = Gtk.CheckButton("Center")
        # self.check_center.connect("toggled", self.on_center_toggled)
        # self.check_center.set_active(False)
        # hbox.pack_start(self.check_center, True, True, 0)

        grid = Gtk.Grid()
        self.add(grid)

        button1 = Gtk.Button(label="Render")
        button1.connect("clicked", self.on_button_clicked)
        button2 = Gtk.Button(label="Button 2")
        button3 = Gtk.Button(label="Button 3")
        button4 = Gtk.Button(label="Button 4")
        button5 = Gtk.Button(label="Button 5")
        button6 = Gtk.Button(label="Button 6")

        grid.add(button1)
        grid.attach(button2, 1, 0, 2, 1)
        grid.attach_next_to(button3, button1, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(button4, button3, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach(button5, 1, 2, 1, 1)
        grid.attach_next_to(button6, button5, Gtk.PositionType.RIGHT, 1, 1)

    def on_button_clicked(self, widget):  
        anim.render_shapes()
        anim.render_volume_data((15,15),240)
        print "Done Rendering"

    # def on_length_toggled(self, button):
    #     value = button.get_active()
    #     self.entry.set_visibility(value)

    # def on_center_toggled(self, button):
    #     value = button.get_active()
    #     self.entry.set_visibility(value)

win = MyWindow() #create instance of mywindow instead of Gtk.Window
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()