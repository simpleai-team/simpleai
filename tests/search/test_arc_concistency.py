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
    def ac3(self, domain_x, domain_y):
        domains = {'x': domain_x, 'y': domain_y}
        constraints = [(('x', 'y'), is_square)]

        return arc_consistency_3(domains, constraints), domains

    def test_values_available_for_all_returns_true(self):
        result, domains = self.ac3([1, 2, 3], [1, 4, 9])
        self.assertTrue(result)

    def test_if_variable_has_no_domain_left_returns_false(self):
        result, domains = self.ac3([1, 2, 3], [2, 3, 6])
        self.assertFalse(result)

    def test_chained_revise_calls_remove_non_obvious_problems(self):
        # if x, y, z must be all different, with domains [1], [2], [2] you
        # can't find a solution, but it requires several chained calls to
        # revise:
        # revise(x, y) -> ok!                      [1] [2] [2]
        # revise(x, z) -> ok!                      [1] [2] [2]
        # revise(y, z) -> fail, remove 2 from y    [1] [] [2]
        #    and re-revise x, y ...
        # revise(x, y) -> fail, remove 1 from x    [] [] [2]
        #    and re-revise ...
        # at the end, there are no possible values in any domain [] [] []

        domains = {'x': [1,],
                   'y': [2,],
                   'z': [2,]}
        different = lambda variables, values: len(set(values)) == len(variables)
        constraints = [(('x', 'y'), different),
                       (('x', 'z'), different),
                       (('y', 'z'), different)]

        result = arc_consistency_3(domains, constraints)

        self.assertFalse(result)
        self.assertEquals(domains['x'], [])
        self.assertEquals(domains['y'], [])
        self.assertEquals(domains['z'], [])
