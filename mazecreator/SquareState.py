from enum import Enum


class SquareState(Enum):
    START, END, EMPTY, WALL, VISITED, PATH = range(0, 6)
