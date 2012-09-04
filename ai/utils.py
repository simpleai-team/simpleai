# coding=utf-8
import heapq


class FifoList(list):
    '''List that pops from the begining.'''
    def pop(self, index=0):
        return super(FifoList, self).pop(index)


class BoundedPriorityQueue(list):
    def __init__(self, limit=None, *args):
        self.limit = limit
        super(BoundedPriorityQueue, self).__init__(*args)

    def append(self, x):
        if len(self) == self.limit:
            heapq.heappushpop(self, x)
        else:
            heapq.heappush(self, x)

    def pop(self):
        return heapq.heappop(self)

    def extend(self, iterable):
        for x in iterable:
            self.append(x)
