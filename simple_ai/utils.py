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
        heapq.heappush(self, x)
        if self.limit and len(self) > self.limit:
            self.remove(heapq.nlargest(1, self)[0])

    def pop(self):
        return heapq.heappop(self)

    def extend(self, iterable):
        for x in iterable:
            self.append(x)
