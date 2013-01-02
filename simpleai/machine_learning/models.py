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
        return self.name


class VectorIndexAttribute(Attribute):
    def __init__(self, i, name=None, description=None):
        self.i = i
        self.name = name
        self.description = description

    def __call__(self, vector):
        return vector[self.i]


def is_attribute(method, name=None):
    if name is None:
        name = method.__name__
    method.is_attribute = True
    method.name = name
    return method
