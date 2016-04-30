"""
A set of classes to define simple user inputs and run Geometry.py and sculpturegen.py,
creating printable stl files from simple user defined functions and capabilities.

Authors: Coleman Ellis, Claire Kincaid, Maximillian Schommer

Software Design Spring 2016"""

import gtk

#main window
class MyWindow(gtk.Window):  #sub class Gtk window to define my window
    def __init__(self):
        gtk.Window.__init__(self, title = "Geometry") 
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

        grid = gtk.Grid()
        self.add(grid)

        #Button 1
        button1 = gtk.Button(label="Render")
        button1.connect("clicked", self.on_button1_clicked)

        #Button 2
        button2 = gtk.Button(label="Preview")
        button2.connect("clicked", self.on_button2_clicked)

        #Button 3
        button3 = gtk.Button(label="Add Square")
        button3.connect("clicked", self.on_button3_clicked)

        #Button 4
        button4 = gtk.Button(label="Rotation")
        button4.connect("clicked", self.on_button4_clicked)

        #Button 5
        button5 = gtk.Button(label="Dilation")
        button5.connect("clicked", self.on_button5_clicked)

        #Button 6
        button6 = gtk.Button(label="Animate")
        button6.connect("clicked", self.on_button6_clicked)

        #Define Button Arrangement
        grid.add(button1)
        grid.attach(button2, 1, 0, 2, 1)
        grid.attach_next_to(button3, button1, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(button4, button3, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach(button5, 1, 2, 1, 1)
        grid.attach_next_to(button6, button5, Gtk.PositionType.RIGHT, 1, 1)

    def on_button1_clicked(self, widget):  
        pass

    def on_button2_clicked(self, widget):
        pass

    def on_button3_clicked(self, widget):
        pass

    def on_button4_clicked(self, widget):
        pass

    def on_button5_clicked(self, widget):
        pass

    def on_button6_clicked(self, widget):
        pass
        
    # def on_length_toggled(self, button):
    #     value = button.get_active()
    #     self.entry.set_visibility(value)

    # def on_center_toggled(self, button):
    #     value = button.get_active()
    #     self.entry.set_visibility(value)

win = MyWindow() #create instance of mywindow instead of Gtk.Window
win.connect("delete-event", gtk.main_quit)
win.show_all()
gtk.main()