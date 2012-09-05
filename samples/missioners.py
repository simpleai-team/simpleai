# coding=utf-8
from ai.models import Problem
from ai.methods import *

class MissionersProblem(Problem):
    '''Missioners and cannibals problem.'''

    def __init__(self):
        super(MissionersProblem, self).__init__(initial_state=(3, 3, 0))
        # each action has a printable text, and the number of missioners
        # and cannibals to move on that action
        self._actions = [('1c', (0,1)),
                         ('1m', (1, 0)),
                         ('2c', (0, 2)),
                         ('2m', (2, 0)),
                         ('1m1c', (1, 1))]

    def actions(self, s):
        '''Possible actions from a state.'''
        # we try to generate every possible state and then filter those
        # states that are valid
        return [a for a in self._actions if self._is_valid(self.result(s, a))]

    def _is_valid(self, s):
        '''Check if a state is valid.'''
        # valid states: no more cannibals than missioners on each side,
        # and numbers between 0 and 3
        return ((s[0] >= s[1] or s[0] == 0)) and \
                ((3 - s[0]) >= (3 - s[1]) or s[0] == 3) and \
                (0 <= s[0] <= 3) and \
                (0 <= s[1] <= 3)

    def result(self, s, a):
        '''Result of applying an action to a state.'''
        # result: boat on opposite side, and numbers of missioners and
        # cannibals updated according to the move
        if s[2] == 0:
            return (s[0] - a[1][0], s[1] - a[1][1], 1)
        else:
            return (s[0] + a[1][0], s[1] + a[1][1], 0)

    def is_goal(self, state):
        return state == (0, 0, 1)

    def heuristic(self, state):
        return (state[0] + state[1]) / 2

    def value(self, state):
        return 6 - state[0] - state[1]


problem = MissionersProblem()

result = breadth_first_search(problem)
#result = breadth_first_search(problem, graph_search=True)

#result = depth_first_search(problem)
#result = depth_first_search(problem, graph_search=True)

#result = limited_depth_first_search(problem, depth_limit=10)
#result = limited_depth_first_search(problem, depth_limit=11)
#result = limited_depth_first_search(problem, depth_limit=10, graph_search=True)
#result = limited_depth_first_search(problem, depth_limit=11, graph_search=True)

#result = iterative_limited_depth_first_search(problem)
#result = iterative_limited_depth_first_search(problem, graph_search=True)

#result = uniform_cost_search(problem)
#result = uniform_cost_search(problem, graph_search=True)

#result = greedy_search(problem)
#result = greedy_search(problem, graph_search=True)

#result = astar_search(problem)
#result = astar_search(problem, graph_search=True)

#result = beam_search(problem, beam_size=5)
#result = beam_search(problem, beam_size=5, graph_search=True)

#result = hill_climbing(problem)
#result = hill_climbing(problem, graph_search=True)

#result = hill_climbing_stochastic(problem)
#result = hill_climbing_stochastic(problem, graph_search=True)

#result = hill_climbing_first_choice(problem)
#result = hill_climbing_first_choice(problem, graph_search=True)

#result = simulated_annealing(problem)
#result = simulated_annealing(problem, graph_search=True)

print result.path()
