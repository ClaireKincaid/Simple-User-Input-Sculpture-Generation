# Simple User Input Sculpture Generation
Software Design Spring 2016 Final Project:  Generating 3D objects based on simple user input and exporting them as an STL file that can be 3D printed, rendered, or otherwise fabricated

Authors: Coleman Ellis, Claire Kincaid, Maximillian Schommer

## Getting Started
As of yet, our program requires the following packages to run correctly:
 - SolidPython
 - OpenCV
 - Numpy

We also recommend downloading and installing OpenSCAD, so you can easily compile an STL using the code we currently have in place.

To install, just download the git repository and use the files locally (or add them to the folder where Python can access them). We're not at a point where we can provide an installer yet.

## Usage
###Geometry.py
Using the Geometry program, you can define shapes, transformations to apply to those shapes over time, and then output those shapes to an OpenSCAD file to render them as an STL (OpenSCAD is fairly slow, a more efficient solution is pending).

There are currently three ways to define a polygon: the Polygon, n-Sided-Polygon, and Square classes (with more to come). The easiest to use is a Square, so let's use that as an example. To define a Square, use the following code:

`sqr = Square() #Generates a 2x2 square centered on the origin`

A square by itself isn't super interesting, so let's add a rotation:

`rot = Rotation(360,(0,0)) #Represents a rotation of 360 degrees about the origin`

Now to apply the rotation to the square, we add them both to an Animation:

`anim = Animation(sqr,[rot]) #If we had more transformations to apply, they'd also go in the list`

Then just export the animation:

`anim.render_shapes() #Exports to test.scad by default`

You should now have an OpenSCAD file showing a square rotating 360 degrees as it moves upwards! From here you can play with adding different shapes (either regular polygons using n_Sided_Polygon, or Polygons defined using lists of points), and different transformations (rotations of different degrees or about different points, as well as dilations). You can make some really interesting sculptures with just a few shapes and a few transformations.

Just a warning though, OpenSCAD takes about 1~2 minutes per shape to render as an STL.

##Schommer's Stuff

##The GUI

#License
How do we want to do this?
