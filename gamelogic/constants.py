# *** CPSC 3710 - Term Project - Fall 2024
# *** Team Kernel Panic Attak - 3d Tetris:
# ***  - Ethan Fisher
# ***  - Patrick Bulbrook
# ***  - Kaelan Croucher

# This file contains constants for in game objects
GRID = {
    "Width": 6,
    "Depth": 6,
    "Height": 22,
}

SPAWN = (3, 3, 18)

PIECES = {
    "I": {
        "name": "I",
        "shape": [(-1, 0), (0, 0), (1, 0), (2, 0)],
        "model": "assets/tetronimos/CubeTeal.glb",
    },
    "J": {
        "name": "J",
        "shape": [(0, 0), (1, 0), (1, 1), (1, 2)],
        "model": "assets/tetronimos/CubeBlue.glb",
    },
    "L": {
        "name": "L",
        "shape": [(2, 0), (1, 0), (1, 1), (1, 2)],
        "model": "assets/tetronimos/CubeOrange.glb",
    },
    "O": {
        "name": "O",
        "shape": [(0, 0), (0, 1), (1, 1), (1, 0)],
        "model": "assets/tetronimos/CubeYellow.glb",
    },
    "S": {
        "name": "S",
        "shape": [(0, 0), (0, 1), (1, 1), (1, 2)],
        "model": "assets/tetronimos/CubeGreen.glb",
    },
    "T": {
        "name": "T",
        "shape": [(0, 0), (1, 0), (2, 0), (1, 1)],
        "model": "assets/tetronimos/CubePurple.glb",
    },
    "Z": {
        "name": "Z",
        "shape": [(1, 0), (1, 1), (0, 1), (0, 2)],
        "model": "assets/tetronimos/CubeRed.glb",
    },
}
