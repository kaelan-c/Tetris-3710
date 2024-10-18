import pytest
from gamelogic.bag import Bag


@pytest.fixture
def bag():
    return Bag()


def test_pieces(bag):
    assert len(bag.pieces) == 7


def test_getNextPeice(bag):
    for i in range(7):
        bag.getNextPeice()
    assert len(bag.bag) == 0


def test_viewNextPeice(bag):
    piece_viewed = bag.viewNextPeice()
    piece_popped = bag.getNextPeice()
    assert piece_viewed == piece_popped
