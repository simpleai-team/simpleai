#!/usr/bin/env python
# coding: utf-8

"""
Tools for evaluate the classification algorithms
"""


def precision(classifier, target, testset):
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
        if classifier.classify(example)[0] == target(example):
            hit += 1
        total += 1
    if total == 0:
        raise ValueError("Empty testset!")
    return hit / float(total)


def kfold(dataset, problem, method, k=10):
    """
    Does a k-fold on `dataset` with `method`.
    This is, creates k-partitions of the dataset, and k-times
    trains the method with k-1 parts and runs it with the partition left.
    After all this, returns the overall success ratio.
    """

    trials = 0
    positive = 0
    div = len(dataset) / k

    for i in xrange(k):
        partition_start = div * i
        partition_end = div * (i + 1)
        to_test = dataset[partition_start:partition_end]
        corpus = dataset[:partition_start - 1] + \
                 dataset[partition_end:]

        tree = method(corpus, problem)

        for row in to_test:
            trials += 1
            if tree.classify(row)[0] == problem.target(row):
                positive += 1

    return float(positive) / float(trials)
