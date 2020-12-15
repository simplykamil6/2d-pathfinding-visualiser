import pygame

from mazecreator.RGBColours import RGBColours
from mazecreator.Square import Square
from mazecreator.SquareState import SquareState


class Picasso:
    """
    Paint master 2D
    """

    def __init__(self, window: pygame.display, rows: int, width: int):
        self.window = window
        self.width = width
        self.rows = rows
        self.gap = self.width // self.rows
        self.square_width = 16

    @staticmethod
    def get_valid_neighbours(r: int, c: int, grid: list, rows: int):
        """
        Find valid neighbours for a square:
        valid means it's not a wall, has not been visited
        :param r: row
        :param c: column
        :param grid: Maze grid
        :param rows: number of rows
        :return: valid neighbours
        """

        up_neighbour = (r, c + 1)
        down_neighbour = (r, c - 1)
        left_neighbour = (r - 1, c)
        right_neighbour = (r + 1, c)

        neighbours = [up_neighbour, down_neighbour, left_neighbour, right_neighbour]
        v_neighbours = list()

        for neighbour in neighbours:
            r, c = neighbour
            if r in range(rows) and c in range(rows):
                if grid[r][c].state not in [SquareState.VISITED, SquareState.WALL, SquareState.START]:
                    v_neighbours.append(grid[r][c])

        return v_neighbours

    def get_grid(self):
        """
        Create and return the grid
        :rtype: list
        """

        grid = list()
        for row in range(self.rows):
            grid.append(list())
            for col in range(self.rows):
                square = Square(row, col, self.square_width)
                grid[row].append(square)

        return grid

    def draw_grid(self):
        """
        Draw the grid
        :rtype: None
        """

        for i in range(self.rows):
            pygame.draw.line(self.window, RGBColours.GREY, (0, i * self.gap), (self.width, i * self.gap))
            for j in range(self.rows):
                pygame.draw.line(self.window, RGBColours.GREY, (j * self.gap, 0), (j * self.gap, self.width))

    def draw(self, grid: list):
        """
        Draw the grid and squares
        :rtype: None
        """

        self.window.fill(RGBColours.WHITE)

        for row in grid:
            for square in row:
                square.draw(self.window)

        self.draw_grid()
        pygame.display.update()

    def get_clicked_pos(self, pos):
        """
        Get row, col that was clicked
        :param pos: position
        :type pos: tuple
        :return: row, col
        :rtype: tuple
        """

        y, x = pos
        return y // self.gap, x // self.gap
