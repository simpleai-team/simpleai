#!/usr/bin/env python
# coding: utf-8

import math
import numpy
from collections import defaultdict


class Counter(defaultdict):

    def __init__(self, target):
        super(Counter, self).__init__(int)
        self.target = target
        self.total = 0

    def add(self, example):
        value = self.target(example)
        self[value] += 1
        self.total += 1


class OnlineEntropy(Counter):
    def get_entropy(self):
        s = 0.0
        for count in self.itervalues():
            p = count / float(self.total)
            s += p * math.log(p, 2)
        return -s


class OnlineInformationGain(object):

    def __init__(self, attribute, target):
        self.attribute = attribute
        self.H = OnlineEntropy(target)
        self.G = defaultdict(lambda: OnlineEntropy(target))

    def add(self, example):
        self.H.add(example)
        value = self.attribute(example)
        self.G[value].add(example)

    def get_target_class_counts(self):
        return self.H

    def get_branches(self):
        return self.G.items()

    def get_gain(self):
        H1 = self.H.get_entropy()
        H2 = 0.0
        for G in self.G.itervalues():
            w = G.total / float(self.H.total)
            H2 += w * G.get_entropy()
        return H1 - H2


class OnlineLogProbability(defaultdict):
    def __init__(self, _=None):  # `_` is for pickle-ability
        super(OnlineLogProbability, self).__init__(int)

    def add(self, x):
        d = super(OnlineLogProbability, self)
        v = d.__getitem__(x)
        d.__setitem__(x, v + 1)

    def __getitem__(self, x):
        if x not in self:
            raise KeyError(x)
        frequencies = super(OnlineLogProbability, self)
        logtotal = getattr(self, "_logtotal", None)
        if logtotal is None:
            logtotal = numpy.log(sum(frequencies.itervalues()))
            self._logtotal = logtotal
        return numpy.log(frequencies.get(x)) - logtotal
