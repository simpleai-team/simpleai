# coding=utf-8
import unittest
from tests.search.dummies import DummyProblem
from simpleai.search.models import (SearchNode, SearchNodeCostOrdered,
                                    SearchNodeValueOrdered,
                                    SearchNodeHeuristicOrdered,
                                    SearchNodeStarOrdered)


class TestSearchNode(unittest.TestCase):
    def setUp(self):
        self.problem = DummyProblem()
        self.node = SearchNode(state='i',
                               problem=self.problem)
        self.childs = self.node.expand()

    def test_expand_creates_node_for_each_action(self):
        self.assertEqual(len(self.childs), 3)

    def test_successors_have_correct_values(self):
        child = self.childs[0]
        self.assertEqual(child.state, 'ia')
        self.assertIs(child.parent, self.node)
        self.assertEqual(child.action, 'a')
        self.assertEqual(child.cost, 1)
        self.assertIs(child.problem, self.problem)
        self.assertEqual(child.depth, 1)

    def test_successors_dont_have_parent_when_local_search(self):
        childs = self.node.expand(local_search=True)
        self.assertEqual(childs[0].parent, None)

    def test_path(self):
        n1 = SearchNode(problem=self.problem, state='i')
        n2 = SearchNode(action='a', state='ia', parent=n1)
        n3 = SearchNode(action='b', state='iab', parent=n2)

        path = [(None, 'i'), ('a', 'ia'), ('b', 'iab')]

        self.assertEqual(n3.path(), path)

    def test_equals(self):
        n1 = SearchNode(problem=self.problem, state='i')
        n2 = SearchNode(problem=self.problem, state='i')
        n3 = SearchNode(problem=self.problem, state='i', action='a')
        n4 = SearchNode(problem=self.problem, state='ia')

        self.assertTrue(n1 == n2)
        self.assertTrue(n1 == n3)
        self.assertFalse(n1 == n4)


class TestOrderedSearchNodeClasses(unittest.TestCase):
    def setUp(self):
        self.problem = DummyProblem()

    def test_search_node_cost_sorted(self):
        n1 = SearchNodeCostOrdered(problem=self.problem, state='i', cost=1)
        n2 = SearchNodeCostOrdered(problem=self.problem, state='i', cost=2)

        self.assertTrue(n1 < n2)
        self.assertFalse(n2 < n1)

    def test_search_node_value_sorted(self):
        n1 = SearchNodeValueOrdered(problem=self.problem, state='iab')
        n2 = SearchNodeValueOrdered(problem=self.problem, state='iba')

        self.assertTrue(n1 < n2)
        self.assertFalse(n2 < n1)

    def test_search_node_heuristic_sorted(self):
        n1 = SearchNodeHeuristicOrdered(problem=self.problem, state='iab')
        n2 = SearchNodeHeuristicOrdered(problem=self.problem, state='iba')

        self.assertTrue(n1 < n2)
        self.assertFalse(n2 < n1)

    def test_search_node_star_sorted(self):
        n1 = SearchNodeStarOrdered(problem=self.problem, state='iab', cost=1)
        n2 = SearchNodeStarOrdered(problem=self.problem, state='iba', cost=2)

        self.assertTrue(n1 < n2)
        self.assertFalse(n2 < n1)

