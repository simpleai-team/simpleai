# -*- coding: utf-8 -*-
from collections import defaultdict, Counter
from .utils import argmax


def make_at_least_n_times(optimistic_reward, min_n):
    def at_least_n_times(utility, n):
        if n < min_n:
            return optimistic_reward
        return utility
    return at_least_n_times


class QLearner(object):

    def __init__(self, exploration_function, discount_factor, Q=None):
        if Q is None:
            self.Q = defaultdict(lambda: defaultdict(lambda: 0))
        else:
            self.Q = Q
        self.exploration_function = exploration_function
        self.last_state = None
        self.last_action = None
        self.counter = defaultdict(lambda: Counter())
        self.discount_factor = discount_factor
        self.trials = 0
        self.last_reward = None

    def update_state(self, percept):
        'Override this method if you need to clean perception'
        return percept

    def set_reward(self, reward, terminal=False):
        self.last_reward = reward
        if terminal:
            self.Q[self.last_state][self.last_action] = reward

    def step(self, percept):
        s = self.last_state
        a = self.last_action

        state = self.update_state(percept)
        actions = self.actions(state)

        if len(actions) > 0:
            #choose current action
            uf = lambda action: self.exploration_function(self.Q[state][action], self.counter[state][action])
            current_action = argmax(actions, uf)
        else:
            current_action = None

        if s is not None:
            self.counter[s][a] += 1
            self.update_rule(s, a, self.last_reward, state, current_action)

        self.last_state = state
        self.last_action = current_action
        return current_action

    def actions(self, state):
        '''Returns the actions available to perform from `state`.
           The returned value is an iterable over actions.
        '''
        pass

    def learning_rate(self, n):
        return 0.9

    def update_rule(self, s, a, r, cs, ca):
        raise NotImplementedError


class TD_QLearner(QLearner):

    def update_rule(self, s, a, r, cs, ca):
        lr = self.learning_rate(self.counter[s][a])
        self.Q[s][a] += lr * (r + self.discount_factor * max(self.Q[cs].values()) - self.Q[s][a])


class SARSA_Learner(QLearner):

    def update_rule(self, s, a, r, cs, ca):
        lr = self.learning_rate(self.counter[s][a])
        self.Q[s][a] += lr * (r + self.discount_factor * self.Q[cs][ca] - self.Q[s][a])
