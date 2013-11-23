# coding=utf-8
import unittest

from operator import itemgetter

from simpleai.search.arc import constraint_wrapper, neighbors, all_arcs, revise, arc_consistency_3

first = itemgetter(0)


class TestNeighborsAndArcs(unittest.TestCase):

    def setUp(self):
        unit = self.unit = lambda vars_, values: False
        self.constraints = [(('A1', 'B2'), unit),
                            (('A1', 'C2'), unit),
                            (('D2', 'A1'), unit),
                            (('D2', 'C1'), unit),
                            (('E2', 'A1'), unit)]

    def test_neighbors(self):
        variables = map(lambda t: first(first(t)), neighbors('A1', self.constraints, 'B2'))
        self.assertEqual(set(variables), set(['C2', 'D2', 'E2']))

    def test_all_arcs(self):
        # does not check that the constraint function is well created
        variables = map(first, list(all_arcs(self.constraints)))
        arcs = [('A1', 'B2'),
                ('B2', 'A1'),
                ('A1', 'C2'),
                ('C2', 'A1'),
                ('D2', 'A1'),
                ('A1', 'D2'),
                ('D2', 'C1'),
                ('C1', 'D2'),
                ('E2', 'A1'),
                ('A1', 'E2')]
        self.assertEqual(variables, arcs)

    def test_constraint_wrapper(self):
        constraint = (('X', 'Y'), lambda vars_, values: values[0] ** 2 == values[1])
        wrapped = constraint_wrapper(*constraint)
        self.assertTrue(wrapped(('Y', 'X'), (25, 5)))

    def test_constraint_wrapper_raises_error(self):
        constraint = (('X', 'Y'), lambda vars_, values: values[0] ** 2 == values[1])
        wrapped = constraint_wrapper(*constraint)
        self.assertRaises(ValueError, wrapped, ('Y', 'Z'), (25, 5))


class TestReviseDomain(unittest.TestCase):

    def set_domains(self):
        self.domains = {'X': [1, 2, 3, 4, 5],
                        'Y': [1, 4, 9, 16, 20]}

    def setUp(self):
        self.set_domains()
        const = lambda vars_, values: values[0] ** 2 == values[1]
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
        self.constraints = [(('X', 'Y'), lambda vars_, values: values[0] ** 2 == values[1])]

    def setUp(self):
        self.set_domains()
        self.set_constraints()

    def test_ac3(self):
        self.assertTrue(arc_consistency_3(self.domains, self.constraints))
        self.assertEqual(self.domains, {'X': [1, 2, 3, 4], 'Y': [1, 4, 9, 16]})
