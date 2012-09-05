# coding=utf-8
from simpleai.models import Problem
from simpleai.methods import astar_search

GOAL = 'HELLO WORLD'

class HelloProblem(Problem):
    def actions(self, state):
        if len(state) < len(GOAL):
            return [c for c in ' ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        else:
            return []

    def result(self, state, action):
        return state + action

    def is_goal(self, state):
        return state == GOAL

    def heuristic(self, state):
        # count wrong chars
        wrong = sum([1 if state[i] != GOAL[i] else 0
                    for i in range(len(state))])
        missing = len(GOAL) - len(state)
        return wrong + missing


problem = HelloProblem(initial_state='')
result = astar_search(problem)

print result
print result.path()
