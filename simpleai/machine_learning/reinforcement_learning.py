# -*- coding: utf-8 -*-
from collections import defaultdict, Counter
import math
import random
from .utils import argmax


def make_at_least_n_times(optimistic_reward, min_n):
    def at_least_n_times_exploration(actions, utilities, temperature, action_counter):
        utilities = [utilities[x] for x in actions]
        for i, utility in enumerate(utilities):
            if action_counter[actions[i]] < min_n:
                utilities[i] = optimistic_reward
        d = dict(zip(actions, utilities))
        uf = lambda action: d[action]
        return argmax(actions, uf)

    return at_least_n_times_exploration


def boltzmann_exploration(actions, utilities, temperature, action_counter):
    '''returns an action with a probability depending on utilities and temperature'''
    utilities = [utilities[x] for x in actions]
    temperature = max(temperature, 0.01)
    _max = max(utilities)
    _min = min(utilities)
    if _max == _min:
        return random.choice(actions)

    utilities = [math.exp(((u - _min) / (_max - _min)) / temperature) for u in utilities]
    probs = [u / sum(utilities) for u in utilities]
    i = 0
    tot = probs[i]
    r = random.random()
    while i < len(actions) and r >= tot:
        i += 1
        tot += probs[i]
    return actions[i]


def make_exponential_temperature(initial_temperature, alpha):
    '''returns a function like initial / exp(n * alpha)'''
    def _function(n):
        try:
            return initial_temperature / math.exp(n * alpha)
        except OverflowError:
            return 0.01
    return _function


class QLearner(object):

    def __init__(self, exploration_function, discount_factor, temperature_function, Q=None):
        if Q is None:
            self.Q = defaultdict(lambda: defaultdict(lambda: 0))
        else:
            self.Q = Q
        self.exploration_function = exploration_function
        self.last_state = None
        self.last_action = None
        self.counter = defaultdict(lambda: Counter())
        self.discount_factor = discount_factor
        self.temperature_function = temperature_function
        self.trials = 0
        self.last_reward = None
        self.accumulated_rewards = [0]

    def update_state(self, percept):
        'Override this method if you need to clean perception'
        return percept

    def set_reward(self, reward, terminal=False):
        self.last_reward = reward
        if terminal:
            self.Q[self.last_state][self.last_action] = reward
            if len(self.accumulated_rewards) > 0:
                self.accumulated_rewards.append(self.accumulated_rewards[-1] + reward)
            else:
                self.accumulated_rewards.append(reward)

    def step(self, percept):
        s = self.last_state
        a = self.last_action

        state = self.update_state(percept)
        actions = self.actions(state)

        self.trials += 1

        if len(actions) > 0:
            current_action = self.exploration_function(actions, self.Q[state],
                                                       self.temperature_function(self.trials), self.counter[state])
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
        return max(1, self.temperature_function(n))

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
