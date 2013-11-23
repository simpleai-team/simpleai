# coding=utf-8
import unittest

from operator import itemgetter

from simpleai.search.arc import all_arcs, revise, arc_consistency_3

first = itemgetter(0)


class TestAllArcs(unittest.TestCase):

    def setUp(self):
        constraint = lambda variables, values: False
        self.constraints = [(('A', 'B'), constraint),
                            (('A', 'C'), constraint),
                            (('C', 'A'), constraint),
                            (('B', 'C'), constraint)]

    def test_all_arcs(self):
        # does not check that the constraint function is well created
        arcs_result = all_arcs(self.constraints)
        arcs_expected = [('A', 'B'),
                         ('B', 'A'),
                         ('A', 'C'),
                         ('C', 'A'),
                         ('B', 'C'),
                         ('C', 'B')]
        self.assertEqual(arcs_result, arcs_expected)


class TestReviseDomain(unittest.TestCase):

    def set_domains(self):
        self.domains = {'X': [1, 2, 3, 4, 5],
                        'Y': [1, 4, 9, 16, 20]}

    def setUp(self):
        self.set_domains()
        const = lambda variables, values: values[0] ** 2 == values[1]
        self.constraint = constraint_wrapper(('X', 'Y'), const)

    def tearDown(self):
        self.set_domains()

    def test_revise_X(self):
        self.assertTrue(revise(self.domains, ('X', 'Y'), self.constraint))
        self.assertEqual(self.domains['X'], [1, 2, 3, 4])
        self.assertEqual(self.domains['Y'], [1, 4, 9, 16, 20])

    def test_revise_Y(self):
        self.assertTrue(revise(self.domains, ('Y', 'X'), self.constraint))
        self.assertEqual(self.domains['X'], [1, 2, 3, 4, 5])
        self.assertEqual(self.domains['Y'], [1, 4, 9, 16])


class TestAC3(unittest.TestCase):

    def set_domains(self):
        self.domains = {'X': [1, 2, 3, 4, 5],
                        'Y': [1, 4, 9, 16, 20]}

    def set_constraints(self):
        self.constraints = [(('X', 'Y'), lambda variables, values: values[0] ** 2 == values[1])]

    def setUp(self):
        self.set_domains()
        self.set_constraints()

    def test_ac3(self):
        self.assertTrue(arc_consistency_3(self.domains, self.constraints))
        self.assertEqual(self.domains, {'X': [1, 2, 3, 4], 'Y': [1, 4, 9, 16]})
