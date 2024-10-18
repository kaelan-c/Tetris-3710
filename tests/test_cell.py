import pytest
from gamelogic.cell import Cell


@pytest.fixture
def cell():
    return Cell()


def test_DefaultState(cell):
    assert all([cell.getEmptyState(), cell.getColour() == (0, 0, 0)])


def test_FillCell(cell):
    colour = (255, 255, 255)
    cell.fillCell(colour)

    assert all([not cell.getEmptyState(), cell.getColour() == colour])
