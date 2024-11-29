from .cell import Cell
from panda3d.core import NodePath, Vec3, LineSegs, LColor, Point3

class Well:
    def __init__(self, render_root, height, width, depth):
        self.render_root = render_root
        self.height = height
        self.width = width
        self.depth = depth
    
        self.grid = [[[Cell() for z in range(depth)] for y in range(height)] for x in range(width)]

        self.grid_node = self.draw_grid()
        self.grid_node.reparentTo(self.render_root)

    def draw_grid(self):
        line_segs = LineSegs()
        line_segs.setColor(LColor(0.6, 0.5, 0.6, 0.3))
        line_segs.setThickness(1)

        for x in range(self.width + 1):
            for y in range(self.depth + 1):
                start = Vec3(x, y, 0)
                end = Vec3(x, y, self.height)
                line_segs.moveTo(start)
                line_segs.drawTo(end)

        for z in range(self.height + 1):
            for x in range(self.width + 1):
                line_segs.moveTo(Vec3(x, 0, z))
                line_segs.drawTo(Vec3(x, self.depth, z))
            for y in range(self.depth + 1):
                line_segs.moveTo(Vec3(0, y, z))
                line_segs.drawTo(Vec3(self.width, y, z))

        return NodePath(line_segs.create())


    def getGrid(self):
        return self.grid

    def getGridCell(self, x, y):
        return self.grid[x][y]

    def placePiece(self):
        print("Check place piece stub")

    def checkGrid(self):
        for i in range(self.height):
            cell_count = 0
            for j in range(self.width):
                empty, colour = self.grid[i][j].getStatus()
                if not empty:
                    cell_count += 1
            if cell_count == self.width:
                self.clearLine(i)

    def clearLine(self, i):
        del self.grid[i]
        self.grid.insert(0, [Cell()] * self.width)
