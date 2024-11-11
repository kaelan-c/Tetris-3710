from .cell import Cell
from .constants import GRID

class Well:
    def __init__(self):
        self.height = GRID["Height"]
        self.width = GRID["Width"]
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]  # Initialize the grid

    def generateGrid(self):
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = Cell()  # Assign a Cell instance to each position
        print("Grid generated")

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