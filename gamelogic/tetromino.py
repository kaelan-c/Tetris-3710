# *** CPSC 3710 - Term Project - Fall 2024
# *** Team Kernel Panic Attak - 3d Tetris:
# ***  - Ethan Fisher
# ***  - Patrick Bulbrook
# ***  - Kaelan Croucher

from math import cos, sin, radians
from panda3d.core import Point3
from .cell import Cell


# Tetromino Class responsible for containing 3d model,
# piece position and piece transformations.
class Tetromino:
    def __init__(self, name, shape, origin, model):
        self.name = name
        self.shape = shape
        self.origin = Point3(origin)
        self.model = model
        self.cells = []

        # Pre calc cos of 90 degrees for on grid rotation
        self.cos = cos(radians(90))
        self.sin = sin(radians(90))

    # Render Piece is responsible for rendering each cell in the piece in the
    # correct position.
    def render_piece(self, render):
        # For each cell in the peice, fill a cell with model, and spawn pos
        for x, y in self.shape:
            pos = self.origin + Point3(x, y, 0)
            cell = Cell(pos)
            cell.fill_cell(self.model, render)
            self.cells.append(cell)

    # Rotate X rotates the piece 90 degrees around the X axis
    def rotate_x(self):
        anchor = self.get_rotation_anchor()
        new_position = []
        # Rotate each cell in cells[] around by 90 degrees around anchor
        for cell in self.cells:
            pos = cell.get_pos()

            rot_pos = Point3(
                pos.x - anchor.x, pos.y - anchor.y, pos.z - anchor.z)

            new_y = (rot_pos.y * self.cos) - (rot_pos.z * self.sin)
            new_z = (rot_pos.y * self.sin) + (rot_pos.z * self.cos)
            new_pos = Point3(rot_pos.x + anchor.x,
                             new_y + anchor.y, new_z + anchor.z)
            new_position.append(new_pos)

        return new_position

    # Rotate Y rotates the piece 90 degrees around the Y axis.
    def rotate_y(self):
        anchor = self.get_rotation_anchor()
        new_position = []
        # Rotate each cell in cells[] around by 90 degrees around anchor
        for cell in self.cells:
            pos = cell.get_pos()
            rot_pos = Point3(
                pos.x - anchor.x, pos.y - anchor.y, pos.z - anchor.z)
            # Perform the rotation around the Y axis
            new_x = (rot_pos.x * self.cos) + (rot_pos.z * self.sin)
            new_z = (-rot_pos.x * self.sin) + (rot_pos.z * self.cos)

            # Translate back to the original anchor
            new_pos = Point3(new_x + anchor.x,
                             rot_pos.y + anchor.y, new_z + anchor.z)
            new_position.append(new_pos)
        return new_position

    # Rotate Z rotates the piece 90 degrees around the Y axis
    def rotate_z(self):
        anchor = self.get_rotation_anchor()
        new_position = []
        # Rotate each cell in cells[] around by 90 degrees around anchor
        for cell in self.cells:
            pos = cell.get_pos()
            # Translate to the anchor
            rot_pos = Point3(
                pos.x - anchor.x, pos.y - anchor.y, pos.z - anchor.z)

            # Perform the rotation around the Z axis
            new_x = (rot_pos.x * self.cos) - (rot_pos.y * self.sin)
            new_y = (rot_pos.x * self.sin) + (rot_pos.y * self.cos)

            # Translate back to the original anchor
            new_pos = Point3(new_x + anchor.x, new_y +
                             anchor.y, rot_pos.z + anchor.z)
            new_position.append(new_pos)

        return new_position

    # Move Piece translates the piece on a 3d grid by passed amount for x, y, z
    def move_piece(self, x, y, z):
        # Check new positions against the grid bounds and block positions
        new_position = []
        # Translate each sell by specified amount
        for cell in self.cells:
            pos = cell.get_pos()
            new_position.append(Point3(pos.x + x, pos.y + y, pos.z + z))

        return new_position

    # Set position updates the pieces position with passed position.
    # this is done to allow for grid validation of new_position arrays
    # returned from transformation functions.
    def set_position(self, new_pos):
        for i, cell in enumerate(self.cells):
            cell.set_pos(new_pos[i])

    # This iterates through a the piece's model list, and removes the model
    # being rendered at each position
    def remove_piece(self):
        for cell in self.cells:
            cell.empty_cell()

    # Rotation anchor returns the point or rotation for each piece
    def get_rotation_anchor(self):
        return self.cells[1].get_pos()
