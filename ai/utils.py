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


def get_max_random_tie(seq, fn):
    '''Returns the element in seq with the highest value for fn,
       breaks tie in random.
    '''
    best_score = fn(seq[0])
    n = 0
    for x in seq:
        x_score = fn(x)
        if x_score > best_score:
            best, best_score = x, x_score
            n = 1
        elif x_score == best_score:
            n += 1
            if random.randrange(n) == 0:
                best = x
    return best
