# coding=utf-8


class DummyNode(object):
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        return self.value < other.value


GOAL = 'iabcabc'

class DummyProblem(object):
    def actions(self, state):
        return ['a', 'b', 'c'] if len(state) < len(GOAL) else []

    def result(self, state, action):
        return state + action

    def is_goal(self, state):
        return state == GOAL

    def heuristic(self, state):
        # incorrect or missing actions
        return (len(GOAL) - self.value(state)) - 1

    def value(self, state):
        # correct actions
        return sum(1 if state[i] == GOAL[i] else 0
                   for i in range(min(len(GOAL), len(state)))) - 1

    def cost(self, state1, action, state2):
        return 1


class DummyGeneticProblem(object):
    def value(self, state):
        return 1

    def crossover(self, state1, state2):
        return state1 + 1

    def mutate(self, state):
        return None  # Mutants are like that

    def generate_random_state(self):
        return 4  # Please see http://xkcd.com/221/
