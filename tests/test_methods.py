# coding=utf-8
import unittest
from tests.dummies import DummyProblem, GOAL
from ai.methods import (breadth_first_search, depth_first_search,
                        limited_depth_first_search,
                        iterative_limited_depth_first_search,
                        uniform_cost_search, greedy_search, astar_search,
                        beam_search, hill_climbing, hill_climbing_stochastic,
                        hill_climbing_first_choice, simulated_annealing)


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.problem = DummyProblem()
        self.problem.initial_state = 'i'

    def test_breadth_first_search(self):
        result = breadth_first_search(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_depth_first_search(self):
        result = depth_first_search(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_limited_depth_first_search(self):
        result = limited_depth_first_search(self.problem, depth_limit=3)
        self.assertEquals(result, None)

        result = limited_depth_first_search(self.problem, depth_limit=6)
        self.assertEquals(result.state, GOAL)

    def test_iterative_limited_depth_first_search(self):
        result = iterative_limited_depth_first_search(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_uniform_cost_search(self):
        result = uniform_cost_search(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_greedy_search(self):
        result = greedy_search(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_astar_search(self):
        result = astar_search(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_beam_search(self):
        result = beam_search(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_hill_climbing(self):
        result = hill_climbing(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_hill_climbing_stochastic(self):
        result = hill_climbing_stochastic(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_hill_climbing_first_choice(self):
        result = hill_climbing_first_choice(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_simulated_annealing(self):
        # give the problem an actions function that always
        # goes up, to test if simulated_annealing takes the
        # correct states
        def dummy_actions(state):
            if len(state) < len(GOAL):
                return {'i': 'a',
                        'a': 'b',
                        'b': 'c',
                        'c': 'a'}[state[-1]]
            else:
                return []
        self.problem.actions = dummy_actions
        result = simulated_annealing(self.problem)
        self.assertEquals(result.state, GOAL)
