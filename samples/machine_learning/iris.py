#!/usr/bin/env python
# coding: utf-8

"""
Iris dataset classification example.

The iris dataset can be downloaded
from here: http://archive.ics.uci.edu/ml/datasets/Iris
It has to be placed in the corpus folder.
"""

from __future__ import print_function

import os
import math
import random
from simpleai.machine_learning import precision
from simpleai.machine_learning import NaiveBayes
from simpleai.machine_learning import KNearestNeighbors
from simpleai.machine_learning import DecisionTreeLearner_Queued
from simpleai.machine_learning import VectorDataClassificationProblem

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
IRIS_PATH = os.path.join(BASE_PATH, "corpus", "iris.data")


def euclidean_vector_distance(x, y):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))


class IrisDataset(list):
    target_index = 4

    def __init__(self, filepath, accept_criteria):
        i = 0
        for line in open(filepath):
            i += 1

            if not accept_criteria(i):
                continue

            line = line[:-1]
            if not line:
                continue
            attrs = line.split(",")
            target = attrs[self.target_index]
            attrs = [float(x) for x in attrs[:self.target_index]]
            self.append(attrs + [target])

        random.shuffle(self)


def main():
    # line count
    N = 0
    for _ in open(IRIS_PATH):
        N += 1
    testindexes = set(random.sample(range(N), N / 10))

    dataset = IrisDataset(IRIS_PATH, lambda i: i not in testindexes)
    testset = IrisDataset(IRIS_PATH, lambda i: i in testindexes)
    problem = VectorDataClassificationProblem(dataset, dataset.target_index)
    # Distance without target
    problem.distance = lambda x, y: euclidean_vector_distance(x[:-1], y[:-1])

    classifiers = {
        "K-Nearest Neighbours": KNearestNeighbors,
        "Naive Bayes": NaiveBayes,
        "Decision Tree": DecisionTreeLearner_Queued,
    }

    print("Precision:\n")
    for name, method in list(classifiers.items()):
        classifier = method(dataset, problem)
        p = precision(classifier, testset)
        print("{:>20} = {:.2}".format(name, p))


if __name__ == "__main__":
    main()
