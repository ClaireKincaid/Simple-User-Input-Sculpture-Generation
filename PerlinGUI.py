"""
A set of classes to define simple user inputs and run Geometry.py and sculptureGen.py,
creatinG printable stl files from simple user defined functions and capabilities.

Authors: Coleman Ellis, Claire Kincaid, Maximillian Schommer

Software DesiGn SprinG 2016"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#main window
class PerlinWindow(Gtk.Window):  #sub class Gtk window to define my window
    def __init__(self):
        Gtk.Window.__init__(self, title = "Sculpture Generation from Perlin Noise")
        self.set_border_width(10)
        self.set_default_size(400, 50)

        #initiates Gtk box window
        self.box = Gtk.Box(spacing = 6)
        self.add(self.box)

        #Initializes Add Picture Button, places in box
        self.AddImageButton = Gtk.Button(label = "Add an Image to Be Inspired By")
        self.AddImageButton.connect("clicked", self.on_AddImageButton_clicked)
        self.box.pack_start(self.AddImageButton, True, True, 0)

    #when Add Shape button clicked, adds a new shape
    def on_AddImageButton_clicked(self, widget):
        pass