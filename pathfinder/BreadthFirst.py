from queue import Queue

import pygame

from mazecreator.MazeCreator import MazeCreator
from mazecreator.Picasso import Picasso
from mazecreator.RGBColours import RGBColours
from mazecreator.SquareState import SquareState


class BreadthFirst:
    """
    Poor man's implementation of Breadth First Pathfinding algorithm
    """

    def __init__(self, visualise: bool = False):
        self.grid = MazeCreator().get_grid()
        self.q = Queue()
        self.start_pos = None
        self.end_pos = None
        self.path_found = False
        self.rows = len(self.grid)
        self.width = 800
        self.window = pygame.display.set_mode((self.width, self.width))
        self.window_title = 'Breadth First Pathfinder'
        self.run = True
        self.gap = self.width // self.rows
        self.path = None
        pygame.display.set_caption(self.window_title)
        self.visualise = visualise

        for r in self.grid:
            for s in r:
                if s.state == SquareState.START:
                    self.start_pos = s.get_pos()
                elif s.state == SquareState.END:
                    self.end_pos = s.get_pos()

            if self.start_pos and self.end_pos:
                break

        print(f'\nMaze dimensions: {len(self.grid)}x{len(self.grid[0])}')
        print(f'Starting position: {self.start_pos}')
        print(f'Ending position: {self.end_pos}\n')

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

    def bfs(self):
        """
        Breadth first pathfinding algorithm implementation
        :return: found path or not
        :rtype: bool
        """

        self.q.put([self.start_pos])

        while self.run:
            self.draw(self.grid)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.run = False

            while not self.q.empty():
                v = self.q.get()
                v_last = v[len(v) - 1]

                sq_r, sq_c = v_last
                for valid_neighbour in Picasso.get_valid_neighbours(sq_r, sq_c, self.grid, self.rows):
                    if self.q.empty() and self.path:
                        break

                    if valid_neighbour.get_pos() == self.end_pos:
                        checked_squares = 0
                        self.path = v
                        self.path.append(self.end_pos)
                        for row in self.grid:
                            for s in row:
                                if s.state in [SquareState.VISITED, SquareState.START, SquareState.END]:
                                    checked_squares += 1
                        print(f'Found a solution, checked {checked_squares} squares, took {len(self.path)} moves')
                        print(f'Moves: {self.path}\n')

                        for i, move in enumerate(self.path):
                            vr, vc = move
                            if i == len(self.path) - 1:
                                self.grid[vr][vc].state = SquareState.END
                            else:
                                self.grid[vr][vc].state = SquareState.PATH

                        self.q = Queue()

                    if valid_neighbour.state != SquareState.VISITED:
                        if valid_neighbour.state != SquareState.END:
                            valid_neighbour.state = SquareState.VISITED

                        v_copy = v.copy()
                        v_copy.append(valid_neighbour.get_pos())

                        self.q.put(v_copy)
                        if self.visualise:
                            self.draw(self.grid)

        pygame.quit()
        return True if self.path else False


if __name__ == '__main__':
    bf = BreadthFirst()
    path_found = bf.bfs()

    print(f'Path found: {path_found}')
