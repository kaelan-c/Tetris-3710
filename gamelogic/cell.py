# *** CPSC 3710 - Term Project - Fall 2024
# *** Team Kernel Panic Attak - 3d Tetris:
# ***  - Ethan Fisher
# ***  - Patrick Bulbrook
# ***  - Kaelan Croucher


# The Cell class is represents a cell on the grid.
# It can exist in two states:
#       - Empty where it holds no model
#       - Full where it holds an instance of a cube model
class Cell:
    def __init__(self, pos):
        self.pos = pos
        self.model = None
        self.node = None
        self.empty = True

    # Fill_cell accepts a position, and a 3dModel file path
    # loads the file, renders it in position, and flips itself to full.
    def fill_cell(self, model, render):
        self.node = render.attachNewNode("New Cell Node")
        self.node.setPos(self.pos)
        self.model = model
        self.model.instanceTo(self.node)
        self.empty = False

    # empty_cell removes the loaded file, and flips itself to empty
    def empty_cell(self):
        if self.node:
            self.node.removeNode()
            self.model = None
            self.node = None
        self.empty = True

    # Set_pos sets the cells model position to a new position
    def set_pos(self, pos):
        self.pos = pos
        if self.node:
            self.node.setPos(pos)

    # Return the set position of the cell
    def get_pos(self):
        return self.pos

    # is_empty returns the current state of the cell
    def is_empty(self):
        return self.empty
