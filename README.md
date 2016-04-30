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

`sqr = Square() #Generates a 2x2 square centered on the origin`

A square by itself isn't super interesting, so let's add a rotation:

`rot = Rotation(360,(0,0)) #Represents a rotation of 360 degrees about the origin`

Now to apply the rotation to the square, we add them both to an Animation:

`anim = Animation(sqr,[rot]) #If we had more transformations to apply, they'd also go in the list`

Then just export the animation:

`anim.write_to_scad() #Exports to test.scad by default`

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