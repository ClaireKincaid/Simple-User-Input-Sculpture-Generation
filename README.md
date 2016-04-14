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

sculpture_gen.py

Using the sculpture_gen program, you can create solids by mathmatically defining them. Begin the progam by running it in the terminal. Answer y/n to the prompts if not otherwise specified. If you choose to mathmatically define objects, then choose the menu item and enter functions and then boolean operations to perform on the functions. A rendering will appear after a boolean operation is completed.

`x2+y2+z**2` < 1 will result in a sphere of radius 1.

`x+y+z` < .5 will result in a planear section which is solid, and the other section is empty.

You can experiment with other defining equations. I do not have an interpreter built into my code. I am using an eval statement. Please don't use this on anything public, because it is very vulnerable to attack.

Right now, there is no way to view the items you are combining, which will be fixed in the next version.

For the function blobby extrude, you choose an image to inspire the program. The image will then be processed to grayscale and a random sculpture will be created from that image.

Currently, the 'i' menu option is not functional, but will be soon. An improved user interface will also be availible in the next update.

ctrl+C will exit the program.

#License
MIT License

Copyright (c) 2016 Coleman Ellis, Claire Kincaid, Maximillian Schommer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
