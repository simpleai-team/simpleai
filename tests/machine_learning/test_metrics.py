#!/usr/bin/env python
# coding: utf-8

"""
Tests for metrics module in machine learning.
"""

import unittest
from simpleai.machine_learning.metrics import Counter, OnlineEntropy, \
                                              OnlineLogProbability


class TestCounter(unittest.TestCase):
    def test_total_starts_in_zero(self):
        counter = Counter(lambda x: None)
        self.assertEqual(counter.total, 0)

    def test_add_elements(self):
        counter = Counter(lambda x: None)
        for i in xrange(20):
            counter.add("something")
        self.assertEqual(counter.total, 20)

    def test_target_values(self):
        counter = Counter(lambda x: x % 2 == 0)
        for i in xrange(25):
            counter.add(i)
        self.assertEqual(counter[0], 12)
        self.assertEqual(counter[1], 13)

        counter = Counter(lambda x: None)
        for i in xrange(50):
            counter.add(i)
        self.assertEqual(counter[None], 50)


class TestOnlineEntropy(unittest.TestCase):
    def test_starts_in_zero(self):
        entropy = OnlineEntropy(lambda x: None)
        self.assertEqual(entropy.get_entropy(), 0)

    def test_valid_values(self):
        entropy = OnlineEntropy(lambda x: x % 10)
        for i in xrange(150):
            entropy.add(i)
        self.assertGreaterEqual(entropy.get_entropy(), 0.0)


if __name__ == "__main__":
    unittest.main()
