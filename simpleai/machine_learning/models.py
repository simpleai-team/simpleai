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
    @property
    def attributes(self):
        attrs = getattr(self, "_attributes", None)
        if attrs is not None:
            return attrs
        attrs = []
        for name in dir(self):
            if name == "attributes":
                continue
            method = getattr(self, name)
            if getattr(method, "is_attribute", False):
                attr = Attribute(method, method.name)
                attrs.append(attr)
        self._attributes = attrs
        return attrs

    def target(self, example):
        raise NotImplementedError()


class VectorDataClassificationProblem(ClassificationProblem):

    def __init__(self, dataset, target_index):
        """
        Dataset should be an iterable, *not* an iterator
        """
        try:
            example = next(iter(dataset))
        except StopIteration:
            raise ValueError("Dataset is empty")
        self.i = target_index
        N = len(example)
        attributes = list(self.attributes)
        if self.i < 0:
            self.i = N + self.i
        if self.i < 0 or N <= self.i:
            raise ValueError("Target index is out of range")
        for i in xrange(N):
            if i == self.i:
                continue
            attribute = VectorIndexAttribute(i, "data at index {}".format(i))
            attributes.append(attribute)
        self._attributes = attributes

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
