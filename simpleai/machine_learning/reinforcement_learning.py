# -*- coding: utf-8 -*-
from collections import defaultdict, Counter
import math
import random
from simpleai.search.utils import argmax
import pickle
try:
    import matplotlib.pyplot as plt
    import numpy
except:
    plt = None  # lint:ok
    numpy = None  # lint:ok


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


class PerformanceCounter(object):

    def __init__(self, learners, names=None):
        self.learners = learners
        for i, learner in enumerate(learners):
            self.update_set_reward(learner)
            learner.accumulated_rewards = []
            learner.known_states = []
            learner.temperatures = []
            if names is None:
                learner.name = 'Learner %d' % i
            else:
                learner.name = names[i]

    def update_set_reward(self, learner):
        def set_reward(reward, terminal=False):
            if terminal:
                if len(learner.accumulated_rewards) > 0:
                    learner.accumulated_rewards.append(learner.accumulated_rewards[-1] + reward)
                else:
                    learner.accumulated_rewards.append(reward)
                learner.known_states.append(len(learner.Q))
                learner.temperatures.append(learner.temperature_function(learner.trials))
            learner.old_set_reward(reward, terminal)
        learner.old_set_reward = learner.set_reward
        learner.set_reward = set_reward

    def _make_plot(self, ax, data_name):
        for learner in self.learners:
            data = numpy.array(getattr(learner, data_name))
            ax.plot(numpy.arange(len(data)), data, label=learner.name)
        nice_name = data_name.replace('_', ' ').capitalize()
        ax.set_title(nice_name)
        ax.legend()

    def show_statistics(self):
        f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
        self._make_plot(ax1, 'accumulated_rewards')
        self._make_plot(ax2, 'known_states')
        self._make_plot(ax3, 'temperatures')
        plt.show()


class RLProblem(object):

    def actions(self, state):
        '''Returns the actions available to perform from `state`.
           The returned value is an iterable over actions.
        '''
        raise NotImplementedError()

    def update_state(self, percept, agent):
        'Override this method if you need to clean perception to a given agent'
        return percept


def inverse(n):
    if n == 0:
        return 1
    return 1.0 / n


def state_default():
    return defaultdict(int)


class QLearner(object):

    def __init__(self, problem, temperature_function=inverse,
                 discount_factor=1,
                 exploration_function=boltzmann_exploration,
                 learning_rate=inverse):

        self.Q = defaultdict(state_default)
        self.problem = problem
        self.discount_factor = discount_factor
        self.temperature_function = temperature_function
        self.exploration_function = exploration_function
        self.learning_rate = learning_rate

        self.last_state = None
        self.last_action = None
        self.last_reward = None
        self.counter = defaultdict(Counter)
        self.trials = 0

    def set_reward(self, reward, terminal=False):
        self.last_reward = reward
        if terminal:
            self.trials += 1
            self.Q[self.last_state][self.last_action] = reward

    def program(self, percept):
        s = self.last_state
        a = self.last_action

        state = self.problem.update_state(percept, self)
        actions = self.problem.actions(state)

        if len(actions) > 0:
            current_action = self.exploration_function(actions, self.Q[state],
                                                       self.temperature_function(self.trials),
                                                       self.counter[state])
        else:
            current_action = None

        if s is not None and current_action:
            self.counter[s][a] += 1
            self.update_rule(s, a, self.last_reward, state, current_action)

        self.last_state = state
        self.last_action = current_action
        return current_action

    def update_rule(self, s, a, r, cs, ca):
        raise NotImplementedError

    def dump(self, path):
        self.temperature_function = inverse
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)


class TDQLearner(QLearner):

    def update_rule(self, s, a, r, cs, ca):
        lr = self.learning_rate(self.counter[s][a])
        self.Q[s][a] += lr * (r + self.discount_factor * max(self.Q[cs].values()) - self.Q[s][a])


class SARSALearner(QLearner):

    def update_rule(self, s, a, r, cs, ca):
        lr = self.learning_rate(self.counter[s][a])
        self.Q[s][a] += lr * (r + self.discount_factor * self.Q[cs][ca] - self.Q[s][a])

