#!/usr/bin/python
import pyglet
import random
from pyglet.gl import *

class VoxelEngine:
    def __init__(self, w, h, d):
        """ Create a new voxel engine. """
        self.w = w
        self.h = h
        self.d = d
        # Create the 3D array
        self.voxels = []
        for _ in range(self.w):
            self.voxels.append([[0 for _ in range(self.d)] for _ in range(self.h)])

    def set(self, x, y, z, value):
        """ Set the value of the voxel at position (x, y, z). """
        self.voxels[x][y][z] = value

    def draw(self):
        """ Draw the voxels. """
        vertices = (
            0, 0, 0,    # vertex 0
            0, 0, 1,    # vertex 1
            0, 1, 0,    # vertex 2
            0, 1, 1,    # vertex 3
            1, 0, 0,    # vertex 4
            1, 0, 1,    # vertex 5
            1, 1, 0,    # vertex 6
            1, 1, 1,    # vertex 7
        )
        indices = (
            0, 1, 3, 2, # top face
            4, 5, 7, 6, # bottom face
            0, 4, 6, 2, # left face
            1, 5, 7, 3, # right face
            0, 1, 5, 4, # down face
            2, 3, 7, 6, # up face
        )
        colors = (
            (107, 83, 28), # dirt
            (18, 124, 39), # grass
            (168, 142, 95), # wood
            (88, 181, 74), # leaves
        )
        # Loop through each voxel
        for x in range(self.w):
            for y in range(self.h):
                for z in range(self.d):
                    voxel_type = self.voxels[x][y][z]
                    if voxel_type != 0:
                        glTranslated(x, y, z)
                        glColor3ub(*colors[voxel_type-1])
                        pyglet.graphics.draw_indexed(8, GL_QUADS,
                            indices, ('v3i', vertices))
                        glTranslated(-x, -y, -z)


class Window(pyglet.window.Window):
    def __init__(self):
        super(Window, self).__init__(resizable=True, caption='PyVoxel')
        self.voxel = VoxelEngine(20, 25, 20)
        glClearColor(0.7, 0.7, 0.8, 1)
        self.generate_island(0, 5, 0)
        self.generate_island(0, 0, 10)

    def generate_island(self, x, y, z):
        # a flying island
        for dx in range(random.randint(4, 10)):
            for dz in range(random.randint(4, 10)):
                for dy in range(random.randint(4, 11)):
                    self.voxel.set(x + dx, 15 - dy + y, z + dz, 1)
                self.voxel.set(x + dx, y +15, z + dz, 2)
        # a tree
        for i in range(15, 18):
            self.voxel.set(x+2, y+i, z+4, 3)
        for i in range(1, 4):
            for j in range(3, 6):
                self.voxel.set(x+i, y+18, z+j, 4)
        self.voxel.set(x+2, y+19, z+4, 4)


    def setup_3D(self):
        """ Setup the 3D matrix """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70, self.width / float(self.height), 0.1, 200)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(24, 20, 20, 0, 10, 4, 0, 1, 0)

if __name__ == '__main__':
    window = Window()
    pyglet.app.run()
    import sys
    global xrot, yrot, d
    win = pyglet.window.Window(width=720, height=720, resizable=True, visible=False,
        config=pyglet.gl.Config(sample_buffers=1, samples=4, double_buffer=True, depth_size=24))
    xrot = yrot = d = 0

    def on_resize(width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70, 1.0*width/height, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    win.on_resize = on_resize

    @win.event
    def on_mouse_motion(x, y, dx, dy):
        global xrot, yrot
        yrot += dx * 0.3
        xrot += dy * 0.3

    @win.event
    def on_draw():
        global xrot, yrot, d
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -1.5)
        glRotatef(xrot, 1.0, 0.0, 0.0)
        glRotatef(yrot, 0.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        glTexCoord3f(0.0, 0.0, d)
        glVertex3f(1, -1, 0)
        glTexCoord3f(0.0, 1.0, d)
        glVertex3f(1, 1, 0)
        glTexCoord3f(1.0, 1.0, d)
        glVertex3f(-1, 1, 0)
        glTexCoord3f(1.0, 0.0, d)
        glVertex3f(-1, -1, 0)
        glEnd()

    def update(dt):
        global d
        d += dt * 0.1
        if d > 1.0:
            d -= 1.0

    pyglet.clock.schedule_interval(update, 1/30.0)

    win.set_visible()
    win.set_exclusive_mouse()
    pyglet.app.run()
