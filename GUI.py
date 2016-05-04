"""
A set of classes to define simple user inputs and run Geometry.py and sculptureGen.py,
creatinG printable stl files from simple user defined functions and capabilities.

Authors: Coleman Ellis, Claire Kincaid, Maximillian Schommer

Software DesiGn SprinG 2016"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import GeometryGUI
import PerlinGUI

#main window
class FirstWindow(Gtk.Window):  #sub class Gtk window to define my window
    def __init__(self):
        Gtk.Window.__init__(self, title = "Choose a method of Sculpture Generation")
        self.set_border_width(10)
        self.set_default_size(400, 50)

        #initiates Gtk box window
        self.box = Gtk.Box(spacing = 6)
        self.add(self.box)

        #Initializes Vector Animation Button, places in box
        self.VectorButton = Gtk.Button(label = "Vector Animation")
        self.VectorButton.connect("clicked", self.on_VectorButton_clicked)
        self.VectorButton.connect("clicked", Gtk.main_quit)
        self.box.pack_start(self.VectorButton, True, True, 0)

        #Initializes Perlin Noise Button, places in box
        self.PerlinButton = Gtk.Button(label = "Perlin Noise")
        self.PerlinButton.connect("clicked", self.on_PerlinButton_clicked)
        self.PerlinButton.connect("clicked", Gtk.main_quit)
        self.box.pack_start(self.PerlinButton, True, True, 0)

    #when VectorButton clicked, toggles to new GUI
    def on_VectorButton_clicked(self, widget):
        Geowin = GeometryGUI.VectorWindow() #create instance of mywindow instead of Gtk.Window
        Geowin.connect("delete-event", Gtk.main_quit)
        Geowin.show_all()
        Gtk.main()

    #when PerlinButton clicked, toggles to new GUI
    def on_PerlinButton_clicked(self, widget):
        Perlinwin = PerlinGUI.PerlinWindow()
        Perlinwin.connect("delete-event", Gtk.main_quit)
        Perlinwin.show_all()
        Gtk.main()

win = FirstWindow() #create instance of mywindow instead of Gtk.Window
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()