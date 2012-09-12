# coding=utf-8
from utils import FifoList, BoundedPriorityQueue, Inverse_transform_sampler
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


def _all_expander(fringe, problem, iteration):
    for node in fringe:
        fringe.extend(node.expand())


def beam_search(problem, beam_size=100, iterations_limit=0):
    return _local_search(problem,
                         _all_expander,
                         iterations_limit=iterations_limit,
                         fringe_size=beam_size)


def _first_expander(fringe, problem, iteration):
    fringe.extend(fringe[0].expand())


def beam_search_best_first(problem, beam_size=100, iterations_limit=0):
    return _local_search(problem,
                         _first_expander,
                         iterations_limit=iterations_limit,
                         fringe_size=beam_size)


def hill_climbing(problem, iterations_limit=0):
    return _local_search(problem,
                         _first_expander,
                         iterations_limit=iterations_limit,
                         fringe_size=1)


def _random_best_expander(fringe, problem, iteration):
    current = fringe[0]
    betters = [n for n in current.expand()
               if n.value() > current.value()]
    if betters:
        random.shuffle(betters)
        fringe.append(betters[0])


def hill_climbing_stochastic(problem, iterations_limit=0):
    '''Stochastic hill climbing, where a random neighbor is chosen among
       those that have a better value'''
    return _local_search(problem,
                         _random_best_expander,
                         iterations_limit=iterations_limit,
                         fringe_size=1)


def hill_climbing_random_restarts(problem, restarts_limit, iterations_limit=0):
    restarts = 0
    best = None
    while restarts < restarts_limit:
        new = hill_climbing(problem, iterations_limit=iterations_limit)
        if not best or best.value() < new.value():
            best = new

        restarts += 1

    return best


# Math literally copied from aima-python
def _exp_schedule(iteration, k=20, lam=0.005, limit=100):
    "One possible schedule function for simulated annealing"
    return k * math.exp(-lam * iteration)


def _create_simulated_annealing_expander(schedule):
    def _expander(fringe, problem, iteration):
        T = schedule(iteration)
        current = fringe[0]
        neighbors = current.expand()
        if neighbors:
            succ = random.choice(neighbors)
            delta_e = succ.value() - current.value()
            if delta_e > 0 or random.random() < math.exp(delta_e / T):
                fringe.pop()
                fringe.append(succ)
    return _expander


def simulated_annealing(problem, schedule=_exp_schedule, iterations_limit=0):
    return _local_search(problem,
                         _create_simulated_annealing_expander(schedule),
                         iterations_limit=iterations_limit,
                         fringe_size=1)


def _create_genetic_expander(mutation_chance):
    def _expander(fringe, problem, iteration):
        fitness = [x.value() for x in fringe]
        sampler = Inverse_transform_sampler(fitness, fringe)
        new_generation = []
        for _ in fringe:
            node1 = sampler.sample()
            node2 = sampler.sample()
            child = problem.crossover(node1.state, node2.state)
            if random.random() < mutation_chance:
                # Noooouuu! she is... he is... *IT* is a mutant!
                child = problem.mutate(child)
            new_generation.append(child)

        fringe.clear()
        for s in new_generation:
            fringe.append(SearchNodeValueOrdered(state=s, problem=problem))

    return _expander


def genetic_search(problem, population_size=100, mutation_chance=0.1, iterations_limit=0):
    return _local_search(problem,
                         _create_genetic_expander(mutation_chance),
                         iterations_limit=iterations_limit,
                         fringe_size=1,
                         random_initial_states=True)


def _iterative_limited_search(problem, search_method, graph_search=False):
    solution = None
    limit = 0

    while not solution:
        solution = search_method(problem, limit, graph_search)
        limit += 1

    return solution


def _search(problem, fringe, graph_search=False, depth_limit=None,
            node_factory=SearchNode):
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


def _local_search(problem, fringe_expander, iterations_limit=0, fringe_size=1, random_initial_states=False):
    fringe = BoundedPriorityQueue(fringe_size)
    if random_initial_states:
        initials = [problem.generate_random_state()
                    for _ in xrange(fringe_size)]
        for s in initials:
            fringe.append(SearchNodeValueOrdered(state=s, problem=problem))
    else:
        fringe.append(SearchNodeValueOrdered(state=problem.initial_state,
                                             problem=problem))

    iteration = 0
    run = True
    best = None
    while run:
        old_best = fringe[0]
        fringe_expander(fringe, problem, iteration)
        best = fringe[0]

        iteration += 1

        if iterations_limit and iteration >= iterations_limit:
            run = False
        elif old_best.value() >= best.value():
            run = False

    return best



