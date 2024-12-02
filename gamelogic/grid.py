# *** CPSC 3710 - Term Project - Fall 2024
# *** Team Kernel Panic Attak - 3d Tetris:
# ***  - Ethan Fisher
# ***  - Patrick Bulbrook
# ***  - Kaelan Croucher

from panda3d.core import LineSegs, NodePath, Vec3
from .cell import Cell


# The grid class is responsible for maintaining a grid of cells
# and checking for cleared lines or game over states
class Grid:
    def __init__(self, width, depth, height):
        self.height = height
        # Render height allows for 3 blocks above the grid for spawn
        # and initial rotation purposes
        self.render_height = height - 3
        self.width = width
        self.depth = depth
        # Fill grid with empty cells according to dimension
        self.grid = [[[Cell((x, y, z)) for z in range(self.height)]
                      for y in range(self.depth)]
                     for x in range(self.width)]

    # Draw grid renders a white grid to the screen
    def render_grid(self, render):
        # Define line colour, transparency and thickness
        line_segs = LineSegs()
        line_segs.setColor(0.5, 0.5, 0.5, 0.5)
        line_segs.setThickness(0.1)

        for x in range(self.width + 1):
            # Draw vertical along x axis of grid
            line_segs.moveTo(Vec3(x, self.depth, 0))
            line_segs.drawTo(Vec3(x, self.depth, self.render_height))
            # Draw bottom grid lines along x axis
            line_segs.moveTo(Vec3(x, 0, 0))
            line_segs.drawTo(Vec3(x, self.depth, 0))

        for y in range(self.depth + 1):
            # Draw vertical lines along y axis
            line_segs.moveTo(Vec3(self.width, y, 0))
            line_segs.drawTo(Vec3(self.width, y, self.render_height))
            # Draw bottom grid lines along y axis
            line_segs.moveTo(Vec3(0, y, 0))
            line_segs.drawTo(Vec3(self.width, y, 0))

        # Draw horizontal lines along x and y axis
        for z in range(self.render_height + 1):
            # Draw along y axis
            line_segs.moveTo(Vec3(self.width, 0, z))
            line_segs.drawTo(Vec3(self.width, self.depth, z))
            # Draw along x axis
            line_segs.moveTo(Vec3(0, self.depth, z))
            line_segs.drawTo(Vec3(self.width, self.depth, z))

        # render the grid lines
        NodePath(line_segs.create()).reparentTo(render)

    # Validates a passed position does not occupy any filled cells
    # or any position falls outside the allowable playing field
    def validate_position(self, new_pos):
        for pos in new_pos:
            if (
                pos.x < 0
                or pos.x >= self.width
                or pos.y < 0
                or pos.y >= self.depth
                or pos.z < 0
                or pos.z >= self.height
            ):
                return False
            if not self.grid[int(pos.x)][int(pos.y)][int(pos.z)].is_empty():
                return False
        return True

    # Takes a peice and converts it to cells on the grid
    def place_piece(self, piece, render):
        # For each cell in piece, fill a grid cell with the same model
        for cell in piece.cells:
            pos = cell.get_pos()
            self.grid[int(pos.x)][int(pos.y)][int(pos.z)].fill_cell(
                piece.model, render
            )

    # Checks each layer of the grid clearing full rows, and returning total
    # number of full rows.
    def check_row(self, render):
        cleared_count = 0
        # Iterate through grid, layer by layer.
        for z in range(self.render_height):
            # If every cell is filled, clear line
            if all(
                not self.grid[x][y][z].is_empty()
                for x in range(self.width)
                for y in range(self.depth)
            ):
                self.clear_row(z, render)
                cleared_count += 1
            # if there is a block filled at render height, game over
            if z >= (self.render_height - 1):
                for x in range(self.width):
                    for y in range(self.depth):
                        if not self.grid[x][y][z].is_empty():
                            cleared_count = -1
        # Return number of rows cleared or -1 for game over
        return cleared_count

    # Clears the row at the passed z value, calls shift down to correct the
    # grid.
    def clear_row(self, z, render):
        # Iterate through layer and clear all the cells, call shift down
        # to move all pieces above layer down one block
        for x in range(self.width):
            for y in range(self.depth):
                self.grid[x][y][z].empty_cell()
        self.shift_down(z, render)

    # Shifts each cell of the grid after the specified cleared row.
    def shift_down(self, cleared, render):
        # Iterate through grid from cleared row to render height -1
        for z in range(cleared, self.render_height - 1):
            for x in range(self.width):
                for y in range(self.depth):
                    # If a the cell above current iterator is not empty
                    if not self.grid[x][y][z + 1].is_empty():
                        # Fill current cell with cell above, empty cell above
                        model = self.grid[x][y][z + 1].model
                        self.grid[x][y][z].fill_cell(model, render)
                        self.grid[x][y][z + 1].empty_cell()
