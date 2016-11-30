# -*- coding: utf-8 -*-


class Environment(object):

    def __init__(self, agents, initial_state):
        self.agents = agents
        self.initial_state = initial_state
        self.state = initial_state

    def run(self, steps=10000, viewer=None):
        self.state = self.initial_state
        for step in range(steps):
            if self.is_completed(self.state):
                return
            self.step(viewer=viewer)

    def step(self, viewer=None):
        "This method evolves one step in time"
        if not self.is_completed(self.state):
            for agent in self.agents:
                action = agent.program(self.percept(agent, self.state))
                next_state = self.do_action(self.state, action, agent)
                if viewer:
                    viewer.event(self.state, action, next_state, agent)
                self.state = next_state
                if self.is_completed(self.state):
                    return

    def do_action(self, state, action, agent):
        "Override this method to apply an action performed by an agent to a state and return a new state"
        raise NotImplementedError()

    def is_completed(self, state):
        "Override this method when the environment have terminal states"
        return False

    def percept(self, agent, state):
        "This method make agent's perception"
        return self.state


class RLEnvironment(Environment):

    def __init__(self, agents, initial_state):
        super(RLEnvironment, self).__init__(agents, initial_state)

    def step(self, viewer=None):
        super(RLEnvironment, self).step(viewer)
        for agent in self.agents:
            agent.set_reward(self.reward(self.state, agent), self.is_completed(self.state))

    def reward(self, state, agent):
        raise NotImplementedError()

