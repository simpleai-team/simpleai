# coding=utf-8
import unittest
from tests.search.dummies import DummyNode
from simpleai.search.utils import FifoList, BoundedPriorityQueue, LifoList, argmax, argmin


def sorted_equals_pop(l):
    _sorted = l.sorted()
    _sorted_by_pop = [l.pop() for x in range(len(l))]
    return _sorted == _sorted_by_pop


class TestLifoList(unittest.TestCase):
    def setUp(self):
        self.f = LifoList()
        self.f.append(1)
        self.f.append(2)
        self.f.append(3)

    def test_sorted_lifo(self):
        self.assertTrue(sorted_equals_pop(self.f))


class TestFifoList(unittest.TestCase):
    def setUp(self):
        self.f = FifoList()
        self.f.append(1)
        self.f.append(2)
        self.f.append(3)

    def test_pop_returns_first_element(self):
        self.assertEqual(self.f.pop(), 1)
        self.assertEqual(len(self.f), 2)

    def test_sorted_fifo(self):
        self.assertTrue(sorted_equals_pop(self.f))


class TestBoundedPriorityQueue(unittest.TestCase):
    def test_append_works(self):
        q = BoundedPriorityQueue()
        q.append(DummyNode(1))
        q.append(DummyNode(1))
        self.assertEqual(len(q), 2)

    def test_extend_works(self):
        q = BoundedPriorityQueue()
        q.extend([DummyNode(1), DummyNode(1)])
        self.assertEqual(len(q), 2)

    def test_pop_works_with_order(self):
        q = BoundedPriorityQueue()
        q.append(DummyNode(3))
        q.append(DummyNode(1))
        q.append(DummyNode(2))
        self.assertEqual(q.pop().value, 1)

    def test_limit_works_on_append(self):
        q = BoundedPriorityQueue(2)
        q.append(DummyNode(1))
        q.append(DummyNode(1))
        q.append(DummyNode(1))
        self.assertEqual(len(q), 2)

    def test_limit_works_on_extend(self):
        q = BoundedPriorityQueue(2)
        q.extend([DummyNode(1), DummyNode(1), DummyNode(1)])
        self.assertEqual(len(q), 2)

    def test_remove(self):
        q = BoundedPriorityQueue(2)
        a = DummyNode(1)
        b = DummyNode(2)
        q.append(a)
        q.append(b)
        q.remove(a)
        self.assertEqual(len(q), 1)
        self.assertIs(q[0], b)

    def test_sorted_priority(self):
        q = BoundedPriorityQueue()
        q.append(DummyNode(3))
        q.append(DummyNode(1))
        q.append(DummyNode(2))
        self.assertTrue(sorted_equals_pop(q))


class TestArgMax(unittest.TestCase):
    def setUp(self):
        self.d = {'a': 3, 'b': 1, 'c': 3}

    def test_return_max(self):
        self.assertEqual('a', argmax(['a', 'b'], lambda x: self.d[x]))

    def test_random_tie(self):
        a = 0
        for x in range(100):
            if argmax(['a', 'b', 'c'], lambda x: self.d[x]) == 'a':
                a += 1
        self.assertTrue(25 < a < 75)

    def test_empty_sequence(self):
        self.assertRaises(ValueError, argmax, [], lambda x: x)


class TestArgMin(unittest.TestCase):
    def setUp(self):
        self.d = {'a': 1, 'b': 1, 'c': 3}

    def test_return_max(self):
        self.assertEqual('b', argmin(['c', 'b'], lambda x: self.d[x]))

    def test_random_tie(self):
        a = 0
        for x in range(100):
            if argmin(['a', 'b', 'c'], lambda x: self.d[x]) == 'a':
                a += 1
        self.assertTrue(25 < a < 75)

    def test_empty_sequence(self):
        self.assertRaises(ValueError, argmin, [], lambda x: x)


