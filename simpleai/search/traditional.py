# coding=utf-8
from simpleai.search.utils import FifoList, BoundedPriorityQueue, LifoList
from simpleai.search.models import (SearchNode, SearchNodeHeuristicOrdered,
                                    SearchNodeStarOrdered,
                                    SearchNodeCostOrdered)


def breadth_first(problem, graph_search=False, viewer=None):
    '''
    Breadth first search.

    If graph_search=True, will avoid exploring repeated states.
    Requires: SearchProblem.actions, SearchProblem.result, and
    SearchProblem.is_goal.
    '''
    return _search(problem,
                   FifoList(),
                   graph_search=graph_search,
                   viewer=viewer)


def depth_first(problem, graph_search=False, viewer=None):
    '''
    Depth first search.

    If graph_search=True, will avoid exploring repeated states.
    Requires: SearchProblem.actions, SearchProblem.result, and
    SearchProblem.is_goal.
    '''
    return _search(problem,
                   LifoList(),
                   graph_search=graph_search,
                   viewer=viewer)


def limited_depth_first(problem, depth_limit, graph_search=False, viewer=None):
    '''
    Limited depth first search.

    Depth_limit is the maximum depth allowed, being depth 0 the initial state.
    If graph_search=True, will avoid exploring repeated states.
    Requires: SearchProblem.actions, SearchProblem.result, and
    SearchProblem.is_goal.
    '''
    return _search(problem,
                   LifoList(),
                   graph_search=graph_search,
                   depth_limit=depth_limit,
                   viewer=viewer)


def iterative_limited_depth_first(problem, graph_search=False, viewer=None):
    '''
    Iterative limited depth first search.

    If graph_search=True, will avoid exploring repeated states.
    Requires: SearchProblem.actions, SearchProblem.result, and
    SearchProblem.is_goal.
    '''
    solution = None
    limit = 0

    while not solution:
        solution = limited_depth_first(problem,
                                       depth_limit=limit,
                                       graph_search=graph_search,
                                       viewer=viewer)
        limit += 1

    if viewer:
        viewer.event('no_more_runs', solution, 'returned after %i runs' % limit)

    return solution


def uniform_cost(problem, graph_search=False, viewer=None):
    '''
    Uniform cost search.

    If graph_search=True, will avoid exploring repeated states.
    Requires: SearchProblem.actions, SearchProblem.result,
    SearchProblem.is_goal, and SearchProblem.cost.
    '''
    return _search(problem,
                   BoundedPriorityQueue(),
                   graph_search=graph_search,
                   node_factory=SearchNodeCostOrdered,
                   graph_replace_when_better=True,
                   viewer=viewer)


def greedy(problem, graph_search=False, viewer=None):
    '''
    Greedy search.

    If graph_search=True, will avoid exploring repeated states.
    Requires: SearchProblem.actions, SearchProblem.result,
    SearchProblem.is_goal, SearchProblem.cost, and SearchProblem.heuristic.
    '''
    return _search(problem,
                   BoundedPriorityQueue(),
                   graph_search=graph_search,
                   node_factory=SearchNodeHeuristicOrdered,
                   graph_replace_when_better=True,
                   viewer=viewer)


def astar(problem, graph_search=False, viewer=None):
    '''
    A* search.

    If graph_search=True, will avoid exploring repeated states.
    Requires: SearchProblem.actions, SearchProblem.result,
    SearchProblem.is_goal, SearchProblem.cost, and SearchProblem.heuristic.
    '''
    return _search(problem,
                   BoundedPriorityQueue(),
                   graph_search=graph_search,
                   node_factory=SearchNodeStarOrdered,
                   graph_replace_when_better=True,
                   viewer=viewer)


def _search(problem, fringe, graph_search=False, depth_limit=None,
            node_factory=SearchNode, graph_replace_when_better=False,
            viewer=None):
    '''
    Basic search algorithm, base of all the other search algorithms.
    '''
    if viewer:
        viewer.event('started')

    memory = {}
    initial_node = node_factory(state=problem.initial_state,
                                problem=problem)
    fringe.append(initial_node)
    memory[problem.initial_state] = initial_node

    while fringe:
        if viewer:
            viewer.event('new_iteration', fringe.sorted())

        node = fringe.pop()

        if problem.is_goal(node.state):
            if viewer:
                viewer.event('chosen_node', node, True)
                viewer.event('finished', fringe.sorted(), node, 'goal found')
            return node
        else:
            if viewer:
                viewer.event('chosen_node', node, False)

        if depth_limit is None or node.depth < depth_limit:
            childs = []
            expanded = node.expand()
            if viewer:
                viewer.event('expanded', [node], [expanded])

            for n in expanded:
                if graph_search:
                    if n.state not in memory:
                        memory[n.state] = n
                        childs.append(n)
                    elif graph_replace_when_better:
                        other = memory[n.state]
                        if n < other:
                            memory[n.state] = n
                            childs.append(n)
                            if other in fringe:
                                fringe.remove(other)
                else:
                    childs.append(n)

            for n in childs:
                fringe.append(n)

    if viewer:
        viewer.event('finished', fringe.sorted(), None, 'goal not found')
