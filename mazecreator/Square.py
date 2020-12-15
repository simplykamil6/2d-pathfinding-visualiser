import pygame

from mazecreator.RGBColours import RGBColours
from mazecreator.SquareState import SquareState


class Square:
    """
    Grid square object
    """
    width: int

    def __init__(self, row: int, col: int, width: int, state=SquareState.EMPTY):
        self.width = width
        self.x = row * self.width
        self.y = col * self.width
        self.row = row
        self.col = col
        self.state = state

    def __repr__(self):
        return f'{self.row}:{self.col} - {self.width} - {self.state.value}'

    def reset(self):
        self.state = SquareState.EMPTY

    def is_visited(self):
        return self.state == SquareState.VISITED

    def is_wall(self):
        return self.state == SquareState.WALL

    def is_start(self):
        return self.state == SquareState.START

    def is_end(self):
        return self.state == SquareState.END

    def is_open(self):
        return self.state == SquareState.OPEN

    def make_visited(self):
        self.state = SquareState.VISITED

    def make_wall(self):
        self.state = SquareState.WALL

    def make_start(self):
        self.state = SquareState.START

    def make_end(self):
        self.state = SquareState.END

    def make_checked(self):
        self.state = SquareState.CHECKED

    def get_pos(self):
        """
        Return position of a square in grid
        :return: position
        :rtype: tuple
        """

        return self.row, self.col

    def draw(self, window: pygame.display):
        """
        Draw the square on a grid
        :param window: Window to draw in
        :type window: pygame.display
        :rtype: None
        """

        def _get_colour_from_state():
            """
            Get the colour square should be depending on its state
            :return: colour RGB as a triple (3-tuple, tuple with 3 values)
            :rtype: tuple
            """

            if self.state == SquareState.EMPTY:
                return RGBColours.WHITE
            elif self.state == SquareState.START:
                return RGBColours.GREEN
            elif self.state == SquareState.END:
                return RGBColours.RED
            elif self.state == SquareState.WALL:
                return RGBColours.BLACK
            elif self.state == SquareState.VISITED:
                return RGBColours.YELLOW
            elif self.state == SquareState.PATH:
                return RGBColours.PURPLE

        # noinspection PyTypeChecker
        pygame.draw.rect(window, _get_colour_from_state(), (self.x, self.y, self.width, self.width))
