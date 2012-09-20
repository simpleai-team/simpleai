# coding=utf-8
import unittest
from simpleai.tests.dummies import DummyNode
from simpleai.utils import FifoList, BoundedPriorityQueue


class TestFifoList(unittest.TestCase):
    def setUp(self):
        self.f = FifoList()
        self.f.append(1)
        self.f.append(2)
        self.f.append(3)

    def test_pop_returns_first_element(self):
        self.assertEquals(self.f.pop(), 1)

    def test_pop_with_index_works(self):
        self.assertEquals(self.f.pop(1), 2)


class TestBoundedPriorityQueue(unittest.TestCase):
    def test_append_works(self):
        q = BoundedPriorityQueue()
        q.append(DummyNode(1))
        q.append(DummyNode(1))
        self.assertEquals(len(q), 2)

    def test_extend_works(self):
        q = BoundedPriorityQueue()
        q.extend([DummyNode(1), DummyNode(1)])
        self.assertEquals(len(q), 2)

    def test_pop_works_with_order(self):
        q = BoundedPriorityQueue()
        q.append(DummyNode(3))
        q.append(DummyNode(1))
        q.append(DummyNode(2))
        self.assertEquals(q.pop().value, 1)

    def test_limit_works_on_append(self):
        q = BoundedPriorityQueue(2)
        q.append(DummyNode(1))
        q.append(DummyNode(1))
        q.append(DummyNode(1))
        self.assertEquals(len(q), 2)

    def test_limit_works_on_extend(self):
        q = BoundedPriorityQueue(2)
        q.extend([DummyNode(1), DummyNode(1), DummyNode(1)])
        self.assertEquals(len(q), 2)
