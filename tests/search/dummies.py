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

    def generate_random_state(self):
        return 'i'


class DummyGeneticProblem(object):
    def value(self, state):
        return state + 1

    def crossover(self, state1, state2):
        return state1 + 1

    def mutate(self, state):
        return 20  # Mutants are like that

    def generate_random_state(self):
        return 4  # Please see http://xkcd.com/221/


class DummyGraphProblem(object):

    _map = {
            'r': {'l': 16},
            'l': {'s': 26, 'a': 10, 'r': 16},
            'a': {'s': 15, 'l': 10},
            's': {'l': 26, 'a': 15},
            }

    consistent = {'r': 0, 'l': 15, 'a': 25, 's': 30}
    inconsistent = {'r': 0, 'l': 10, 'a': 25, 's': 30}
    inadmissible = {'r': 0, 'l': 15, 'a': 28, 's': 30}

    def __init__(self, heuristic_dict=None):
        self.initial_state = 's'
        self.goal = 'r'
        self.heuristic_dict = heuristic_dict

    def is_goal(self, state):
        return state == self.goal

    def actions(self, state):
        "returns state's neighbors"
        return list(self._map[state].keys())

    def result(self, state, action):
        'returns the action because it indicates the next city'
        return action

    def cost(self, state1, action, state2):
        return self._map[state1][state2]

    def heuristic(self, state):
        return self.heuristic_dict[state]

    def state_representation(self, state):
        return state

    def action_representation(self, action):
        return action