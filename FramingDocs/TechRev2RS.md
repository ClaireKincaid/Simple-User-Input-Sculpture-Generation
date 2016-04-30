Technical Review 2 Reflection and Synthesis
Claire Kincaid
Coleman Ellis
Maximillian Schommer

Feedback and Decisions
	Feedback from classmates: 
		Ideas for GUI:
			Three menus: 
				Perlin noise
				Mathematical function
				Vector animation
			Constant preview
			preset/default functions
			“Character Building” type program
			Toggled menus
			Undo button
    	Ideas for Sculpture Generation Program: 
			Render using mayavi or pyglet
			Don’t render in cubes (from Sam’s team)
	Decisions going forward:
		Change GUI basis from gtk3 to gtk2 and/or mayavi
		Three nested menus that allow the user to traverse through the three
		We’re not really sure how to implement an undo button but it’s worth thinking about
		Render using mayavi (really cool 3D plotting program)
Review Process Reflection
	We realized from our feedback that a way to pass an output from one function to the input of another function is needed for each of our transformation functions. This means that all of our transformations should be adapted to work on the same kind of data, and then merged together. Our GUI is going to move towards the direction of integrating both MayaVi and gtk2. 
