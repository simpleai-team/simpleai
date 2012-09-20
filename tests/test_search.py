# coding=utf-8
import unittest
from simpleai.tests.dummies import DummyProblem, GOAL
from simpleai.search import (breadth_first, depth_first, limited_depth_first,
                             iterative_limited_depth_first, uniform_cost,
                             greedy, astar)


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.problem = DummyProblem()
        self.problem.initial_state = 'i'

    def test_breadth_first(self):
        result = breadth_first(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_depth_first(self):
        result = depth_first(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_limited_depth_first(self):
        result = limited_depth_first(self.problem, depth_limit=3)
        self.assertEquals(result, None)

        result = limited_depth_first(self.problem, depth_limit=6)
        self.assertEquals(result.state, GOAL)

    def test_iterative_limited_depth_first(self):
        result = iterative_limited_depth_first(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_uniform_cost(self):
        result = uniform_cost(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_greedy(self):
        result = greedy(self.problem)
        self.assertEquals(result.state, GOAL)

    def test_astar(self):
        result = astar(self.problem)
        self.assertEquals(result.state, GOAL)

