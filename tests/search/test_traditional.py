# coding=utf-8
import unittest
from tests.search.dummies import DummyProblem, GOAL, DummyGraphProblem
from simpleai.search.traditional import (breadth_first, depth_first,
                                         limited_depth_first,
                                         iterative_limited_depth_first,
                                         uniform_cost, greedy, astar)


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.problem = DummyProblem()
        self.problem.initial_state = 'i'
        self.graph_problem = DummyGraphProblem()

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

    def test_astar_graph_execution_ok(self):
        result = astar(self.graph_problem, graph_search=True)
        self.assertEquals(result.state, self.graph_problem.goal)

