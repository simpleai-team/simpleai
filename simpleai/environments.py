# -*- coding: utf-8 -*-


class Environment(object):

    def __init__(self, agents, initial_state):
        self.agents = agents
        self.state = initial_state

    def run(self, steps=100):
        for step in xrange(steps):
            if self.is_completed(self.state):
                return
            self.step()

    def step(self):
        """This method evolves one step in time."""
        if not self.is_completed(self.state):
            for agent in self.agents:
                action = agent.program(self.percept(agent, self.state))
                self.state = self.do_action(self.state, action)

    def do_action(self, state, action):
        "Override this method to apply an action to a state and return a new state"
        raise NotImplementedError()

    def is_completed(self, state):
        "Override this method when the environment have terminal states"
        return False

    def percept(self, agent, state):
        "This method make agent's perception"
        return self.state

