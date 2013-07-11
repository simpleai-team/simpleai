import unittest
from operator import itemgetter
from simpleai.search import convert_to_binary

fst = itemgetter(0)


class TestHiddenVariableRepr(unittest.TestCase):

    def setUp(self):
        alldiff = lambda vars_, values_: len(set(values_)) == len(values_)
        const = lambda vars_, values_: True

        self.variables = ('A', 'B', 'C')

        self.domains = {
            'A': [1, 2, 3],
            'B': [1, 3, 4],
            'C': [1, 2],
        }

        self.constraints = [
            (('A', 'B', 'C'), alldiff),
            (('A', 'C'), const),
            (('A', 'C'), const),
            (('A',), lambda _vars, _value: _value[0] % 2 == 0)
        ]

    def test_conver_to_binary_adds_variables(self):
        v, d, c = convert_to_binary(self.variables, self.domains, self.constraints)
        self.assertNotEqual(v, self.variables)
        self.assertIn('hidden0', v)
        self.assertIn('hidden1', v)

    def test_conver_to_binary_constraints_variables(self):
        v, d, c = convert_to_binary(self.variables, self.domains, self.constraints)
        var_tuples = map(fst, c)
        self.assertIn(('hidden0', 'A'), var_tuples)
        self.assertIn(('hidden0', 'B'), var_tuples)
        self.assertIn(('hidden0', 'C'), var_tuples)
        self.assertIn(('hidden1', 'A'), var_tuples)

    def test_hidden_variable__domains_is_constraint_by_the_constraint_on_the_variable_it_hides(self):
        v, d, c = convert_to_binary(self.variables, self.domains, self.constraints)
        # hidden0 hides A, B, C
        domain = sorted(d['hidden0'])
        self.assertEqual(domain, [(1, 3, 2), (1, 4, 2), (2, 3, 1), (2, 4, 1), (3, 1, 2), (3, 4, 1), (3, 4, 2)])

        domain = sorted(d['hidden1'])
        self.assertEqual(domain, [(2,)])
