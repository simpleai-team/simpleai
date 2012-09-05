# coding=utf-8


class DummyNode(object):
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        return self.value < other.value


class DummyProblem(object):
    def actions(self, state):
        return ['a1', 'a2', 'a3']

    def result(self, state, action):
        return state + action

    def is_goal(self, state):
        return state == 'ia1'

    def cost(self, state1, action, state2):
        return 1

    def value(self, state):
        return len(state)

    def heuristic(self, state):
        return len(state)


