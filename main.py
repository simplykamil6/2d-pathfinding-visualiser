import sys

from pathfinder.AStar import AStar
from pathfinder.BreadthFirst import BreadthFirst

algorithms = [(1, 'A*'), (2, 'Breadth First')]


def choose_algorithm():
    """
    Choose your pathfinding algorithm
    :return: algorithm chosen
    :rtype: int
    """

    print()
    for algo in algorithms:
        print(f'{algo[0]} - {algo[1]}')

    print()
    choice_input = None
    while choice_input not in [*[str(x[0]) for x in algorithms], 'q', 'Q']:
        choice_input = input('Please choose a pathfinding algorithm you would like to use(q to quit): ')

    if choice_input in 'qQ':
        print('See ya')
        sys.exit(0)

    return choice_input


def ask_visualiser():
    """
    Ask whether to visualise or not
    :rtype: bool
    """

    choice_input = 'X'
    while choice_input not in 'yYnN':
        choice_input = input('Visualise the algorithm?[y/n]: ')

    return choice_input in 'yY'


def find_path(algo: int, vis: bool):
    """
    Run the pathfinder
    :param algo: algorithm to run
    :param vis: should visualise?
    """
    algo = int(algo)

    path_found = False
    if algo == 1:
        a_star = AStar(vis)
        path_found = a_star.a_star()
    elif algo == 2:
        bf = BreadthFirst(vis)
        path_found = bf.bfs()

    if not path_found:
        print('Path cannot be found')


if __name__ == '__main__':
    find_path(choose_algorithm(), ask_visualiser())
