"""
A set of classes to define simple user inputs and run Geometry.py and sculptureGen.py,
creatinG printable stl files from simple user defined functions and capabilities.

Authors: Coleman Ellis, Claire Kincaid, Maximillian Schommer

Software DesiGn SprinG 2016"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
# import sculpture_gen.py

#main window
class PerlinWindow(Gtk.Window):  #sub class Gtk window to define my window
    def __init__(self):
        Gtk.Window.__init__(self, title = "Sculpture Generation from Perlin Noise")
        self.set_border_width(10)
        self.set_default_size(400, 50)

        #initiates sculpture
        # self.sculpture = sculpture_gen.Sculpture()

        #initiates Gtk box window
        self.grid = Gtk.Grid()
        self.add(self.grid)

		#Initializes Add Picture Button, places in grid
        self.AddImageButton = Gtk.Button(label = "Add an Image to Be Inspired By")
        self.AddImageButton.connect("clicked", self.on_AddImageButton_clicked)
        self.grid.add(self.AddImageButton)

        #initializes add image entry, places in grid
        self.AddImageEntry = Gtk.Entry()
        self.AddImageEntry.set_text("FileName")
        self.grid.attach_next_to(self.AddImageEntry, self.AddImageButton, Gtk.PositionType.RIGHT, 2, 1)

        #initializes load noise button, places in grid
        self.LoadNoiseButton = Gtk.Button(label = "Load Perlin Noise")
        self.LoadNoiseButton.connect("clicked", self.on_LoadNoiseButton_clicked)
        self.grid.attach_next_to(self.LoadNoiseButton, self.AddImageButton, Gtk.PositionType.BOTTOM, 2, 1)

        #initializes Preview Button, places in grid
        self.PreviewButton = Gtk.Button(label = "PREVIEW")
        self.PreviewButton.connect("clicked", self.on_PreviewButton_clicked)
        self.grid.attach_next_to(self.PreviewButton, self.LoadNoiseButton, Gtk.PositionType.RIGHT, 2, 1)

       	#initializes export button, places in grid
       	self.ExportButton = Gtk.Button(label = "EXPORT")
       	self.ExportButton.connect("clicked", self.on_ExportButton_clicked)
       	self.grid.attach_next_to(self.ExportButton, self.LoadNoiseButton, Gtk.PositionType.BOTTOM, 2, 1)

       	#initializes Export entry, places in grid
       	self.ExportFileName = Gtk.Entry()
       	self.ExportFileName.set_text("FileName")
       	self.grid.attach_next_to(self.ExportFileName, self.ExportButton, Gtk.PositionType.RIGHT, 2, 1)

    #when Add Add picture button clicked, adds picture
    def on_AddImageButton_clicked(self, widget):
        pass

    #when Load Noise button clicked, loads noise
    def on_LoadNoiseButton_clicked(self, widget):
    	pass

    #when preview button clicked, loads preview
    def on_PreviewButton_clicked(self, widget):
    	pass

    #when export button clicked, exports as stl
    def on_ExportButton_clicked(self, widget):
    	pass