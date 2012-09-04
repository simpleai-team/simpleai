# coding=utf-8
from utils import FifoList, BoundedPriorityQueue
from models import SearchNode, SearchNodeHeuristicOrdered, SearchNodeStarOrdered


def breadth_first_search(problem, graph_search=False):
    return _search(problem,
                   FifoList(),
                   graph_search=graph_search)


def depth_first_search(problem, graph_search=False):
    return _search(problem,
                   [],
                   graph_search=graph_search)


def limited_depth_first_search(problem, depth_limit, graph_search=False):
    return _search(problem,
                   [],
                   graph_search=graph_search,
                   depth_limit=depth_limit)


def iterative_limited_depth_first_search(problem, graph_search=False):
    return _iterative_limited_search(problem,
                                     limited_depth_first_search,
                                     graph_search=graph_search)


def uniform_cost_search(problem, graph_search=False):
    return _search(problem,
                   BoundedPriorityQueue(),
                   graph_search=graph_search)


def greedy_search(problem, graph_search=False):
    return _search(problem,
                   BoundedPriorityQueue(),
                   graph_search=graph_search,
                   node_factory=SearchNodeHeuristicOrdered)


def astar_search(problem, graph_search=False):
    return _search(problem,
                   BoundedPriorityQueue(),
                   graph_search=graph_search,
                   node_factory=SearchNodeStarOrdered)


def _iterative_limited_search(problem, search_method, graph_search=False):
    solution = None
    limit = 0

    while not solution:
        solution = search_method(problem, limit, graph_search)
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


def _search(problem, fringe, graph_search=False, depth_limit=None, node_factory=SearchNode):
    memory = set()
    fringe.append(node_factory(state=problem.initial_state,
                               parent=None,
                               cost=0,
                               problem=problem,
                               depth=0))

    while fringe:
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node
        if depth_limit is None or node.depth < depth_limit:
            for n in node.expand():
                if graph_search:
                    if hash(n.state) not in memory:
                        memory.add(hash(n.state))
                        fringe.append(n)
                else:
                    fringe.append(n)
