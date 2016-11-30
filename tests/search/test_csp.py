# coding=utf-8
import unittest
from simpleai.search.models import CspProblem
from simpleai.search.csp import (_find_conflicts, _count_conflicts,
                                 _most_constrained_variable_chooser,
                                 _highest_degree_variable_chooser,
                                 _least_constraining_values_sorter,
                                 _min_conflicts_value, backtrack,
                                 min_conflicts)


class TestCsp(unittest.TestCase):
    def setUp(self):
        self.variables = ('A', 'B', 'C')

        self.domains = {
            'A': [1, 2, 3],
            'B': [1, 3, 4],
            'C': [1, 2],
        }

        # a constraint that expects different variables to have different values
        def const_different(variables, values):
            return len(values) == len(set(values))  # remove repeated values and count

        # a constraint that expects one variable to be bigger than other
        def const_one_bigger_other(variables, values):
            return values[0] > values[1]

        # a constraint thet expects two variables to be one odd and the other even,
        # no matter which one is which type
        def const_one_odd_one_even(variables, values):
            if values[0] % 2 == 0:
                return values[1] % 2 == 1  # first even, expect second to be odd
            else:
                return values[1] % 2 == 0  # first odd, expect second to be even

        # a constraint that requires one variable to be different than 1
        def const_not_1(variables, values):
            return values[0] != 1

        self.constraints = [
            (('A', 'B', 'C'), const_different),
            (('A', 'C'), const_one_bigger_other),
            (('A', 'C'), const_one_odd_one_even),
            (('A',), const_not_1)
        ]

        self.problem = CspProblem(self.variables, self.domains, self.constraints)

    def test_most_constrained_variable_chooser(self):
        variable = _most_constrained_variable_chooser(self.problem, self.variables, self.domains)
        self.assertEqual(variable, 'C')

    def test_highest_degree_variable_chooser(self):
        variable = _highest_degree_variable_chooser(self.problem, self.variables, self.domains)
        self.assertEqual(variable, 'A')

    def test_find_conflicts(self):
        assignment = {'A': 1, 'B': 1, 'C': 3}
        conflicts = _find_conflicts(self.problem, assignment)
        self.assertEqual(conflicts, self.constraints)

    def test_find_conflicts_with_added_variable(self):
        assignment = {'A': 1, 'B': 1}
        conflicts = _find_conflicts(self.problem, assignment, 'C', 3)
        self.assertEqual(conflicts, self.constraints)

    def test_count_conflicts(self):
        assignment = {'A': 1, 'B': 1, 'C': 3}
        conflicts_count = _count_conflicts(self.problem, assignment)
        self.assertEqual(conflicts_count, 4)

    def test_count_conflicts_with_added_variable(self):
        assignment = {'A': 1, 'B': 1}
        conflicts_count = _count_conflicts(self.problem, assignment, 'C', 3)
        self.assertEqual(conflicts_count, 4)

    def test_least_constraining_values_sorter(self):
        assignment = {'A': 1, 'B': 1}
        values = _least_constraining_values_sorter(self.problem, assignment, 'C', self.domains)
        self.assertEqual(values, [2, 1])

    def test_min_conflicts_value(self):
        assignment = {'A': 1, 'B': 1}
        value = _min_conflicts_value(self.problem, assignment, 'C')
        self.assertEqual(value, 2)

    def test_backtrack(self):
        result = backtrack(self.problem)
        self.assertEqual(result, {'A': 2, 'B': 3, 'C': 1})

    def test_min_conflicts(self):
        result = min_conflicts(self.problem)
        c = _count_conflicts(self.problem, result)
        self.assertEqual(c, 0)
