"""
A set of classes to define simple user inputs and run Geometry.py and sculptureGen.py,
creatinG printable stl files from simple user defined functions and capabilities.

Authors: Coleman Ellis, Claire Kincaid, Maximillian Schommer

Software DesiGn SprinG 2016"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import Geometry

#main window
class VectorWindow(Gtk.Window):  #sub class Gtk window to define my window
    def __init__(self):
        Gtk.Window.__init__(self, title = "Sculpture Generation from Vector Animation")
        self.set_border_width(10)

        #initiates Gtk grid window
        self.grid = Gtk.Grid()
        self.add(self.grid)

        #Initializes Add Shape Button, places in window
        self.AddSquareButton = Gtk.Button(label = "Add a Square")
        self.AddSquareButton.connect("clicked", self.on_AddSquareButton_clicked)
        self.grid.add(self.AddSquareButton)

        #initializes the length entry for add square, puts in window
        self.SquareLengthEntry = Gtk.Entry()
        self.SquareLengthEntry.set_text("Length")
        self.grid.attach_next_to(self.SquareLengthEntry, self.AddSquareButton, Gtk.PositionType.RIGHT, 2, 1)

        #initializes the center entry for add square, puts in window
        self.SquareCenterEntry = Gtk.Entry()
        self.SquareCenterEntry.set_text("Square Center, (x,y)")
        self.grid.attach_next_to(self.SquareCenterEntry, self.SquareLengthEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes the angle entry for add square, puts in window
        self.SquareAngleEntry = Gtk.Entry()
        self.SquareAngleEntry.set_text("Angle, (rad)")
        self.grid.attach_next_to(self.SquareAngleEntry, self.SquareCenterEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes the n sided polygon button, places in window
        self.AddNPolygonButton = Gtk.Button(label = "Add a Polygon")
        self.AddNPolygonButton.connect("clicked", self.on_AddNPolygonButton_clicked)
        self.grid.attach_next_to(self.AddNPolygonButton, self.AddSquareButton, Gtk.PositionType.BOTTOM, 1, 1)

        #initializes n sides entry for add n polygon, puts in window
        self.NSidesEntry = Gtk.Entry()
        self.NSidesEntry.set_text("Number of Sides")
        self.grid.attach_next_to(self.NSidesEntry, self.AddNPolygonButton, Gtk.PositionType.RIGHT, 2, 1)

        #initializes radius entry for add n polygon, puts in window
        self.NRadiusEntry = Gtk.Entry()
        self.NRadiusEntry.set_text("Polygon Radius")
        self.grid.attach_next_to(self.NRadiusEntry, self.NSidesEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes center entry for add n polygon, puts in window
        self.NCenterEntry = Gtk.Entry()
        self.NCenterEntry.set_text("Polygon Center, (x,y)")
        self.grid.attach_next_to(self.NCenterEntry, self.NRadiusEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes angle entry for add n polygon, puts in window
        self.NAngleEntry = Gtk.Entry()
        self.NAngleEntry.set_text("Angle, (rad)")
        self.grid.attach_next_to(self.NAngleEntry, self.NCenterEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes Add Circle Button, puts in window
        self.AddCircleButton = Gtk.Button(label = "Add a Circle")
        self.AddCircleButton.connect("clicked", self.on_AddCircleButton_clicked)
        self.grid.attach_next_to(self.AddCircleButton, self.AddNPolygonButton, Gtk.PositionType.BOTTOM, 1, 1)

        #initializes radius entry for add circle, puts in window
        self.CircRadiusEntry = Gtk.Entry()
        self.CircRadiusEntry.set_text("Circle Radius")
        self.grid.attach_next_to(self.CircRadiusEntry, self.AddCircleButton, Gtk.PositionType.RIGHT, 2, 1)

        #initializes center entry for add circle, puts in window
        self.CircCenterEntry = Gtk.Entry()
        self.CircCenterEntry.set_text("Circle Center, (x, y)")
        self.grid.attach_next_to(self.CircCenterEntry, self.CircRadiusEntry, Gtk.PositionType.RIGHT, 2, 1)

        #intializes add polygon from points button, puts in window
        self.AddPointsPolyButton = Gtk.Button(label = "Add Polygon from Points")
        self.AddPointsPolyButton.connect("clicked", self.on_AddPointsPolyButton_clicked)
        self.grid.attach_next_to(self.AddPointsPolyButton, self.AddCircleButton, Gtk.PositionType.BOTTOM, 1, 1)

        #initializes points entry for add points poly, puts in window
        self.PointsPolyPointsEntry = Gtk.Entry()
        self.PointsPolyPointsEntry.set_text("Points, (list)")
        self.grid.attach_next_to(self.PointsPolyPointsEntry, self.AddPointsPolyButton, Gtk.PositionType.RIGHT, 6, 1)

        #initializes add rotation button, puts in window
        self.AddRotButton = Gtk.Button(label = "Add a Rotation")
        self.AddRotButton.connect("clicked", self.on_AddRotButton_clicked)
        self.grid.attach_next_to(self.AddRotButton, self.AddPointsPolyButton, Gtk.PositionType.BOTTOM, 1, 1)

        #intializes angle entry for add rot, puts in window
        self.RotAngleEntry = Gtk.Entry()
        self.RotAngleEntry.set_text("Rotation Angle, (rad)")
        self.grid.attach_next_to(self.RotAngleEntry, self.AddRotButton, Gtk.PositionType.RIGHT, 2, 1)

        #initializes center entry for add rot, puts in window
        self.RotCenterEntry = Gtk.Entry()
        self.RotCenterEntry.set_text("Rotation Center, (x,y)")
        self.grid.attach_next_to(self.RotCenterEntry, self.RotAngleEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes layers entry for add rot, puts in window
        self.RotLayersEntry = Gtk.Entry()
        self.RotLayersEntry.set_text("Number of Layers")
        self.grid.attach_next_to(self.RotLayersEntry, self.RotCenterEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes add dilation button, puts in window
        self.AddDilButton = Gtk.Button(label = "Add a Dilation")
        self.AddDilButton.connect("clicked", self.on_AddDilButton_clicked)
        self.grid.attach_next_to(self.AddDilButton, self.AddRotButton, Gtk.PositionType.BOTTOM, 1, 1)

        #initializes scale entry for add dil, puts in window
        self.DilScaleEntry = Gtk.Entry()
        self.DilScaleEntry.set_text("Scale Factor")
        self.grid.attach_next_to(self.DilScaleEntry, self.AddDilButton, Gtk.PositionType.RIGHT, 2, 1)

        #initializes center entry for add dil, puts in window
        self.DilCenterEntry = Gtk.Entry()
        self.DilCenterEntry.set_text("Dilation Center, (x,y)")
        self.grid.attach_next_to(self.DilCenterEntry, self.DilScaleEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes layers entry for add dil, puts in window
        self.DilLayersEntry = Gtk.Entry()
        self.DilLayersEntry.set_text("Number of Layers")
        self.grid.attach_next_to(self.DilLayersEntry, self.DilCenterEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes add Cosine Harmonic Dilation button, puts in window
        self.AddCosHarmDilButton = Gtk.Button(label = "Add a Cosine Harmonic Dilation")
        self.AddCosHarmDilButton.connect("clicked", self.on_AddCosHarmDilButton_clicked)
        self.grid.attach_next_to(self.AddCosHarmDilButton, self.AddDilButton, Gtk.PositionType.BOTTOM, 1, 1)

        #initializes angle entry for cosharmdil, puts in window
        self.CosHarmDilAngleEntry = Gtk.Entry()
        self.CosHarmDilAngleEntry.set_text("Dilation Angle, (rad)")
        self.grid.attach_next_to(self.CosHarmDilAngleEntry, self.AddCosHarmDilButton, Gtk.PositionType.RIGHT, 2, 1)

        # initializes center entry for cosharmdil, puts in window
        self.CosHarmDilCenterEntry = Gtk.Entry()
        self.CosHarmDilCenterEntry.set_text("Dilation Center, (x,y)")
        self.grid.attach_next_to(self.CosHarmDilCenterEntry, self.CosHarmDilAngleEntry, Gtk.PositionType.RIGHT, 2, 1)

        # #initializes layers entry for cosharmdil, puts in window
        self.CosHarmDilLayersEntry = Gtk.Entry()
        self.CosHarmDilLayersEntry.set_text("Number of Layers")
        self.grid.attach_next_to(self.CosHarmDilLayersEntry, self.CosHarmDilCenterEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes Add Inward Harmonic Dilation button, puts in window
        self.AddInHarmDilButton = Gtk.Button(label = "Add an Inward Harmonic Dilation")
        self.AddInHarmDilButton.connect("clicked", self.on_AddInHarmDilButton_clicked)
        self.grid.attach_next_to(self.AddInHarmDilButton, self.AddCosHarmDilButton, Gtk.PositionType.BOTTOM, 1, 1)

        #initializes scale entry for InHarmDil, puts in window
        self.InHarmDilScaleEntry = Gtk.Entry()
        self.InHarmDilScaleEntry.set_text("Scale Factor (d/D)")
        self.grid.attach_next_to(self.InHarmDilScaleEntry, self.AddInHarmDilButton, Gtk.PositionType.RIGHT, 2, 1)

        #initializes center entry for InHarmDil, puts in window
        self.InHarmDilCenterEntry = Gtk.Entry()
        self.InHarmDilCenterEntry.set_text("Dilation Center, (x,y)")
        self.grid.attach_next_to(self.InHarmDilCenterEntry, self.InHarmDilScaleEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes layers entry for InHarmDil, puts in window
        self.InHarmDilLayersEntry = Gtk.Entry()
        self.InHarmDilLayersEntry.set_text("Number of Layers")
        self.grid.attach_next_to(self.InHarmDilLayersEntry, self.InHarmDilCenterEntry, Gtk.PositionType.RIGHT, 2, 1)

        #intializes Preview button, puts in window
        self.PreviewButton = Gtk.Button(label = "PREVIEW")
        self.PreviewButton.connect("clicked", self.on_PreviewButton_clicked)
        self.grid.attach_next_to(self.PreviewButton, self.AddInHarmDilButton, Gtk.PositionType.BOTTOM, 4, 1)

        #initializes Render button, puts in window
        self.RenderButton = Gtk.Button(label = "RENDER")
        self.RenderButton.connect("clicked", self.on_RenderButton_clicked)
        self.grid.attach_next_to(self.RenderButton, self.PreviewButton, Gtk.PositionType.RIGHT, 5, 1)

    #when Add Square button clicked, adds a new Square
    def on_AddSquareButton_clicked(self, widget):
    	pass

    #when Add N polygon button clicked, adds a new polygon
    def on_AddNPolygonButton_clicked(self, widget):
        pass

    #when Add Circle button clicked, adds a new circle
    def on_AddCircleButton_clicked(self, widget):
        pass

    #when Add Polygon from points button clicked, adds a new polygon
    def on_AddPointsPolyButton_clicked(self, widget):
        pass

    #when Add Rotation button clicked, adds a new rotation
    def on_AddRotButton_clicked(self, widget):
        pass

    #when Add Dilation button clicked, adds a new dilation
    def on_AddDilButton_clicked(self, widget):
        pass

    #when Add Cosine Harmonic Dilation button clicked, adds a new dilation
    def on_AddCosHarmDilButton_clicked(self, widget):
        pass

    #when Add Inward Harmonic Dilation button clicked, adds new dilation
    def on_AddInHarmDilButton_clicked(self, widget):
        pass

    #when Preview button clicked, previews in OpenSCAD
    def on_PreviewButton_clicked(self, widget):
        pass

    #when Render button clicked, renders stl of sculpture
    def on_RenderButton_clicked(self, widget):
        pass