#!/usr/bin/env python
# coding: utf-8

try:
    import cPickle as pickle
except ImportError:
    import pickle


class Classifier(object):
    """
    Base of all classifiers.
    This specifies the classifier API.

    Each classifier holds at least a dataset and a ClassificationProblem.
    """

    def __init__(self, dataset, problem):
        self.dataset = dataset
        self.problem = problem

    @property
    def attributes(self):
        return self.problem.attributes

    @property
    def target(self):
        return self.problem.target

    def classify(self, example):
        """
        Returns the classification for example.
        """
        raise NotImplementedError()

    def save(self, filepath):
        """
        Pickles the tree and saves it into `filepath`
        """

        if not filepath or not isinstance(filepath, basestring):
            raise ValueError("Invalid filepath")

        # Removes dataset so is not saved in the pickle
        self.dataset = None
        with open(filepath, "w") as filehandler:
            pickle.dump(self, filehandler)

    def distance(self, a, b):
        """
        Custom distance between `a` and `b`.
        """
        raise NotImplementedError()

    @classmethod
    def load(cls, filepath):
        with open(filepath) as filehandler:
            classifier = pickle.load(filehandler)

        if not isinstance(classifier, Classifier):
            raise ValueError("Pickled object is not a Classifier")

        return classifier


class ClassificationProblem(object):
    """
    Represents a problem to be solved with a classifier.
    It holds the attributes to be tested and the defines
    the target of an example.

    You can define attributes by adding them to the `attributes`
    list or by defining a method and decorating it with `is_attribute`.
    """

    def __init__(self):
        attrs = []
        for name in dir(self):
            method = getattr(self, name)
            if getattr(method, "is_attribute", False):
                attr = Attribute(method, method.name)
                attrs.append(attr)
        self.attributes = attrs

    def target(self, example):
        raise NotImplementedError()


class VectorDataClassificationProblem(ClassificationProblem):
    """
    A ClassificationProblem that defines attribute for a dataset
    that is a set of vectors.
    """

    def __init__(self, dataset, target_index):
        """
        Dataset should be an iterable, *not* an iterator
        """
        super(VectorDataClassificationProblem, self).__init__()
        try:
            example = next(iter(dataset))
        except StopIteration:
            raise ValueError("Dataset is empty")
        self.i = target_index
        N = len(example)
        if self.i < 0:
            self.i = N + self.i
        if self.i < 0 or N <= self.i:
            raise ValueError("Target index is out of range")
        for i in xrange(N):
            if i == self.i:
                continue
            attribute = VectorIndexAttribute(i, "data at index {}".format(i))
            self.attributes.append(attribute)

    def target(self, example):
        return example[self.i]


class Attribute(object):
    def __init__(self, function=None, name=None, description=None):
        self.name = name
        self.function = function
        self.description = description

    def reason(self, example):
        """
        Returns a string with an explanation of
        why the attribute is being applied.
        """
        raise NotImplementedError()

    def __call__(self, example):
        return self.function(example)

    def __str__(self):
        if self.name is None:
            return "<undefined name>"
        return self.name


class VectorIndexAttribute(Attribute):
    """
    Attribute that returns the i-th element from a vector.
    """

    def __init__(self, i, name=None, description=None):
        super(VectorIndexAttribute, self).__init__(self, name, description)
        self.i = i

    def __call__(self, vector):
        return vector[self.i]


def is_attribute(method, name=None):
    """
    Decorator for methods that are attributes.
    """
    if name is None:
        name = method.__name__
    method.is_attribute = True
    method.name = name
    return method
