#!/usr/bin/env python
# coding: utf-8

"""
Basic API for modeling a classification problem.
"""

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
        self.learn()

    def learn(self):
        """
        Does the training. Returns nothing.
        """
        raise NotImplementedError()

    @property
    def attributes(self):
        """
        The attributes of the problem.
        A list of callable objects.
        """
        return self.problem.attributes

    @property
    def target(self):
        """
        The problem's target.
        A callable that takes an observation and returns the correct
        classification for it.
        """
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
        """
        Loads a pickled version of the classifier saved in `filepath`
        """
        with open(filepath) as filehandler:
            classifier = pickle.load(filehandler)

        if not isinstance(classifier, Classifier):
            raise ValueError("Pickled object is not a Classifier")

        return classifier


class ClassificationProblem(object):
    """
    Abstract representation of a classification problem.
    It holds the attributes to be tested and defines them
    "target" of an example.

    You can define attributes by adding them to the `attributes`
    list or by defining a method and decorating it with `is_attribute`.

    The target method returns the real classification of an example from
    the dataset.
    """

    def __init__(self):
        self._load_self_attributes()

    def _load_self_attributes(self, attrs=None):
        if attrs is None:
            attrs = []
        for name in dir(self):
            method = getattr(self, name)
            if hasattr(method, "is_attribute"):
                attr = Attribute(method, method.name)
                attrs.append(attr)
        self.attributes = attrs
        # This sort is useful in cases where attributes are feeded vectorized
        # to the classifier (like SVMs) and you want to pickle and unpickle it
        # safely.
        # Requieres attributes to have names.
        self.attributes.sort(key=lambda attr: attr.name)

    def target(self, example):
        """
        Given an example it returns the classification for that
        example.
        """
        raise NotImplementedError()

    def __getstate__(self):
        # For pickle-ability of method objects
        attributes = [a for a in self.attributes
                      if not hasattr(a.function, "is_attribute")]
        d = dict(self.__dict__)
        d["attributes"] = attributes
        return d

    def __setstate__(self, d):
        # For pickle-ability
        for name, value in d.iteritems():
            setattr(self, name, value)
        self._load_self_attributes(self.attributes)


class VectorDataClassificationProblem(ClassificationProblem):
    """
    A classification problem that defines attribute for a dataset
    that is a set of vectors. An attribute for each index of the
    vector is created.
    """

    def __init__(self, dataset, target_index):
        """
        `dataset` should be an iterable, *not* an iterator.
        `target_index` is the index in the vector where the classification
        of an example is defined.
        """
        super(VectorDataClassificationProblem, self).__init__()
        try:
            example = next(iter(dataset))
        except StopIteration:
            raise ValueError("Dataset is empty")

        self.target_index = target_index

        N = len(example)
        if self.target_index < 0:  # Negative number allowed, counts in reverse
            self.target_index = N + self.target_index
        if self.target_index < 0 or N <= self.target_index:
            raise ValueError("Target index is out of range")
        for i in xrange(N):
            if i == self.target_index:
                continue
            attribute = VectorIndexAttribute(i, "data at index {}".format(i))
            self.attributes.append(attribute)

    def target(self, example):
        """
        Uses the target defined in the creation of the vector problem
        to return the target of `example`.
        """
        return example[self.target_index]


class Attribute(object):
    """
    Abstract base of an attribute, a feature to be tested on the
    examples.
    """

    def __init__(self, function=None, name=None, description=None):
        """
        Creates an attribute with `function`.
        Adds a name and a description if it's specified.
        """
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
    Attribute that returns the n-th element from a vector.
    """

    def __init__(self, n, name=None, description=None):
        super(VectorIndexAttribute, self).__init__(self, name, description)
        self.n = n

    def reason(self, vector):
        message = "{} is the {}-th element of the vector"
        return message.format(vector[self.n], self.n)

    def __call__(self, vector):
        return vector[self.n]


def is_attribute(method, name=None):
    """
    Decorator for methods that are attributes.
    """
    if name is None:
        name = method.__name__
    method.is_attribute = True
    method.name = name
    return method
