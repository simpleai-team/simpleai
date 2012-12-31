# coding=utf-8
from simpleai.search import SearchProblem, astar
import copy


class EightPuzzleProblem(SearchProblem):
    ''' 8 puzzle problem, a smaller version of the fifteen puzzle:
        http://en.wikipedia.org/wiki/Fifteen_puzzle
        States are defined as a list of lists of integers, being 0 the
        empty tile.
        Actions denote where the empty tile goes, meaning that another tile
        takes its place.
    '''

    def __init__(self):
        initial = [
            [0, 2, 3],
            [1, 8, 5],
            [4, 7, 6]]
        super(EightPuzzleProblem, self).__init__(initial_state=initial)

    def _get_empty_coordinates(self, state):
        '''Returns the coordinates of the empty tile as dictionary'''
        for row in state:
            if 0 in row:
                break
        return {'row': state.index(row), 'column': row.index(0)}

    def _switch_tiles(self, state, tile1, tile2):
        '''Makes a copy of ``state`` and switches the ``tile1`` with
           the ``tile2``'''
        new_state = copy.deepcopy(state)
        aux = new_state[tile2[0]][tile2[1]]
        new_state[tile2[0]][tile2[1]] = new_state[tile1[0]][tile1[1]]
        new_state[tile1[0]][tile1[1]] = aux
        return new_state

    def actions(self, state):
        actions = []
        coordinates = self._get_empty_coordinates(state)
        if coordinates['row'] > 0:
            actions.append('up')
        if coordinates['row'] < 2:
            actions.append('down')
        if coordinates['column'] > 0:
            actions.append('left')
        if coordinates['column'] < 2:
            actions.append('right')
        return actions

    def result(self, state, action):
        coordinates = self._get_empty_coordinates(state)
        empty_tile = (coordinates['row'], coordinates['column'])
        if action == 'up' and coordinates['row'] > 0:
            tile2 = (coordinates['row'] - 1, coordinates['column'])
        if action == 'down' and coordinates['row'] < 2:
            tile2 = (coordinates['row'] + 1, coordinates['column'])
        if action == 'left' and coordinates['column'] > 0:
            tile2 = (coordinates['row'], coordinates['column'] - 1)
        if action == 'right' and coordinates['column'] < 2:
            tile2 = (coordinates['row'], coordinates['column'] + 1)
        new_state = self._switch_tiles(state, empty_tile, tile2)
        return new_state

    def is_goal(self, state):
        ''' Check if the state is goal:
            | 1 2 3 |
            | 4 5 6 |
            | 7 8   |
        '''
        return (state[0] == [1, 2, 3] and
                state[1] == [4, 5, 6] and state[2] == [7, 8, 0])

    def heuristic(self, state):
        total = 0
        row_no = 0
        for row in state:
            for i in row:
                total += abs(int((i - 1) / 3) - row_no) + \
                    abs((i - 1) % 3 - row.index(i))
            row_no += 1
        return total

problem = EightPuzzleProblem()

# NOTE: because of using a mutable type (list) as state, you can't use
# graph_search=True for this problem
result = astar(problem)

print result.path()
