from tetromino import Tetromino
from well import Well
from bag import Bag


class Tetris:
    def __init__(self):
        self.well = Well()
        self.bag = Bag()
        self.piece_store
        self.current_piece

    def spawnPiece(self):
        self.current_piece = self.bag.getNextPeice()

    def holdPiece(self):
        self.piece_store = self.current_piece
        self.current_piece = self.bag.getNextPeice()

