# coding=utf-8
import heapq
from itertools import izip
import random


class FifoList(list):
    '''List that pops from the begining.'''
    def pop(self, index=0):
        return super(FifoList, self).pop(index)


class BoundedPriorityQueue(list):
    def __init__(self, limit=None, *args):
        self.limit = limit
        super(BoundedPriorityQueue, self).__init__(*args)

    def append(self, x):
        heapq.heappush(self, x)
        if self.limit and len(self) > self.limit:
            self.remove(heapq.nlargest(1, self)[0])

    def pop(self):
        return heapq.heappop(self)

    def extend(self, iterable):
        for x in iterable:
            self.append(x)

    def clear(self):
        for x in self:
            self.remove(x)


class InverseTransformSampler(object):
    def __init__(self, weights, objects):
        assert weights and objects and len(weights) == len(objects)
        self.objects = objects
        tot = float(sum(weights))
        if tot == 0:
            tot = len(weights)
            weights = [1 for x in weights]
        accumulated = 0
        self.probs = []
        for w, x in izip(weights, objects):
            p = w / tot
            accumulated += p
            self.probs.append(accumulated)

    def sample(self):
        target = random.random()
        i = 0
        while i + 1 != len(self.probs) and target > self.probs[i]:
            i += 1
        return self.objects[i]
