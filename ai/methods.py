# coding=utf-8
from utils import FifoList, AddOnceList, AddOnceFifoList
from models import SearchNode


def breadth_first_tree_search(problem):
    return _tree_search(problem, FifoList())


def depth_first_tree_search(problem):
    return _tree_search(problem, [])


def breadth_first_graph_search(problem):
    return _tree_search(problem, AddOnceFifoList())


def depth_first_graph_search(problem):
    return _tree_search(problem, AddOnceList())


def _tree_search(problem, fringe):
    fringe.append(SearchNode(state=problem.initial_state,
                             parent=None,
                             cost=0,
                             problem=problem))
    while fringe:
        node = fringe.pop()
        if node.has_goal_state():
            return node
        fringe.extend(node.expand())
    return None
