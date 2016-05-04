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

        #initiates list of shapes
        self.Shapes = []

        #initializes list of transformations
        self.Transformations = []

        #initiates Gtk grid window
        self.grid = Gtk.Grid()
        self.add(self.grid)

        #Initializes Add Square Button, places in window
        self.AddSquareButton = Gtk.Button(label = "Add a Square")
        self.AddSquareButton.connect("clicked", self.on_AddSquareButton_clicked)
        self.grid.add(self.AddSquareButton)

        #initializes the length entry for add square, puts in window
        self.SquareLengthEntry = Gtk.Entry()
        self.SquareLengthEntry.set_text("Length")
        self.grid.attach_next_to(self.SquareLengthEntry, self.AddSquareButton, Gtk.PositionType.RIGHT, 2, 1)

        #initializes the center entry for add square, puts in window
        self.SquareCenterEntry = Gtk.Entry()
        self.SquareCenterEntry.set_text("Square Center, x, y")
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
        self.NCenterEntry.set_text("Polygon Center, x, y")
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
        self.CircCenterEntry.set_text("Circle Center, x, y")
        self.grid.attach_next_to(self.CircCenterEntry, self.CircRadiusEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes add rotation button, puts in window
        self.AddRotButton = Gtk.Button(label = "Add a Rotation")
        self.AddRotButton.connect("clicked", self.on_AddRotButton_clicked)
        self.grid.attach_next_to(self.AddRotButton, self.AddCircleButton, Gtk.PositionType.BOTTOM, 1, 1)

        #intializes angle entry for add rot, puts in window
        self.RotAngleEntry = Gtk.Entry()
        self.RotAngleEntry.set_text("Rotation Angle, (rad)")
        self.grid.attach_next_to(self.RotAngleEntry, self.AddRotButton, Gtk.PositionType.RIGHT, 2, 1)

        #initializes center entry for add rot, puts in window
        self.RotCenterEntry = Gtk.Entry()
        self.RotCenterEntry.set_text("Rotation Center, x, y")
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
        self.DilCenterEntry.set_text("Dilation Center, x, y")
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
        self.CosHarmDilCenterEntry.set_text("Dilation Center, x, y")
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
        self.InHarmDilCenterEntry.set_text("Dilation Center, x, y")
        self.grid.attach_next_to(self.InHarmDilCenterEntry, self.InHarmDilScaleEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes layers entry for InHarmDil, puts in window
        self.InHarmDilLayersEntry = Gtk.Entry()
        self.InHarmDilLayersEntry.set_text("Number of Layers")
        self.grid.attach_next_to(self.InHarmDilLayersEntry, self.InHarmDilCenterEntry, Gtk.PositionType.RIGHT, 2, 1)

        #initializes undo shape button, puts in window
        self.UndoShapeButton = Gtk.Button(label = "Undo Shape")
        self.UndoShapeButton.connect("clicked", self.on_UndoShapeButton_clicked)
        self.grid.attach_next_to(self.UndoShapeButton, self.AddInHarmDilButton, Gtk.PositionType.BOTTOM, 4, 1)

        #initializes undo transformation button, puts in window
        self.UndoTransButton = Gtk.Button(label = "Undo Transformation")
        self.UndoTransButton.connect("clicked", self.on_UndoTransButton_clicked)
        self.grid.attach_next_to(self.UndoTransButton, self.UndoShapeButton, Gtk.PositionType.RIGHT, 5, 1)

        #initializes clear shapes button, puts in window
        self.ClearShapesButton = Gtk.Button(label = "Clear Shapes")
        self.ClearShapesButton.connect("clicked", self.on_ClearShapesButton_clicked)
        self.grid.attach_next_to(self.ClearShapesButton, self.UndoShapeButton, Gtk.PositionType.BOTTOM, 4, 1)

        ##initializes clear transformations button, puts in window
        self.ClearTransButton = Gtk.Button("Clear Transformations")
        self.ClearTransButton.connect("clicked", self.on_ClearTransButton_clicked)
        self.grid.attach_next_to(self.ClearTransButton, self.ClearShapesButton, Gtk.PositionType.RIGHT, 5, 1)

        #intializes Preview button, puts in window
        self.PreviewButton = Gtk.Button(label = "PREVIEW")
        self.PreviewButton.connect("clicked", self.on_PreviewButton_clicked)
        self.grid.attach_next_to(self.PreviewButton, self.ClearShapesButton, Gtk.PositionType.BOTTOM, 4, 1)

        #initializes Render button, puts in window
        self.RenderButton = Gtk.Button(label = "RENDER")
        self.RenderButton.connect("clicked", self.on_RenderButton_clicked)
        self.grid.attach_next_to(self.RenderButton, self.PreviewButton, Gtk.PositionType.RIGHT, 5, 1)

    #when Add Square button clicked, adds a new Square
    def on_AddSquareButton_clicked(self, widget):
        Length = float(Gtk.Entry.get_text(self.SquareLengthEntry))
        Center = tuple(map(int, Gtk.Entry.get_text(self.SquareCenterEntry).split(",")))
        Angle = float(Gtk.Entry.get_text(self.SquareAngleEntry))
        print Center
        Square = Geometry.Square(Length, Center, Angle)
        self.Shapes.append(Square)

    #when Add N polygon button clicked, adds a new polygon
    def on_AddNPolygonButton_clicked(self, widget):
        N = int(Gtk.Entry.get_text(self.NSidesEntry))
        Radius = float(Gtk.Entry.get_text(self.NRadiusEntry))
        Center = tuple(map(int, Gtk.Entry.get_text(self.NCenterEntry).split(",")))
        Angle = float(Gtk.Entry.get_text(self.NAngleEntry))
        Polygon = Geometry.n_Sided_Polygon(N, Radius, Center, Angle)
        self.Shapes.append(Polygon)

    #when Add Circle button clicked, adds a new circle
    def on_AddCircleButton_clicked(self, widget):
        Radius = float(Gtk.Entry.get_text(self.CircRadiusEntry))
        Center = tuple(map(int, Gtk.Entry.get_text(self.CircCenterEntry).split(",")))
        Circle = Geometry.Circle(Radius, Center)
        self.Shapes.append(Circle)

    #when Add Rotation button clicked, adds a new rotation
    def on_AddRotButton_clicked(self, widget):
        Angle = float(Gtk.Entry.get_text(self.RotAngleEntry))
        Center = tuple(map(int, Gtk.Entry.get_text(self.RotCenterEntry).split(",")))
        Depth = int(Gtk.Entry.get_text(self.RotLayersEntry))
        Rotation = Geometry.Rotation(Angle, Center, Depth)
        self.Transformations.append(Rotation)

    #when Add Dilation button clicked, adds a new dilation
    def on_AddDilButton_clicked(self, widget):
        Factor = float(Gtk.Entry.get_text(self.DilScaleEntry))
        Center = tuple(map(int, Gtk.Entry.get_text(self.DilCenterEntry).split(",")))
        Depth = int(Gtk.Entry.get_text(self.DilLayersEntry))
        Dilation = Geometry.Dilation(Factor, Center, Depth)
        self.Transformations.append(Dilation)

    #when Add Cosine Harmonic Dilation button clicked, adds a new dilation
    def on_AddCosHarmDilButton_clicked(self, widget):
        Angle = float(Gtk.Entry.get_text(self.CosHarmDilAngleEntry))
        Center = tuple(map(int, Gtk.Entry.get_text(self.CosHarmDilCenterEntry).split(",")))
        Depth = int(Gtk.Entry.get_text(self.CosHarmDilLayersEntry))
        Dilation = Geometry.Cosine_Harmonic_Dilation(Angle, Center, Depth)
        self.Transformations.append(Dilation)

    #when Add Inward Harmonic Dilation button clicked, adds new dilation
    def on_AddInHarmDilButton_clicked(self, widget):
        Factor = float(Gtk.Entry.get_text(self.InHarmDilScaleEntry))
        Center = tuple(map(int, Gtk.Entry.get_text(self.InHarmDilCenterEntry).split(",")))
        Depth = int(Gtk.Entry.get_text(self.CosHarmDilLayersEntry))
        Dilation = Geometry.Inward_Harmonic_Dilation
        self.Transformations.append(Dilation)

    #when Undo shape button clicked, removes last shape added
    def on_UndoShapeButton_clicked(self, widget):
        self.Shapes.pop()

    #when Undo transofrmation button clicked, removes last transformation added
    def on_UndoTransButton_clicked(self, widget):
        self.Transformations.pop()

    #when clear shapes button clicked, removes all shapes
    def on_ClearShapesButton_clicked(self, widget):
        self.Shapes = []
        print self.Shapes

    #when clear transformations button clicked, removes all transformations
    def on_ClearTransButton_clicked(self, widget):
        self.Transformations = []
        print self.Transformations

    #when Preview button clicked, previews in OpenSCAD
    def on_PreviewButton_clicked(self, widget):
        pass

    #when Render button clicked, renders stl of sculpture
    def on_RenderButton_clicked(self, widget):
        pass

