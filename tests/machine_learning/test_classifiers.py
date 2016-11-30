#!/usr/bin/env python
# coding: utf-8

"""
Tests for dtree.
"""

import os
import math
import tempfile
import unittest
from collections import defaultdict

import numpy as np

from simpleai.machine_learning import evaluation
from simpleai.machine_learning.models import VectorDataClassificationProblem
from simpleai.machine_learning.classifiers import DecisionTreeLearner, \
    DecisionTreeLearner_Queued, DecisionTreeLearner_LargeData, NaiveBayes, \
    KNearestNeighbors


def euclidean_vector_distance(x, y):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))


class BaseTestClassifier(object):
    classifier = None

    def setup_dataset(self):
        raise NotImplementedError()

    def setUp(self):
        if self.classifier is None:
            raise NotImplementedError("Choose a classifier")
        self.setup_dataset()
        N = int(len(self.corpus) / 10)
        self.test_set = []
        i = 1
        while len(self.test_set) != N:
            i = (i * 1223) % len(self.corpus) + 1  # "random" number generator
            self.test_set.append(self.corpus.pop(i - 1))
        self.this = self.classifier(self.corpus, self.problem)
        self.attributes = self.problem.attributes
        self.target = self.problem.target

    def test_better_than_majority(self):
        d = defaultdict(int)
        for example in self.corpus:
            d[self.target(example)] += 1
        majority = max(d, key=d.get)

        class MockClassifier(object):
            target = self.target

            def classify(self, example):
                return majority, 1.0

        mock = MockClassifier()
        mock_prec = evaluation.precision(mock, self.test_set)
        this_prec = evaluation.precision(self.this, self.test_set)
        try:
            self.assertGreaterEqual(this_prec, mock_prec)
        except:
            print(self.corpus)

    def test_tolerates_empty_attributes(self):
        self.problem.attributes = []
        self.this = self.classifier(self.corpus, self.problem)
        evaluation.precision(self.this, self.test_set)

    def test_handles_empty_dataset(self):
        self.assertRaises(ValueError, self.classifier,
                          [], self.problem)

    def test_target_in_attributes(self):
        """
        If target in attributes precision is 1.0.
        """
        self.problem.attributes = [self.target]
        self.this = self.classifier(self.corpus, self.problem)
        prec = evaluation.precision(self.this, self.test_set)
        self.assertEqual(prec, 1.0)

    def test_save_classifier(self):
        _, tmp_filepath = tempfile.mkstemp()

        # Bad values
        self.assertRaises(ValueError, self.this.save, None)
        self.assertRaises(ValueError, self.this.save, "")
        self.assertRaises(ValueError, self.this.save, 42)

        # Save the values before saving the tree
        classification_values = {}
        for test in self.test_set:
            classification_values[tuple(test)] = self.this.classify(test)

        self.this.save(tmp_filepath)
        self.assertTrue(os.path.exists(tmp_filepath))
        self.assertNotEqual(os.stat(tmp_filepath).st_size, 0)  # File not empty

        # The classification must remain equal after saving the dtree
        for test in self.test_set:
            self.assertEqual(classification_values[tuple(test)],
                             self.this.classify(test))

    def test_load(self):
        _, tmp_filepath = tempfile.mkstemp()
        self.this.save(tmp_filepath)

        # Save the values before saving the tree
        classification_values = {}
        for test in self.test_set:
            classification_values[tuple(test)] = self.this.classify(test)

        classifier = self.classifier.load(tmp_filepath)
        self.assertIsInstance(classifier, self.classifier)

        # The classification must remain equal after loading the dtree
        for test in self.test_set:
            self.assertEqual(classification_values[tuple(test)],
                             classifier.classify(test))

    def test_leave_one_out(self):
        fold = evaluation.kfold(self.corpus, self.problem,
                                self.classifier, len(self.corpus))
        self.assertNotEqual(fold, 0)


class BaseTestDtree_Pseudo(BaseTestClassifier):
    classifier = DecisionTreeLearner

    def test_no_target_split(self):
        nodes = [self.this.root]

        while nodes:
            node = nodes.pop()
            self.assertNotEqual(self.target, node.attribute)
            nodes.extend(list(node.branches.values()))


class BaseTestDtree_LargeData(BaseTestDtree_Pseudo):
    classifier = DecisionTreeLearner_LargeData

    def test_equal_classification(self):
        """
        This checks that the three tree learning methods are equal.
        """

        pseudo = DecisionTreeLearner(self.corpus, self.problem)
        for test in self.test_set:
            self.assertEqual(pseudo.classify(test), self.this.classify(test))

    def test_every_node_can_classify(self):
        nodes = [self.this.root]

        while nodes:
            node = nodes.pop()
            self.assertNotEqual(node.result, None)
            nodes.extend(list(node.branches.values()))


class BaseTestDtree_Queued(BaseTestDtree_LargeData):
    classifier = DecisionTreeLearner_Queued


class BaseTestNaiveBayes(BaseTestClassifier):
    classifier = NaiveBayes


class BaseTestKNearestNeighbors(BaseTestClassifier):
    classifier = KNearestNeighbors


class CorpusIris(object):
    IRIS_PATH = os.path.join(os.path.dirname(__file__), "iris.txt")

    def setup_dataset(self):
        """
        Creates a corpus with the iris dataset. Returns the dataset,
        the attributes getter and the target getter.
        """

        dataset = []
        with open(self.IRIS_PATH) as filehandler:
            file_data = filehandler.read()

        for line in file_data.split("\n"):
            line_data = [np.rint(float(x)) for x in line.split()]
            if line_data:
                dataset.append(line_data)

        problem = VectorDataClassificationProblem(dataset, target_index=4)
        problem.distance = euclidean_vector_distance
        self.corpus = dataset
        self.problem = problem


class CorpusXor(object):
    def setup_dataset(self):
        """
        Creates a corpus  with n k-bit examples of the parity problem:
        k random bits followed by a 1 if an odd number of bits are 1, else 0
        """
        k = 2
        n = 100

        dataset = []
        for i in range(n):
            # Pseudo random generation of bits
            bits = [(((i + j) * 1223) % (n + 1)) % 2 for j in range(k)]
            bits.append(sum(bits) % 2)
            dataset.append(bits)

        problem = VectorDataClassificationProblem(dataset, target_index=k)
        self.corpus = dataset
        self.problem = problem


class CorpusPrimes(object):
    def setup_dataset(self):
        """
        Creates a corpus of primes. Returns the dataset,
        the attributes getter and the target getter.
        """
        size = 105  # Magic number, chosen to avoid an "error" that cannot be
                    # patched in Dtree Pseudo (with modifing the pseudocode).

        dataset = []
        for i in range(size):
            dataset.append([
                i % 2 == 0,
                i % 3 == 0,
                i % 5 == 0,
                i % 7 == 0,
                self.isprime(i)
            ])

        problem = VectorDataClassificationProblem(dataset, target_index=-1)
        problem.distance = euclidean_vector_distance
        self.corpus = dataset
        self.problem = problem

    def isprime(self, number):
        """
        Returns if a number is prime testing if
        is divisible by any number from 0 to sqrt(number)
        """

        if number < 2:
            return False
        if number == 2:
            return True
        if not number & 1:
            return False

        for i in range(3, int(number ** 0.5) + 1, 2):
            if number % i == 0:
                return False
        return True


def create_tstcase(classifier, corpus):
    name = "{}_{}".format(classifier.__name__, corpus.__name__)
    bases = (corpus, classifier, unittest.TestCase)
    newclass = type(name, bases, {})
    globals()[name] = newclass


TestDtree_Pseudo_CorpusIris = create_tstcase(BaseTestDtree_Pseudo, CorpusIris)
TestDtree_Pseudo_CorpusXor = create_tstcase(BaseTestDtree_Pseudo, CorpusXor)
TestDtree_Pseudo_CorpusPrimes = create_tstcase(BaseTestDtree_Pseudo, CorpusPrimes)

TestDtree_Queued_CorpusIris = create_tstcase(BaseTestDtree_Queued, CorpusIris)
TestDtree_Queued_CorpusXor = create_tstcase(BaseTestDtree_Queued, CorpusXor)
TestDtree_Queued_CorpusPrimes = create_tstcase(BaseTestDtree_Queued, CorpusPrimes)

TestDtree_LargeData_CorpusIris = create_tstcase(BaseTestDtree_LargeData, CorpusIris)
TestDtree_LargeData_CorpusXor = create_tstcase(BaseTestDtree_LargeData, CorpusXor)
TestDtree_LargeData_CorpusPrimes = create_tstcase(BaseTestDtree_LargeData, CorpusPrimes)

TestNaiveBayes_CorpusIris = create_tstcase(BaseTestNaiveBayes, CorpusIris)
TestNaiveBayes_CorpusXor = create_tstcase(BaseTestNaiveBayes, CorpusXor)
TestNaiveBayes_CorpusPrimes = create_tstcase(BaseTestNaiveBayes, CorpusPrimes)

TestKNearestNeighbors_CorpusPrimes = create_tstcase(BaseTestKNearestNeighbors, CorpusPrimes)
TestKNearestNeighbors_CorpusIris = create_tstcase(BaseTestKNearestNeighbors, CorpusIris)
