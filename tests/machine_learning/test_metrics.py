#!/usr/bin/env python
# coding: utf-8

"""
Tests for metrics module in machine learning.
"""

import unittest
from simpleai.machine_learning.metrics import Counter, OnlineEntropy, \
                                              OnlineLogProbability, \
                                              OnlineInformationGain


class TestCounter(unittest.TestCase):
    def test_total_starts_in_zero(self):
        counter = Counter(lambda x: None)
        self.assertEqual(counter.total, 0)

    def test_add_elements(self):
        counter = Counter(lambda x: None)
        for i in range(20):
            counter.add("something")
        self.assertEqual(counter.total, 20)

    def test_target_values(self):
        counter = Counter(lambda x: x % 2 == 0)
        for i in range(25):
            counter.add(i)
        self.assertEqual(counter[0], 12)
        self.assertEqual(counter[1], 13)

        counter = Counter(lambda x: None)
        for i in range(50):
            counter.add(i)
        self.assertEqual(counter[None], 50)


class TestOnlineEntropy(unittest.TestCase):
    def test_starts_in_zero(self):
        entropy = OnlineEntropy(lambda x: None)
        self.assertEqual(entropy.get_entropy(), 0)

    def test_valid_values(self):
        entropy = OnlineEntropy(lambda x: x % 10)
        for i in range(150):
            entropy.add(i)
        self.assertGreaterEqual(entropy.get_entropy(), 0.0)


class TestOnlineInformationGain(unittest.TestCase):
    def test_starts_in_zero(self):
        gain = OnlineInformationGain(lambda x: None, lambda x: None)
        self.assertEqual(gain.get_gain(), 0)
        self.assertEqual(list(gain.get_target_class_counts().items()), [])
        self.assertEqual(gain.get_branches(), [])

    def test_no_gain(self):
        f = lambda x: None
        gain = OnlineInformationGain(f, f)
        for i in range(30):
            gain.add(i)
        self.assertEqual(gain.get_gain(), 0)

    def test_full_gain(self):
        target = lambda x: x % 7
        gain = OnlineInformationGain(target, target)
        entropy = OnlineEntropy(target)
        for i in range(50):
            gain.add(i)
            entropy.add(i)
        self.assertEqual(gain.get_gain(), entropy.get_entropy())
        self.assertGreaterEqual(gain.get_gain(), 0)
