# coding=utf-8
import unittest
from tests.search.dummies import DummyProblem, GOAL, DummyGeneticProblem
from simpleai.search.local import (beam, beam_best_first,
                                   hill_climbing,
                                   hill_climbing_stochastic,
                                   simulated_annealing,
                                   hill_climbing_random_restarts, genetic)
from simpleai.search.models import SearchNode


class TestLocalSearch(unittest.TestCase):
    def setUp(self):
        self.problem = DummyProblem()
        self.problem.initial_state = 'i'

    def test_beam(self):
        result = beam(self.problem)
        self.assertEqual(result.state, GOAL)

    def test_beam_best_first(self):
        result = beam_best_first(self.problem)
        self.assertEqual(result.state, GOAL)

    def test_hill_climbing(self):
        result = hill_climbing(self.problem)
        self.assertEqual(result.state, GOAL)

    def test_hill_climbing_stochastic(self):
        result = hill_climbing_stochastic(self.problem)
        self.assertEqual(result.state, GOAL)

    def test_hill_climbing_random_restarts(self):
        result = hill_climbing_random_restarts(self.problem, restarts_limit=2)
        self.assertEqual(result.state, GOAL)

    def test_simulated_annealing(self):
        # give the problem an actions function that always
        # goes up, to test if simulated_annealing takes the
        # correct states
        def dummy_actions(state):
            if len(state) < len(GOAL):
                return {'i': 'a',
                        'a': 'b',
                        'b': 'c',
                        'c': 'a'}[state[-1]]
            else:
                return []
        self.problem.actions = dummy_actions
        result = simulated_annealing(self.problem)
        self.assertEqual(result.state, GOAL)


class TestGeneticSearch(unittest.TestCase):

    def setUp(self):
        self.problem = DummyGeneticProblem()

    def test_solution_is_node(self):
        node = genetic(self.problem, iterations_limit=1, mutation_chance=0, population_size=1)
        self.assertIsInstance(node, SearchNode)

    def test_calls_crossover(self):
        node = genetic(self.problem, iterations_limit=1, mutation_chance=0, population_size=5)
        self.assertEqual(node.state, 5)

    def test_calls_mutation(self):
        node = genetic(self.problem, iterations_limit=1, mutation_chance=1, population_size=5)
        self.assertEqual(node.state, 20)

    def test_count_generations(self):
        node = genetic(self.problem, iterations_limit=10, mutation_chance=0, population_size=5)
        self.assertEqual(node.state, 14)  # initial is 4, plus 10 generations

    def test_zero_fitness_get_waxed(self):
        count = [-1]

        def g():
            count[0] = count[0] + 1  # Nasty trick uh? try without the list
            return [0, 0, 1, 0, 0][count[0]]

        def fitness(state):
            return state

        self.problem.generate_random_state = g
        self.problem.value = fitness
        node = genetic(self.problem, iterations_limit=1, mutation_chance=0, population_size=5)
        self.assertEqual(node.state, 2)
