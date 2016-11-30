# -*- coding: utf-8 -*-
import unittest
from simpleai.machine_learning.reinforcement_learning import boltzmann_exploration, make_at_least_n_times
from collections import Counter


class TestBoltzmann_exploration(unittest.TestCase):

    def setUp(self):
        self.actions = ['a', 'b', 'c']
        self.utilities = dict(zip(self.actions, [1, 2, 3]))

    def test_high_randomness_in_hot(self):
        counter = Counter()
        for i in range(100):
            a = boltzmann_exploration(self.actions, self.utilities, 10000000, None)
            counter[a] += 1
        for a, c in list(counter.items()):
            self.assertTrue(20 <= c <= 45)

    def test_low_randomness_in_cold(self):
        counter = Counter()
        for i in range(100):
            a = boltzmann_exploration(self.actions, self.utilities, 0.005, None)
            counter[a] += 1
        self.assertGreater(counter['c'], 95)

    def test_all_equals_utilities(self):
        self.utilities = dict(zip(self.actions, [0, 0, 0]))
        counter = Counter()
        for i in range(100):
            a = boltzmann_exploration(self.actions, self.utilities, 10000000, None)
            counter[a] += 1
        for a, c in list(counter.items()):
            self.assertTrue(25 <= c <= 40)


class Testat_least_n_times_exploration(unittest.TestCase):

    def setUp(self):
        self.actions = ['a', 'b', 'c']
        self.utilities = dict(zip(self.actions, [1, 2, 3]))
        self.function = make_at_least_n_times(100, 5)

    def test_selection_with_lower_n(self):
        c = Counter()
        c['a'] = 4
        c['b'] = 6
        c['c'] = 5
        action = self.function(self.actions, self.utilities, 0, c)
        self.assertEqual(action, 'a')

    def test_selection_with_higher_n(self):
        c = Counter()
        c['a'] = 5
        c['b'] = 6
        c['c'] = 5
        action = self.function(self.actions, self.utilities, 0, c)
        self.assertEqual(action, 'c')