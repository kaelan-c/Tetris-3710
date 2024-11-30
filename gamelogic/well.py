from .cell import Cell
from panda3d.core import NodePath, Vec3, LineSegs, LColor


class Well:
    def __init__(self, render_root, loader, width, depth, height):
        self.render_root = render_root
        self.loader = loader
        self.height = height
        self.render_height = height - 3
        self.width = width
        self.depth = depth
        self.grid = [[[None for z in range(self.height)]
                      for y in range(self.depth)]
                     for x in range(self.width)]
        self.generate_grid()

        self.grid_node = self.draw_grid()
        self.grid_node.reparentTo(self.render_root)

    # This function draws a semi transparent grid to screen as a player guide.
    def draw_grid(self):
        # Define line colour, transparency and thickness
        line_segs = LineSegs()
        line_segs.setColor(0.5, 0.5, 0.5, 0.5)
        line_segs.setThickness(0.1)

        for x in range(self.width + 1):
            start = Vec3(x, self.depth, 0)
            end = Vec3(x, self.depth, self.render_height)
            line_segs.moveTo(start)
            line_segs.drawTo(end)
        
        for y in range(self.depth + 1):
            start = Vec3(self.width, y, 0)
            end = Vec3(self.width, y, self.render_height)
            line_segs.moveTo(start)
            line_segs.drawTo(end)

        for z in range(self.render_height + 1):
            start = Vec3(self.width, 0, z)
            end = Vec3(self.width, self.depth, z)

            line_segs.moveTo(start)
            line_segs.drawTo(end)

            start = Vec3(0, self.depth, z)
            end = Vec3(self.width, self.depth, z)

            line_segs.moveTo(start)
            line_segs.drawTo(end)



        for z in range(self.render_height + 1):
            for x in range(self.width + 1):
                if z == 0:
                    line_segs.moveTo(Vec3(x, 0, z))
                    line_segs.drawTo(Vec3(x, self.depth, z))
            for y in range(self.depth + 1):
                if z == 0:
                    line_segs.moveTo(Vec3(0, y, z))
                    line_segs.drawTo(Vec3(self.width, y, z))

        #start = Vec3(0, 0, self.render_height)
        #end = Vec3(self.width, 0, self.render_height)
        #line_segs.moveTo(start)
        #line_segs.drawTo(end)

        start = Vec3(0, self.depth, self.render_height)
        end = Vec3(self.width, self.depth, self.render_height)

        line_segs.moveTo(start)
        line_segs.drawTo(end)

        #start = Vec3(0, 0, self.render_height)
        #end = Vec3(0, self.depth, self.render_height)

        #line_segs.moveTo(start)
        #line_segs.drawTo(end)

        start = Vec3(self.width, 0, self.render_height)
        end = Vec3(self.width, self.depth, self.render_height)

        line_segs.moveTo(start)
        line_segs.drawTo(end)

        return NodePath(line_segs.create())

    def generate_grid(self):
        for z in range(self.height):
            for y in range(self.depth):
                for x in range(self.width):
                    self.grid[x][y][z] = (Cell(self.render_root, self.loader))

    def validate_position(self, new_pos):
        for pos in new_pos:
            if (pos.x < 0 or pos.x >= self.width or
                    pos.y < 0 or pos.y >= self.depth or
                    pos.z < 0 or pos.z >= self.height):
                return False
            if not self.grid[int(pos.x)][int(pos.y)][int(pos.z)].is_empty():
                return False
        return True

    def place_piece(self, piece):
        for pos, cube in piece.model:
            self.grid[int(pos.x)][int(pos.y)][int(
                pos.z)].fill_cell(piece.shape_string, pos)

    def check_row(self):
        cleared_count = 0
        for z in range(self.render_height):
            if all(not self.grid[x][y][z].is_empty()
                   for x in range(self.width)
                   for y in range(self.depth)):
                self.clear_row(z)
                cleared_count += 1
            if z >= (self.render_height - 1):
                for x in range(self.width):
                    for y in range(self.depth):
                        if not self.grid[x][y][z].is_empty():
                            return -1
        self.shift_down(cleared_count)
        return cleared_count

    def clear_row(self, z):
        for x in range(self.width):
            for y in range(self.depth):
                self.grid[x][y][z].empty_cell()

    def shift_down(self, rows):
        if rows == 0:
            return
        for i in range(rows):
            for z in range(self.height):
                for x in range(self.width):
                    for y in range(self.depth):
                        if (z + 1) < self.render_height:
                            self.grid[x][y][z] = self.grid[x][y][z + 1]
                            if not self.grid[x][y][z + 1].is_empty():
                                self.grid[x][y][z + 1].empty_cell()
