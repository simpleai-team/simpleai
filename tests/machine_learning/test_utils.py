# -*- coding: utf-8 -*-
import unittest
from simpleai.machine_learning.utils import argmax


class TestArgMax(unittest.TestCase):
    def setUp(self):
        self.d = {'a': 3, 'b': 1, 'c': 3}

    def test_return_max(self):
        self.assertEquals('a', argmax(['a', 'b'], lambda x: self.d[x]))

    def test_random_tie(self):
        a = 0
        for x in range(100):
            if argmax(['a', 'b', 'c'], lambda x: self.d[x]) == 'a':
                a += 1
        self.assertTrue(25 < a < 75)

    def test_empty_sequence(self):
        self.assertRaises(ValueError, argmax, [], lambda x: x)