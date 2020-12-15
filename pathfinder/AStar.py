from queue import PriorityQueue

import pygame

from mazecreator.MazeCreator import MazeCreator
from mazecreator.Picasso import Picasso
from mazecreator.RGBColours import RGBColours
from mazecreator.SquareState import SquareState


class AStar:
    """
    Poor man's implementation of A* Pathfinding algorithm
    """

    def __init__(self, visualise: bool = False):
        self.grid = MazeCreator().get_grid()
        self.open_set = PriorityQueue()
        self.start_pos = None
        self.end_pos = None
        self.path_found = False
        self.rows = len(self.grid)
        self.width = 800
        self.g_score = {}
        self.f_score = {}
        self.window = pygame.display.set_mode((self.width, self.width))
        self.window_title = 'AStar Pathfinder'
        self.run = True
        self.gap = self.width // self.rows
        self.path = None
        self.came_from = {}
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

    @staticmethod
    def get_heuristic(p1: tuple, p2: tuple):
        """
        Get approximate distance to p2
        :param p1: position 1
        :param p2: end position
        :return: approximate distance
        :rtype: int
        """
        x1, y1 = p1
        x2, y2 = p2

        return abs(x1 - x2) + abs(y1 - y2)

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

    def a_star(self):
        """
        A* pathfinding algorithm implementation
        :return: found path or not
        :rtype: bool
        """

        self.came_from = {}

        for row in self.grid:
            for s in row:
                sp = s.get_pos()
                self.g_score[sp] = float('inf')
                self.f_score[sp] = float('inf')

        self.g_score[self.start_pos] = 0
        self.f_score[self.start_pos] = self.get_heuristic(self.start_pos, self.end_pos)
        self.open_set.put((self.f_score[self.start_pos], self.start_pos))

        while self.run:
            self.draw(self.grid)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.run = False

            while not self.open_set.empty():
                current = self.open_set.get()
                current_f_score, current_pos = current
                current_row, current_col = current_pos

                if current_pos == self.end_pos:
                    checked_squares = 0
                    self.path = list()
                    self.path.append(self.end_pos)
                    for row in self.grid:
                        for s in row:
                            if s.state in [SquareState.VISITED, SquareState.START, SquareState.END]:
                                checked_squares += 1

                    curr = self.end_pos
                    while curr:
                        prev = self.came_from.get(curr)

                        self.path.append(prev)
                        curr = prev

                    self.path = self.path[:-1]
                    for move in self.path:
                        if move:
                            m_r, m_c = move
                            if move == self.end_pos:
                                self.grid[m_r][m_c].state = SquareState.END
                            else:
                                self.grid[m_r][m_c].state = SquareState.PATH

                    print(f'Found a solution, checked {checked_squares} squares, took {len(self.path)} moves')
                    print(f'Moves: {self.path}\n')

                    self.open_set = PriorityQueue()
                    break

                for valid_neighbour in Picasso.get_valid_neighbours(current_row, current_col, self.grid, self.rows):
                    if valid_neighbour.state != SquareState.VISITED:
                        valid_neighbour.state = SquareState.VISITED

                    tentative_g_score = self.g_score[current_pos] + 1
                    vn_pos = valid_neighbour.get_pos()

                    if tentative_g_score < self.g_score[vn_pos]:
                        self.came_from[vn_pos] = current_pos
                        self.g_score[vn_pos] = tentative_g_score
                        self.f_score[vn_pos] = self.g_score[vn_pos] + self.get_heuristic(vn_pos, self.end_pos)

                        if vn_pos not in self.open_set.queue:
                            self.open_set.put((self.f_score[vn_pos], vn_pos))
                            if self.visualise:
                                self.draw(self.grid)

        pygame.quit()
        return True if self.path else False


if __name__ == '__main__':
    a_star = AStar()
    path_found = a_star.a_star()

    print(f'Path found: {path_found}')
