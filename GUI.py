#Simple GUI for Simple User Input Sculpture Generation
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


#sample render function
def render():
    pass

#main window
class MyWindow(Gtk.Window):  #sub class Gtk window to define my window
    def __init__(self):
        Gtk.Window.__init__(self, title = "Render") #set value of init to hello world
        self.button = Gtk.Button(label = "Render")
        self.button.connect("clicked", self.on_button_clicked) #connecked to clicked signal
        self.add(self.button) #add as child to top level window
    def on_button_clicked(self, widget):  #method on-buttn-clicked, called if you click on the button
        print("Rendering...") #when method is called, print hello world
        render()

win = MyWindow() #create instance of mywindow instead of Gtk.Window
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()