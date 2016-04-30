"""
A set of classes to define simple user inputs and run Geometry.py and sculptureGen.py,
creatinG printable stl files from simple user defined functions and capabilities.

Authors: Coleman Ellis, Claire Kincaid, Maximillian Schommer

Software DesiGn SprinG 2016"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Geometry import *

#main window
class MyWindow(Gtk.Window):  #sub class Gtk window to define my window
    def __init__(self):
        Gtk.Window.__init__(self, title = "Geometry") 
        # self.set_size_request(200,100)

        # self.timeout_id = None

        # vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacinG = 6)
        # self.add(vbox)

        # self.entry = Gtk.Entry()
        # self.entry.set_text("Values")
        # vbox.pack_start(self.entry, True, True, 0)

        # hbox = Gtk.Box(spacinG = 6)
        # vbox.pack_start(hbox, True, True, 0)

        # self.check_lenGth = Gtk.CheckButton("LenGth")
        # self.check_lenGth.connect("toGGled", self.on_lenGth_toGGled)
        # self.check_lenGth.set_active(True)
        # hbox.pack_start(self.check_lenGth, True, True, 0)

        # self.check_center = Gtk.CheckButton("Center")
        # self.check_center.connect("toGGled", self.on_center_toGGled)
        # self.check_center.set_active(False)
        # hbox.pack_start(self.check_center, True, True, 0)

        Grid = Gtk.Grid()
        self.add(Grid)

        #Button 1
        button1 = Gtk.Button(label="Render")
        button1.connect("clicked", self.on_button1_clicked)

        #Button 2
        button2 = Gtk.Button(label="Preview")
        button2.connect("clicked", self.on_button2_clicked)

        #Button 3
        button3 = Gtk.Button(label="Add Square")
        button3.connect("clicked", self.on_button3_clicked)

        #Button 4
        button4 = Gtk.Button(label="Rotation")
        button4.connect("clicked", self.on_button4_clicked)

        #Button 5
        button5 = Gtk.Button(label="Dilation")
        button5.connect("clicked", self.on_button5_clicked)

        #Button 6
        button6 = Gtk.Button(label="Animate")
        button6.connect("clicked", self.on_button6_clicked)

        #Define Button ArranGement
        Grid.add(button1)
        Grid.attach(button2, 1, 0, 2, 1)
        Grid.attach_next_to(button3, button1, Gtk.PositionType.BOTTOM, 1, 2)
        Grid.attach_next_to(button4, button3, Gtk.PositionType.RIGHT, 2, 1)
        Grid.attach(button5, 1, 2, 1, 1)
        Grid.attach_next_to(button6, button5, Gtk.PositionType.RIGHT, 1, 1)

    def on_button1_clicked(self, widGet):  
        hex1 = n_Sided_Polygon(6,12.35*8/sqrt(3))
        hex2 = n_Sided_Polygon(6,12.35*8/sqrt(3))

        rot1 = Rotation( 120,None,96)
        rot2 = Rotation(-60,None,96)
        di   = Inward_Harmonic_Dilation(.3,None,96)

        anim = Animation(hex1,[rot1,di])
        anim.add_shape(hex2,[rot2,di])

        anim.write_to_scad()
        print "Complete"

    def on_button2_clicked(self, widGet):
        pass

    def on_button3_clicked(self, widGet):
        pass

    def on_button4_clicked(self, widGet):
        pass

    def on_button5_clicked(self, widGet):
        pass

    def on_button6_clicked(self, widGet):
        pass
        
    # def on_lenGth_toGGled(self, button):
    #     value = button.Get_active()
    #     self.entry.set_visibility(value)

    # def on_center_toGGled(self, button):
    #     value = button.Get_active()
    #     self.entry.set_visibility(value)

win = MyWindow() #create instance of mywindow instead of Gtk.Window
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()