# coding=utf-8
from utils import BoundedPriorityQueue, InverseTransformSampler
from models import SearchNodeValueOrdered
import math
import random


def _all_expander(fringe, iteration):
    '''
    Expander that expands all nodes on the fringe.
    '''
    for node in fringe:
        fringe.extend(node.expand(local_search=True))


def beam(problem, beam_size=100, iterations_limit=0):
    '''
    Beam search.

    beam_size is the size of the beam.
    If iterations_limit is specified, the algorithm will end after that
    number of iterations. Else, it will continue until it can't find a
    better node than the current one.
    Requires: Problem.actions, Problem.result, Problem.value.
    '''
    return _local_search(problem,
                         _all_expander,
                         iterations_limit=iterations_limit,
                         fringe_size=beam_size)


def _first_expander(fringe, iteration):
    '''
    Expander that expands only the first node on the fringe.
    '''
    fringe.extend(fringe[0].expand(local_search=True))


def beam_best_first(problem, beam_size=100, iterations_limit=0):
    '''
    Beam search best first.

    beam_size is the size of the beam.
    If iterations_limit is specified, the algorithm will end after that
    number of iterations. Else, it will continue until it can't find a
    better node than the current one.
    Requires: Problem.actions, Problem.result, Problem.value.
    '''
    return _local_search(problem,
                         _first_expander,
                         iterations_limit=iterations_limit,
                         fringe_size=beam_size)


def hill_climbing(problem, iterations_limit=0):
    '''
    Hill climbing search.

    If iterations_limit is specified, the algorithm will end after that
    number of iterations. Else, it will continue until it can't find a
    better node than the current one.
    Requires: Problem.actions, Problem.result, Problem.value.
    '''
    return _local_search(problem,
                         _first_expander,
                         iterations_limit=iterations_limit,
                         fringe_size=1)


def _random_best_expander(fringe, iteration):
    '''
    Expander that expands one randomly choosen nodes on the fringe that
    is better than the current (first) node.
    '''
    current = fringe[0]
    betters = [n for n in current.expand(local_search=True)
               if n.value() > current.value()]
    if betters:
        random.shuffle(betters)
        fringe.append(betters[0])


def hill_climbing_stochastic(problem, iterations_limit=0):
    '''
    Stochastic hill climbing.

    If iterations_limit is specified, the algorithm will end after that
    number of iterations. Else, it will continue until it can't find a
    better node than the current one.
    Requires: Problem.actions, Problem.result, Problem.value.
    '''
    return _local_search(problem,
                         _random_best_expander,
                         iterations_limit=iterations_limit,
                         fringe_size=1)


def hill_climbing_random_restarts(problem, restarts_limit, iterations_limit=0):
    '''
    Hill climbing with random restarts.

    restarts_limit specifies the number of times hill_climbing will be runned.
    If iterations_limit is specified, each hill_climbing will end after that
    number of iterations. Else, it will continue until it can't find a
    better node than the current one.
    Requires: Problem.actions, Problem.result, Problem.value, and
    Problem.generate_random_state.
    '''
    restarts = 0
    best = None
    while restarts < restarts_limit:
        new = _local_search(problem,
                            _first_expander,
                            iterations_limit=iterations_limit,
                            fringe_size=1,
                            random_initial_states=True)

        if not best or best.value() < new.value():
            best = new

        restarts += 1

    return best


# Math literally copied from aima-python
def _exp_schedule(iteration, k=20, lam=0.005, limit=100):
    '''
    Possible scheduler for simulated_annealing, based on the aima example.
    '''
    return k * math.exp(-lam * iteration)


def _create_simulated_annealing_expander(schedule):
    '''
    Creates an expander that has a random chance to choose a node that is worse
    than the current (first) node, but that chance decreases with time.
    '''
    def _expander(fringe, iteration):
        T = schedule(iteration)
        current = fringe[0]
        neighbors = current.expand(local_search=True)
        if neighbors:
            succ = random.choice(neighbors)
            delta_e = succ.value() - current.value()
            if delta_e > 0 or random.random() < math.exp(delta_e / T):
                fringe.pop()
                fringe.append(succ)
    return _expander


def simulated_annealing(problem, schedule=_exp_schedule, iterations_limit=0):
    '''
    Simulated annealing.

    schedule is the scheduling function that decides the chance to choose worst
    nodes depending on the time.
    If iterations_limit is specified, the algorithm will end after that
    number of iterations. Else, it will continue until it can't find a
    better node than the current one.
    Requires: Problem.actions, Problem.result, Problem.value.
    '''
    return _local_search(problem,
                         _create_simulated_annealing_expander(schedule),
                         iterations_limit=iterations_limit,
                         fringe_size=1)


def _create_genetic_expander(problem, mutation_chance):
    '''
    Creates an expander that expands the bests nodes of the population,
    crossing over them.
    '''
    def _expander(fringe, iteration):
        fitness = [x.value() for x in fringe]
        sampler = InverseTransformSampler(fitness, fringe)
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


def genetic(problem, population_size=100, mutation_chance=0.1,
            iterations_limit=0):
    '''
    Genetic search.

    population_size specifies the size of the population (ORLY).
    mutation_chance specifies the probability of a mutation on a child,
    varying from 0 to 1.
    If iterations_limit is specified, the algorithm will end after that
    number of iterations. Else, it will continue until it can't find a
    better node than the current one.
    Requires: Problem.generate_random_state, Problem.crossover, Problem.mutate
    and Problem.value.
    '''
    return _local_search(problem,
                         _create_genetic_expander(problem, mutation_chance),
                         iterations_limit=iterations_limit,
                         fringe_size=1,
                         random_initial_states=True)


def _local_search(problem, fringe_expander, iterations_limit=0, fringe_size=1,
                  random_initial_states=False):
    '''
    Basic algorithm for all local search algorithms.
    '''
    fringe = BoundedPriorityQueue(fringe_size)
    if random_initial_states:
        for _ in xrange(fringe_size):
            s = problem.generate_random_state()
            fringe.append(SearchNodeValueOrdered(state=s, problem=problem))
    else:
        fringe.append(SearchNodeValueOrdered(state=problem.initial_state,
                                             problem=problem))

    iteration = 0
    run = True
    best = None
    while run:
        old_best = fringe[0]
        fringe_expander(fringe, iteration)
        best = fringe[0]

        iteration += 1

        if iterations_limit and iteration >= iterations_limit:
            run = False
        elif old_best.value() >= best.value():
            run = False

    return best
