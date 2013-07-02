# coding=utf-8
import unittest

from copy import copy

from simpleai.search.arc import neighbors, all_arcs, revise


class TestNeighborsAndArcs(unittest.TestCase):

    def setUp(self):
        self.constraints = [(('A1', 'B2'), None),
                            (('A1', 'C2'), None),
                            (('D2', 'A1'), None),
                            (('D2', 'C1'), None),
                            (('E2', 'A1'), None)]

    def test_neighbors(self):
        variables = neighbors('A1', self.constraints, 'B2')
        self.assertEqual(set(variables), set(['C2', 'D2', 'E2']))

    def test_all_arcs(self):
        variables = list(all_arcs(self.constraints))
        arcs = [(('A1', 'B2'), None),
                (('B2', 'A1'), None),
                (('A1', 'C2'), None),
                (('C2', 'A1'), None),
                (('D2', 'A1'), None),
                (('A1', 'D2'), None),
                (('D2', 'C1'), None),
                (('C1', 'D2'), None),
                (('E2', 'A1'), None),
                (('A1', 'E2'), None)]
        self.assertEqual(variables, arcs)


class TestReviseDomain(unittest.TestCase):

    def set_domains(self):
        self.domains = {'X': [1, 2, 3, 4, 5],
                        'Y': [1, 4, 9, 16, 20]}

    def setUp(self):
        self.set_domains()
        self.constraint = (
            lambda vars_, values:
            values[0] ** 2 == values[1])

    def tearDown(self):
        self.set_domains()

    def test_revise_X(self):
        self.assertTrue(revise(self.domains, ('X', 'Y'), self.constraint))
        self.assertEqual(self.domains['X'], [1, 2, 3, 4])
        self.assertEqual(self.domains['Y'], [1, 4, 9, 16, 20])

    def test_revise_Y(self):
        self.constraint = (
            lambda vars_, values:
            values[1] ** 2 == values[0])

        self.assertTrue(revise(self.domains, ('Y', 'X'), self.constraint))
        self.assertEqual(self.domains['X'], [1, 2, 3, 4, 5])
        self.assertEqual(self.domains['Y'], [1, 4, 9, 16])
