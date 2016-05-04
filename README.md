# Simple User Input Sculpture Generation (SUISG)
Coleman Ellis, Claire Kincaid, Maximillian Schommer

Software Design Spring 2016

## Description
SUISG is both a toolset for computationally generating sculptures, as well as a GUI that makes it fast and easy to design compelling sculptures.

SUISG was born out of the desire for a convenient way to develop artistically and compelling art pieces without the use of unintuitive CAD software. It works at the intersection of three parts: sculptures generated via shapes and transformations over time, sculptures generated via perlin noise, and a GUI that ties the two together.

## Getting Started
SUISG has a fair few packages that need to be installed. These commands should get everything up and running:

```
pip install solidpython
pip install subprocess32
pip install numpy-stl
pip install mayavi
pip install -U textblob
sudo apt-get install python-skimage
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
sudo apt-get install libvtk5-dev python-vtk
sudo apt-get install python-pyglet
sudo apt-get install openscad
python -m textblob.download_corpora
```

Lastly, head over here https://pypi.python.org/pypi/noise/, download noise-1.2.2.zip(md5), then run `python setup.py install`

All of the previous commands might require root access, depending on your system setup.


## Usage

### Vector Animations

Using the Geometry program, you can define shapes, transformations to apply to those shapes over time, and then output those shapes to an OpenSCAD file to render them as an STL (OpenSCAD is fairly slow, a more efficient solution is pending).

There are currently three ways to define a polygon: the Polygon, n-Sided-Polygon, and Square classes (with more to come). The easiest to use is a Square, so let's use that as an example. To define a Square, use the following code:

```python
sqr = Square() #Generates a 2x2 square centered on the origin
```

A square by itself isn't super interesting, so let's add a rotation:

```python
rot = Rotation(360,(0,0)) #Represents a rotation of 360 degrees about the origin
```

Now to apply the rotation to the square, we add them both to an Animation:

```python
anim = Animation(sqr,[rot]) #If we had more transformations to apply, they'd also go in the list
```

Then just export the animation:

```python
anim.write_to_scad() #Exports to test.scad by default
```

You should now have an OpenSCAD file showing a square rotating 360 degrees as it moves upwards! From here you can play with adding different shapes (either regular polygons using n_Sided_Polygon, or Polygons defined using lists of points), and different transformations (rotations of different degrees or about different points, as well as dilations). You can make some really interesting sculptures with just a few shapes and a few transformations. The following code, for example, generates a cool swirly dome:

```python
from Geometry import *
from math import pi
hex1 = n_Sided_Polygon(6,12) #A hexagon, centered on the origin, with radius 12
hex2 = n_Sided_Polygon(6,12)
rot1 = Rotation( 240,None,128) #A transformation with None as the center is applied to the shape's center
rot2 = Rotation(-120,None,128) #128 is the "depth" of the transformation, it's the number of layers that will be in the final stl. It defaults to 500
di   = Cosine_Harmonic_Dilation(pi/2,None,128) #Cosine_Harmonic_Dilation scales the entire sculpture by a cosine wave over a particular angle range
di2  = Dilation(1.2,None,128)
anim = Animation(hex1,[rot1,di,di2])
anim.add_shape(hex2,[rot2,di,di2]) #This is how you add a second shape
anim.write_to_scad('capstone.scad')
```

Just a warning though, OpenSCAD takes about 1~2 minutes per shape to render as an STL.

### Perlin Noise

### GUI
Using the simple GUI, you can easily interface with the Geometry Program and the Sculpture_gen program to generate sculptures without typing complicated sequences of commands into the terminal.  The GUI is organized into three pieces: A main window that prompts the user to choose a method of sculpture generation, a dialog that allows the user to interface easily with Geometry.py, and a dialog that allows the user to interface with sculpture_gen.py.

'''Geometry GUI'''
Geometry GUI allows the user to generate a list of shapes and a list of transformations, then apply the transformations to the shapes.  It will then animate and render the sculpture in openscad.  There are view, undo, and clear functions to edit existing pieces of the list. There are currently three ways to create and add shapes in GeometryGUI:

'''
Add Square: This function takes in length, center, and angle values, and generates a square in the x-y plane.  In order to use this function, add the appropriate values to each of the entry boxes and then click "Add a Square".
    - Length denotes the length of your square's sides, and is unitless, though when 3D printed is often interpreted as mm.  You must enter a number value in this box.
    - Center denotes the centerpoint of your square in the x, y coordinate plane. Inputs in this box must be of the form   x, y   where x and y are integers
    - Angle denotes the orientation of your square in the coordinate plane, in radians.  Input must be a number value

Add Polygon: This function takes in number of sides, radius, center, and angle values and generates an n sided polygon in the x-y plane.  To use this function, add the appropriate values to each of the entry boxes and then click "Add a Polygon".
    - Number of Sides: this denotes the number of sides your polygon will have.  there is no minimum or maximum value for this input, but it must take the form of an integer
    - Radius denotes the length from the center point to the corners of your polygon.  This entry has no real units but openSCAD defaults to mm during rendering.  You must enter a number value in this box
    - Center denotes the centerpoint of your polygon in the x, y coordinate plane. Inputs in this box must be of the form   x, y   where x and y are integers.
    - Angle denotes the orientation of your square in the coordinate plane, in radians. Input must be a number value

Add Circle: This function takes in Radius and Center and generates a circle in the x-y plane.  To use this function, add the appropriate values in each of the entry boxes and then click "Add a Circle"
    - Radius denotes the radius of the circle.  This entry has no units but will default to mm during the rendering process.  Input in this box must be a number value
    - Center denotes the centerpoint of your circle in the x, y coordinate plane.  Inputs in this box must be of the form   x, y   where x and y are integers.

'''
You may add as many shapes as you would like to your sculpture simply by editing the inputs of each of the dialog boxes and selecting the "Add a _____" button corresponding to those boxes.  There are also some additional functions to edit the list of shapes:

Display Shapes: this button will print the current list of shapes in your terminal.  However, as shapes are read as lists of points, you will see in terminal a list of lists of points, where each list is an individual shape entry.  You can use this function to keep track of the shapes that you have added to your sculpture

Undo Shape: this button will remove the last indexed shape from the list of shapes, then return it to your terminal so that you may view what you removed.  You may select this as many times as you would like until your list of shapes is empty

Clear Shapes: this button will reset the shapes list to an empty list, allowing you to create a new sculpture from different shapes.  Keep in mind this button clears only the shapes list, and will keep any current transformations unless you select the "clear transformations" button as well.

'''
There are four possible transformations you may apply to your sculpture:

Rotation: This transformation takes in angle and center and will rotate your shapes around the centerpoint by the given angle. To use this function, add the appropriate values in each of the entry boxes and then click "Add a Rotation".
    - Angle denotes the angle of rotation, in radians. Input for this box must be a number value
    - Center denotes the centerpoint of the rotation, i.e. the axis about which your rotation will occur, as a point in the x-y plane.  Inputs in this box must be of the form    x, y    where x and y are integers

Dilation: This transformation takes in a scale factor and a center value and will perform a basic dilation on your shapes about a given center point by the scaled factor. To use this function, add the appropriate values in each of the entry boxes and then click "Add a Dilation".
    - Scale Factor denotes the factor by which your shape will dilate, i.e. how much larger or smaller it will get in comparison to its current size.  Inputs in this box must be number values, not equations.
    - Center Point denotes the center point of your dilation.  Inputs in this box must be of the form    x, y   where x and y are integers

Cosine Harmonic Dilation: This transformation takes in an angle and a center point and will perform a cosine harmonic dilation on your shapes about a given center point (A cosine harmonic dilation causes your shapes to widen and then narrow to a point). To use this function, add the appropriate values in each of the entry boxes and then click "Add a Cosine Harmonic Dilation".
	- Angle denotes the angle in radians that defines the cosine harmonic scale factor of your dilation. Inputs in this box must be number values
	- Center Point denotes the center point of your dilation. Inputs in this box must be of the form    x, y   where x and y are integers

Inward Harmonic Dilation: This transformation takes in a scale factor and a center point and will perform an inward harmonic dilation on your shapes about a given center point (an inward harmonic dilation causes your shapes to have an hourglass form). To use this function, add the appropriate values in each of the entry boxes and then click "Add an Inward Harmonic Dilation".
	- Scale factor denotes the percentage decrease of the inward harmonic dilation.  This value is calculated as the smallest diameter/largest diameter. However, you must calculate this value yourself, and enter it into the box as a number value.
	- Center Point denotes the center point of your dilation. Inputs in this box must be of the form    x, y   where x and y are integers

Number of Layers:  This box is located below all of the add transformation boxes and MUST BE FILLED in order to create a transformation.  This denotes the height of your sculpture via the number of layers.  This number must be an integer, and will remain constant across all of your transformations.  Layers, or depth, is an important parameter for your transformations, so again be sure to fill this box appropriately before adding a transformation to your list.

'''
You may add as many transformations to your sculpture as you would like simply by editing the inputs of the appropriate dialog boxes and then selecting the corresponding "Add a ____" button. Keep in mind that ALL of your transformations will be uniformly applied to ALL of your shapes when generating your sculpture.  There are also some additional functions to view and edit your transformations. 

Display Transformations: This button prints a list of transformations in the command terminal, allowing you to view all translations that you've defined.

Undo Transformation: this button will remove the last indexed transformation from the list of transformations, then return it to your terminal so that you may view what you removed.  You may select this as many times as you would like until your list of transformations is empty

Clear Transformations: this button will reset the transformations list to an empty list, allowing you to create a new sculpture using new transformations.  Keep in mind this button clears only the current transformations, not the shapes.  If you would like to clear shapes as well, you must select the "Clear Shapes" button.

'''
The next step in the SUISG process is to preview and export.  SUISG Geometric Sculptures uses OpenSCAD to preview and Render in a new dialog window.  

PREVIEW: To activate the preview, select the PREVIEW button in the bottom left corner of the page.  This will immediately pull up an empty OpenSCAD window.  In order to preview your sculpture in the window, press the F5 key on your keyboard.  This will render a preview of your sculpture.  In order to edit your sculpture, you must first close the OpenSCAD preview, make any changes, and then select Preview and press F5 again.  It is recommended that you preview your sculpture before you move on to exporting it

EXPORT: to export your sculpture, simply select the EXPORT button in the bottom right corner of the page.  This will save your sculpture as 'text.stl' to your home directory.  Stl files are 3D printable files composed of point data.  In order to keep this sculpture and not have it rewritten when you create and export a new sculpture, you will need to go into your home directory and manually rename this file.  

Congratulations, you can now generate geometric sculptures using SUISG!

'''