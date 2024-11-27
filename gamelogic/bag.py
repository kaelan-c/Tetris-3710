import random
from .constants import PIECES
from .tetromino import Tetromino
from .constants import PIECES
from .tetromino import Tetromino

from .constants import PIECES
from .tetromino import Tetromino


class Bag:
    def __init__(self):
        self.pieces = self.genPieces()
        self.bag = self.fillBag()

    def genPieces(self):
        pieces = []
        for p_key, p in PIECES.items():
            pieces.append(Tetromino(p.get("name"), p.get("shape2d"),
                                    p.get("offset"), p.get("colour")))
        return pieces

    def fillBag(self):
        return random.sample(self.pieces, len(self.pieces))

    def viewNextPeice(self):
        return self.bag[-1]if self.bag else None

    def getNextPiece(self):
        if not self.bag:
            self.fillBag()
        return self.bag.pop()