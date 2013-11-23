# coding=utf-8
import unittest

from operator import itemgetter

from simpleai.search.arc import all_arcs, revise, arc_consistency_3

first = itemgetter(0)


class TestAllArcs(unittest.TestCase):

    def setUp(self):
        self.constraint = lambda variables, values: False

    def test_adds_pairs_in_both_directions(self):
        constraints = [(('A', 'B'), self.constraint)]

        arcs_result = all_arcs(constraints)
        arcs_expected = set([('A', 'B'),
                             ('B', 'A')])

        self.assertEqual(arcs_result, arcs_expected)

    def test_constraints_with_more_than_2_neighbors_arent_added(self):
        constraints = [(('A', 'B', 'C'), self.constraint)]

        arcs_result = all_arcs(constraints)
        arcs_expected = set()

        self.assertEqual(arcs_result, arcs_expected)


def is_square(variables, values):
    return values[0] ** 2 == values[1]


class TestReviseDomain(unittest.TestCase):
    def revise(self, domain_x, domain_y, duplicate_constraints=False):
        domains = {'x': domain_x, 'y': domain_y}
        constraints = [(('x', 'y'), is_square)]
        if duplicate_constraints:
            constraints = constraints * 2

        return revise(domains, ('x', 'y'), constraints), domains

    def test_if_all_values_have_possible_match_the_domain_is_untouched(self):
        result, domains = self.revise([1, 2, 3], [1, 4, 9])
        self.assertFalse(result)
        self.assertEquals(domains['x'], [1, 2, 3])

    def test_if_a_value_has_no_possible_match_remove_it_from_domain(self):
        result, domains = self.revise([1, 2, 3], [1, 4])
        self.assertTrue(result)
        self.assertEquals(domains['x'], [1, 2])

    def test_if_multiple_constraints_dont_fail_removing_twice(self):
        # there was a bug when two constraints tried to remove the same value
        result, domains = self.revise([1, 2, 3], [1, 4], True)
        self.assertTrue(result)
        self.assertEquals(domains['x'], [1, 2])


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
