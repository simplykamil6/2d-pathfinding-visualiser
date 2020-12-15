import os

import pygame

from mazecreator.Picasso import Picasso
from mazecreator.Square import Square
from mazecreator.SquareState import SquareState


class MazeCreator:
    """
    Create the maze
    """

    def __init__(self):
        self.rows = 50
        self.window = None
        self.width = 800
        self.title = 'Maze Creator'
        self.start_square, self.start_pos = None, None
        self.end_square, self.end_pos = None, None
        self.maze_file = f'{os.getcwd()}/maze'

    def get_grid(self):
        """
        Create and return the grid
        :return: grid
        :rtype: list
        """

        def _remove_maze_file():
            try:
                os.remove(self.maze_file)
            except FileNotFoundError:
                pass

        def _export_grid():
            with open(self.maze_file, 'w') as output_file:
                for row in grid:
                    output_file.write(f'{str(row)}\n')
            output_file.close()

        def _load_grid():
            """
            Load  from the saved file
            :return: grid
            :exception: Can throw if file doesn't exist
            """
            file_lines = list()
            new_grid = list()

            with open(self.maze_file, 'r') as input_file:
                for file_line in input_file:
                    file_lines.append(file_line)
            input_file.close()

            for file_line in file_lines:
                grid_line = list()

                for square_line_object in file_line.split(','):
                    objects = [x.strip().replace('[', '').replace(']', '') for x in square_line_object.split(' - ')]
                    sq_pos = objects[0].split(':')
                    sq_pos_x, sq_pos_y = int(sq_pos[0]), int(sq_pos[1])
                    sq_width = int(objects[1])
                    sq_state = int(objects[2])

                    if sq_state == 0:
                        st = SquareState.START
                    elif sq_state == 1:
                        st = SquareState.END
                    elif sq_state == 3:
                        st = SquareState.WALL
                    else:
                        st = SquareState.EMPTY

                    grid_line.append(Square(sq_pos_x, sq_pos_y, sq_width, st))
                new_grid.append(grid_line)

            return new_grid

        window = pygame.display.set_mode((self.width, self.width))
        picasso = Picasso(window, 50, self.width)
        grid = picasso.get_grid()
        pygame.display.set_caption(self.title)

        run = True
        while run:
            picasso.draw(grid)

            for event in pygame.event.get():
                # noinspection PyArgumentList
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False
                elif pygame.mouse.get_pressed()[0]:
                    clicked_row, clicked_col = picasso.get_clicked_pos(pygame.mouse.get_pos())
                    square = grid[clicked_row][clicked_col]
                    square_pos = square.get_pos()
                    square_state = square.state

                    if square_state != SquareState.WALL:
                        if not self.start_square and square_pos != self.end_pos:
                            self.start_square = square
                            self.start_pos = square_pos
                            self.start_square.make_start()
                        elif not self.end_square and square_pos != self.start_pos:
                            self.end_square = square
                            self.end_pos = square_pos
                            self.end_square.make_end()
                    if square_pos not in (self.start_pos, self.end_pos):
                        square.make_wall()

                elif pygame.mouse.get_pressed()[2]:
                    clicked_row, clicked_col = picasso.get_clicked_pos(pygame.mouse.get_pos())
                    square = grid[clicked_row][clicked_col]

                    if square == self.start_square:
                        self.start_square, self.start_pos = None, None
                    elif square == self.end_square:
                        self.end_square, self.end_pos = None, None

                    square.reset()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.start_pos and self.end_pos:
                            run = False
                    elif event.key == pygame.K_l:
                        grid = _load_grid()

                        # look for start_square and end_square
                        start_found, end_found = False, False
                        for g_row in grid:
                            for s in g_row:
                                if s.state == SquareState.START:
                                    start_found = True
                                    self.start_square = s
                                    self.start_pos = s.get_pos()
                                if s.state == SquareState.END:
                                    end_found = True
                                    self.end_square = s
                                    self.end_pos = s.get_pos()

                        if not start_found:
                            self.start_square, start_pos = None, None
                        if not end_found:
                            self.end_square, self.end_pos = None, None

                    elif event.key == pygame.K_c:
                        for r in grid:
                            for s in r:
                                s.reset()
                        self.start_square, start_pos = None, None
                        self.end_square, self.end_pos = None, None
                    elif event.key == pygame.K_d:
                        _remove_maze_file()
                    elif event.key == pygame.K_e:
                        _export_grid()

        pygame.quit()
        return grid


if __name__ == '__main__':
    GRID = MazeCreator().get_grid()
