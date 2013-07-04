# -*- coding: utf-8 -*-

import unittest
from simpleai.machine_learning.evaluation import precision, kfold
from simpleai.machine_learning import VectorDataClassificationProblem, \
                                      Classifier


class MockClassifier(Classifier):
    """
    Classifies everything as the first item in the dataset.
    """
    def learn(self):
        pass

    def classify(self, x):
        return self.target(self.dataset[0]), 1.0


class TestPrecision(unittest.TestCase):
    train = [(0, 1, 1), (1, 1, 0), (0, 1, 0), (1, 7, 0), (0, 1, 9)]

    def setUp(self):
        self.p = VectorDataClassificationProblem(self.train, 0)
        self.c = MockClassifier(self.train, self.p)

    def test_is_1(self):
        test = [(0, 3, 3), (0, 2, 2)]
        p = precision(self.c, test)
        self.assertEqual(p, 1.0)

    def test_is_0(self):
        test = [(1, 3, 3), (1, 2, 2)]
        p = precision(self.c, test)
        self.assertEqual(p, 0.0)

    def test_bad_testset(self):
        test = []
        with self.assertRaises(ValueError):
            precision(self.c, test)


class TestKfold(unittest.TestCase):

    def my_setup(self, train):
        self.p = VectorDataClassificationProblem(train, 0)
        self.c = MockClassifier(train, self.p)

    def test_k1_is_bad(self):
        testset = [(0, 1, 1), (1, 1, 0), (1, 6, 5), (1, 7, 0), (0, 1, 9)]
        self.my_setup(testset)
        with self.assertRaises(ValueError):
            kfold(testset, self.p, MockClassifier, k=1)

    def test_kfold_is_0(self):
        testset = [(0, 1, 1), (1, 1, 0)]
        self.my_setup(testset)
        p = kfold(testset, self.p, MockClassifier, k=2)
        self.assertEqual(p, 0.0)

    def test_kfold_lt_75(self):
        testset = [(1, 0, 0), (1, 0, 1), (1, 1, 0), (0, 1, 1)]
        self.my_setup(testset)
        p = kfold(testset, self.p, MockClassifier, k=4)
        self.assertLessEqual(p, 0.75)
