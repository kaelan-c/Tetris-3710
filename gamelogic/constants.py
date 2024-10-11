# Grid detail the paramerters of the games well class.
GRID = {
    "Width": 10,
    "Height": 40,
}

# Pieces details Tetromino name, 2d shape, offset, and colour
# Shape is represented by a 4x4 matrix of their starting orientation.

PIECES = {
    "I": {
        "name": "I",
        "shape2d": [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
        "offset": 0,
        "colour": (0, 255, 255),  # Cyan RGB Code
    },
    "J": {
        "name": "J",
        "shape2d": [[1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "offset": 0,
        "colour": (0, 0, 255),  # Blue RGB Code
    },
    "L": {
        "name": "L",
        "shape2d": [[0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "offset": 0,
        "colour": (255, 165, 0),  # Orange RGB Code
    },
    "O": {
        "name": "O",
        "shape2d": [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "offset": 0,
        "colour": (255, 255, 0),  # Yellow RGB Code
    },
    "S": {
        "name": "S",
        "shape2d": [[0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "offset": 0,
        "colour": (0, 255, 0),  # Green RGB Code
    },
    "T": {
        "name": "T",
        "shape2d": [[0, 1, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "offset": 0,
        "colour": (255, 0, 255),  # Magneta RGB Code
    },
    "Z": {
        "name": "Z",
        "shape2d": [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        "offset": 0,
        "colour": (255, 0, 0),  # Red RGB Code
    },
}
