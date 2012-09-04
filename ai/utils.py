# coding=utf-8


class FifoList(list):
    '''List that pops from the begining.'''

    def pop(self, index=0):
        return super(FifoList, self).pop(index)


class AddOnceList(list):
    '''List which doesn't allow adding two times the same element,
    even when the element isn't present on the list any more.'''

    def __init__(self, *args, **kargs):
        super(AddOnceList, self).__init__(*args, **kargs)
        self.memory = set()

    def append(self, element):
        if hash(element) not in self.memory:
            super(AddOnceList, self).append(element)
            self.memory.add(hash(element))

    def extend(self, iterable):
        new_elements = [x for x in iterable
                        if hash(x) not in self.memory]
        super(AddOnceList, self).extend(new_elements)


class AddOnceFifoList(FifoList, AddOnceList):
    '''Combines a FifoList with a AddOnceList.'''
    pass


class CostSortedList(list):
    '''List that pops the element with less cost.'''
    def pop(self):
        if self:
            cheapest, position = self[0], 0
            for i, n in enumerate(self):
                if n.cost < cheapest.cost:
                    cheapest, position = n, i
            return super(CostSortedList, self).pop(position)
        else:
            raise IndexError('pop from empty list')
