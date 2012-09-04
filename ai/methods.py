# coding=utf-8
from utils import Fringe, FifoFringe, SortedFringe, BoundedPriorityQueue
from models import SearchNode


def breadth_first_tree_search(problem):
    return _search(problem, FifoFringe())


def breadth_first_graph_search(problem):
    return _search(problem, FifoFringe(avoid_repeated=True))


def depth_first_tree_search(problem):
    return _search(problem, Fringe())


def depth_first_graph_search(problem):
    return _search(problem, Fringe(avoid_repeated=True))


def limited_depth_first_tree_search(problem, depth_limit):
    return _search(problem, Fringe(), depth_limit=depth_limit)


def limited_depth_first_graph_search(problem, depth_limit):
    return _search(problem, Fringe(avoid_repeated=True),
                   depth_limit=depth_limit)


def iterative_limited_depth_first_tree_search(problem):
    return _iterative_limited_search(problem, limited_depth_first_tree_search)


def iterative_limited_depth_first_graph_search(problem):
    return _iterative_limited_search(problem, limited_depth_first_graph_search)


def uniform_cost_tree_search(problem):
    return _search(problem, SortedFringe(sorting_function=lambda n: n.cost))


def _iterative_limited_search(problem, search_method):
    solution = None
    limit = 0

    while not solution:
        solution = search_method(problem, limit)
        limit += 1

    return solution


def beam_search_best_first(problem, beamsize=100):
    return _search(problem, BoundedPriorityQueue(beamsize))


def beam_search_breadth_first(problem, beamsize=100):
    fringe = BoundedPriorityQueue(beamsize)
    while fringe:
        successors = BoundedPriorityQueue(beamsize)
        for node in fringe:
            if problem.is_goal(node.state):
                return node
            successors.extend(node.expand())
        fringe = successors


def _search(problem, fringe, depth_limit=None):
    fringe.add(SearchNode(state=problem.initial_state,
                          parent=None,
                          cost=0,
                          problem=problem,
                          depth=0))
    while fringe:
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node
        if depth_limit is None or node.depth < depth_limit:
            map(fringe.add, node.expand())
