from cell import Cell
from constants import GRID


class Well:
    def __init__(self):
        self.height = GRID.Height
        self.width = GRID.Width

    def generateGrid(self):
        self.grid = []
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = Cell()
        print("set Grid Stub")

    def getGrid(self):
        return self.grid

    def getGridCell(self, x, y):
        return self.grid[x][y]

    def placePiece(self):
        print("Check place piece stub")

    def checkGrid(self):
        print("Check Grid Stub")

    def clearLine(self):
        print("Clear line Stub")
