# Grid detail the paramerters of the games well class.
GRID = {
    "Width": 5,
    "Depth": 5,
    "Height": 15,
}

SPAWN = (2, 2, 11)

CELL = {
    "Size": 1,
}

PIECES = {
    "I": {
        "name": "I",
        "shape": [(0, 0), (1, 0), (2, 0)],
        "color": (0, 255, 255, 1),  # Cyan RGB Code
    },
    "J": {
        "name": "J",
        "shape": [(1, 0), (1, 1), (1, 2)],
        "color": (0, 0, 255, 1),  # Blue RGB Code
    },
    "L": {
        "name": "L",
        "shape": [(0, 0), (0, 1), (0, 2)],
        "color": (255, 165, 0, 1),  # Orange RGB Code
    },
    "O": {
        "name": "O",
        "shape": [(0, 0), (1, 1), (1, 1)],
        "color": (255, 255, 0, 1),  # Yellow RGB Code
    },
    "S": {
        "name": "S",
        "shape": [(0, 0), (1, 0), (1, 1)],
        "color": (0, 255, 0, 1),  # Green RGB Code
    },
    "T": {
        "name": "T",
        "shape": [(0, 0), (1, 0), (2, 0), (1, 1)],
        "color": (255, 0, 255, 1),  # Magneta RGB Code
    },
    "Z": {
        "name": "Z",
        "shape": [(0, 0), (1, 0), (1, 1)],
        "color": (255, 0, 0, 1),  # Red RGB Code
    },
}
