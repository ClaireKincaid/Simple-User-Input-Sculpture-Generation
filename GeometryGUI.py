"""
A set of classes to define simple user inputs and run Geometry.py and sculptureGen.py,
creatinG printable stl files from simple user defined functions and capabilities.

Authors: Coleman Ellis, Claire Kincaid, Maximillian Schommer

Software DesiGn SprinG 2016"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#main window
class VectorWindow(Gtk.Window):  #sub class Gtk window to define my window
    def __init__(self):
        Gtk.Window.__init__(self, title = "Sculpture Generation from Vector Animation")
        self.set_border_width(10)
        self.set_default_size(400, 50)

        #initiates Gtk box window
        self.box = Gtk.Box(spacing = 6)
        self.add(self.box)

        #Initializes Add Shape Button, places in box
        self.AddShapeButton = Gtk.Button(label = "Add a Shape")
        self.AddShapeButton.connect("clicked", self.on_AddShapeButton_clicked)
        self.box.pack_start(self.AddShapeButton, True, True, 0)

    #when Add Shape button clicked, adds a new shape
    def on_AddShapeButton_clicked(self, widget):
        pass

