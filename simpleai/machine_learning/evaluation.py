#!/usr/bin/env python
# coding: utf-8

"""
Tools for evaluate the classification algorithms
"""


import random


def precision(classifier, testset):
    """
    Runs the classifier for each example in `testset`
    and verifies that the classification is correct
    using the `target`.

    Returns a number between 0.0 and 1.0 with the
    precision of classification for this test set.
    """

    hit = 0
    total = 0
    for example in testset:
        if classifier.classify(example)[0] == classifier.target(example):
            hit += 1
        total += 1
    if total == 0:
        raise ValueError("Empty testset!")
    return hit / float(total)


def kfold(dataset, problem, method, k=10):
    """
    Does a k-fold on `dataset` with `method`.
    This is, it randomly creates k-partitions of the dataset, and k-times
    trains the method with k-1 parts and runs it with the partition left.
    After all this, returns the overall success ratio.
    """

    if k <= 1:
        raise ValueError("k argument must be at least 2")

    dataset = list(dataset)
    random.shuffle(dataset)

    trials = 0
    positive = 0
    for i in range(k):
        train = [x for j, x in enumerate(dataset) if j % k != i]
        test = [x for j, x in enumerate(dataset) if j % k == i]
        classifier = method(train, problem)
        for data in test:
            trials += 1
            result = classifier.classify(data)
            if result is not None and result[0] == problem.target(data):
                positive += 1

    return float(positive) / float(trials)
