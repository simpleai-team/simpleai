# coding=utf-8
import bisect

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


class Fringe(object):
    '''Basic fringe of nodes (lifo).'''
    def __init__(self, avoid_repeated=False):
        if avoid_repeated:
            self.nodes = AddOnceList()
        else:
            self.nodes = []

    def add(self, node):
        self.nodes.append(node)

    def pop(self):
        return self.nodes.pop()

    def __len__(self):
        return len(self.nodes)


class FifoFringe(Fringe):
    '''Fringe that pops from the begining.'''
    def pop(self):
        return self.nodes.pop(0)


class SortedFringe(FifoFringe):
    '''Fringe that pops the element based on a value function (less value pops first).'''
    def __init__(self, sorting_function):
        super(SortedFringe, self).__init__()
        self.sorting_function = sorting_function

    def add(self, node):
        node.sorted_fringe_value = self.sorting_function(node)
        for i, n in enumerate(self.nodes):
            if node.sorted_fringe_value < n.sorted_fringe_value:
                self.nodes.insert(i, node)
                return
        self.nodes.append(node)

