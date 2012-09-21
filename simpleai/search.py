# coding=utf-8
from utils import FifoList, BoundedPriorityQueue
from models import (SearchNode, SearchNodeHeuristicOrdered,
                    SearchNodeStarOrdered, SearchNodeCostOrdered)


def breadth_first(problem, graph_search=False):
    '''
    Breadth first search.

    If graph_search=True, will avoid exploring repeated states.
    Requires: Problem.actions, Problem.result, Problen.is_goal.
    '''
    return _search(problem,
                   FifoList(),
                   graph_search=graph_search)


def depth_first(problem, graph_search=False):
    '''
    Depth first search.

    If graph_search=True, will avoid exploring repeated states.
    Requires: Problem.actions, Problem.result, Problen.is_goal.
    '''
    return _search(problem,
                   [],
                   graph_search=graph_search)


def limited_depth_first(problem, depth_limit, graph_search=False):
    '''
    Limited depth first search.

    Depth_limit is the maximum depth allowed, being depth 0 the initial state.
    If graph_search=True, will avoid exploring repeated states.
    Requires: Problem.actions, Problem.result, Problen.is_goal.
    '''
    return _search(problem,
                   [],
                   graph_search=graph_search,
                   depth_limit=depth_limit)


def iterative_limited_depth_first(problem, graph_search=False):
    '''
    Iterative limited depth first search.

    If graph_search=True, will avoid exploring repeated states.
    Requires: Problem.actions, Problem.result, Problen.is_goal.
    '''
    solution = None
    limit = 0

    while not solution:
        solution = limited_depth_first(problem, limit, graph_search)
        limit += 1

    return solution


def uniform_cost(problem, graph_search=False):
    '''
    Uniform cost search.

    If graph_search=True, will avoid exploring repeated states.
    Requires: Problem.actions, Problem.result, Problen.is_goal, Problem.cost.
    '''
    return _search(problem,
                   BoundedPriorityQueue(),
                   graph_search=graph_search,
                   node_factory=SearchNodeCostOrdered)


def greedy(problem, graph_search=False):
    '''
    Greedy search.

    If graph_search=True, will avoid exploring repeated states.
    Requires: Problem.actions, Problem.result, Problen.is_goal, Problem.cost,
    and Problem.heuristic.
    '''
    return _search(problem,
                   BoundedPriorityQueue(),
                   graph_search=graph_search,
                   node_factory=SearchNodeHeuristicOrdered)


def astar(problem, graph_search=False):
    '''
    A* search.

    If graph_search=True, will avoid exploring repeated states.
    Requires: Problem.actions, Problem.result, Problen.is_goal, Problem.cost,
    and Problem.heuristic.
    '''
    return _search(problem,
                   BoundedPriorityQueue(),
                   graph_search=graph_search,
                   node_factory=SearchNodeStarOrdered)


def _search(problem, fringe, graph_search=False, depth_limit=None,
            node_factory=SearchNode):
    '''
    Basic search algorithm, base of all the other search algorithms.
    '''
    memory = set()
    fringe.append(node_factory(state=problem.initial_state,
                               problem=problem))

    while fringe:
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node
        if depth_limit is None or node.depth < depth_limit:
            childs = []
            for n in node.expand():
                if graph_search:
                    if n.state not in memory:
                        memory.add(n.state)
                        childs.append(n)
                else:
                    childs.append(n)

            for n in childs:
                fringe.append(n)
