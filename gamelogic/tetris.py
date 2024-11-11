from .tetromino import Tetromino
from .well import Well
from .bag import Bag


class Tetris:
    def __init__(self):
        self.well = Well()
        self.bag = Bag()

    def spawnPiece(self):
        print("Spawn Peice Stub")

    def holdPiece(self):
        print("Spawn Peice Stub")
