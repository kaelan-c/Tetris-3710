# Grid detail the paramerters of the games well class.
GRID = {
    "Width": 5,
    "Depth": 5,
    "Height": 15,
}

SPAWN = (2, 2, 11)

PIECES = {
    "I": {
        "name": "I",
        "shape": [(0, 0), (1, 0), (2, 0)],
        "shape_string": "assets/tetronimos/CubeTeal.glb",
    },
    "J": {
        "name": "J",
        "shape": [(0, 0), (1, 0), (1, 1), (1, 2)],
        "shape_string": "assets/tetronimos/CubeBlue.glb",
    },
    "L": {
        "name": "L",
        "shape": [(2, 0), (1, 0), (1, 1), (1, 2)],
        "shape_string": "assets/tetronimos/CubeOrange.glb",
    },
    "O": {
        "name": "O",
        "shape": [(0, 0), (0, 1), (1, 1), (1, 0)],
        "shape_string": "assets/tetronimos/CubeYellow.glb",
    },
    "S": {
        "name": "S",
        "shape": [(0, 0), (0, 1), (1, 1), (1, 2)],
        "shape_string": "assets/tetronimos/CubeGreen.glb",
    },
    "T": {
        "name": "T",
        "shape": [(0, 0), (1, 0), (2, 0), (1, 1)],
        "shape_string": "assets/tetronimos/CubePurple.glb",
    },
    "Z": {
        "name": "Z",
        "shape": [(1, 0), (1, 1), (0, 1), (0, 2)],
        "shape_string": "assets/tetronimos/CubeRed.glb",
    },
}
