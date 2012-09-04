# coding=utf-8
import unittest
from ai.utils import FifoList


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


