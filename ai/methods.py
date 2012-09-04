# coding=utf-8
from utils import FifoList, BoundedPriorityQueue
from models import (SearchNode, SearchNodeHeuristicOrdered,
                    SearchNodeStarOrdered, SearchNodeCostOrdered,
                    SearchNodeValueOrdered)
import copy
import math
import random
from itertools import count


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
                   graph_search=graph_search,
                   node_factory=SearchNodeCostOrdered)


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


def beam_search(problem, beam_size=100, graph_search=False, node_filter=None):
    return _search(problem,
                   BoundedPriorityQueue(beam_size),
                   node_factory=SearchNodeValueOrdered,
                   local_search=True)


def hill_climbing(problem, graph_search=False, node_filter=None):
    return beam_search(problem,
                       beam_size=1,
                       graph_search=graph_search,
                       node_filter=node_filter)


def _filter_random_uphill_neighbor(problem, node, childs):
    neighbor = None
    is_uphill = lambda x: problem.value(x.state) > problem.value(node.state)
    uphill = filter(is_uphill, childs)
    if uphill:
        random.shuffle(uphill)
        neighbor = uphill[0]
    return [neighbor, ]


def hill_climbing_stochastic(problem, graph_search=False):
    '''Stochastic hill climbing, where a random neighbor is chosen among
       those that have a better value'''
    return hill_climbing(problem,
                         graph_search=graph_search,
                         node_filter=_filter_random_uphill_neighbor)


def _filter_first_choice_random(problem, node, childs):
    neighbor = None
    eligible = copy.copy(childs)
    current_value = problem.value(node.state)
    while eligible:
        candidate = eligible.pop()
        if problem.value(candidate.state) > current_value:
            neighbor = candidate
            break
    return neighbor


def hill_climbing_first_choice(problem, graph_search=False):
    '''First-choice hill climbing, where neighbors are randomly taken and the
       first with a better value is chosen'''
    return hill_climbing(problem,
                         graph_search=graph_search,
                         node_filter=_filter_first_choice_random)


# Quite literally copied from aima
def simulated_annealing(problem, schedule=None):
    if not schedule:
        schedule = _exp_schedule()
    current = SearchNode(problem.initial_state,
                         problem=problem)
    for t in count():
        T = schedule(t)
        if T == 0:
            return current
        neighbors = current.expand()
        if not neighbors:
            return current
        succ = random.choice(neighbors)
        delta_e = problem.value(succ.state) - problem.value(current.state)
        if delta_e > 0 or random.random() < math.exp(delta_e / T):
            current = succ


def _iterative_limited_search(problem, search_method, graph_search=False):
    solution = None
    limit = 0

    while not solution:
        solution = search_method(problem, limit, graph_search)
        limit += 1

    return solution


def _search(problem, fringe, graph_search=False, depth_limit=None,
            node_factory=SearchNode, local_search=False, node_filter=None):
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

            if node_filter:
                childs = node_filter(problem, node, childs)

            for n in childs:
                fringe.append(n)


# Math literally copied from aima-python
def _exp_schedule(k=20, lam=0.005, limit=100):
    "One possible schedule function for simulated annealing"
    def f(t):
        if t < limit:
            return k * math.exp(-lam * t)
        return 0
    return f
