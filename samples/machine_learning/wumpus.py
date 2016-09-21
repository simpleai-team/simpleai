# -*- coding: utf-8 -*-

from __future__ import print_function

from simpleai.machine_learning.reinforcement_learning import TDQLearner, \
                                                             make_exponential_temperature, \
                                                             PerformanceCounter, \
                                                             RLProblem
from simpleai.environments import RLEnvironment
import threading
try:
    from Tkinter import *
except ImportError:
    from tkinter import *


class PerpetualTimer(threading._Timer):

    def __init__(self, interval, function, name=None, daemon=False,
                    args=(), kwargs={}):
        super(PerpetualTimer, self).__init__(interval, function, args, kwargs)
        self.setName(name)
        self.setDaemon(daemon)

    def run(self):
        while True:
            self.finished.wait(self.interval)
            if self.finished.isSet():
                return
            self.function(*self.args, **self.kwargs)

    def stop(self, timeout=None):
        self.cancel()
        self.join(timeout)

    def callback(egg):
        egg.cook()


class WumpusViewer(object):

    def __init__(self, environment):
        self.environment = environment
        root = Tk()
        w = Canvas(root, width=400, height=400)
        self.w = w
        w.pack()

        w.create_polygon(0, 0, 0, 400, 400, 400, 400, 0, fill='white')
        for x in range(4):
            w.create_line(100 * x, 0, 100 * x, 400)
            w.create_line(0, 100 * x, 400, 100 * x)

        #make holes
        for x, y in environment.holes:
            w.create_oval(*self._coord(x, y), fill='red')

        #make wumpus
        x, y = environment.wumpus
        w.create_oval(*self._coord(x, y), fill='blue')

        #make agent
        x, y, have_gold = environment.state
        self.agent = w.create_oval(*self._coord(x, y), fill='green')

        #make gold
        x, y = environment.gold
        self.gold = w.create_oval(*self._coord(x, y), fill='yellow')

        frame = Frame(root)
        frame.pack()

        self.start = Button(frame, text="Start", command=self.start)
        self.start.pack(side=LEFT)
        self.stop = Button(frame, text="Stop", command=self.stop)
        self.stop.pack(side=LEFT)

        root.mainloop()

    def _coord(self, x, y):
        y = 5 - y
        cx = 100 * (x - 1) + 50
        cy = 100 * (y - 1) + 50
        r = 30
        return (cx - r, cy - r, cx + r, cy + r)

    def step(self):
        if self.environment.is_completed(self.environment.state):
            self.timer.cancel()
        else:
            self.environment.step(viewer=self)

    def start(self):
        self.timer = PerpetualTimer(0.5, self.step)
        self.timer.start()
        self.environment.state = self.environment.initial_state

    def stop(self):
        self.timer.cancel()

    def event(self, state1, action, state2, agent):
        print('action: %s state: %s' % (action, str(state2)))
        x, y, have_gold = state2
        if have_gold and self.gold:
            self.w.delete(self.gold)
            self.w.itemconfig(self.agent, outline="yellow", width=6.0)
        self.w.coords(self.agent, self._coord(x, y))


class WumpusEnvironment(RLEnvironment):

    def __init__(self, agent):
        super(RLEnvironment, self).__init__([agent], (1, 1, False))
        self.action_dict = {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'rigth': (1, 0)}
        self.wumpus = (1, 3)
        self.holes = [(3, 1), (3, 3), (4, 4)]
        self.gold = (3, 4)
        self.threats = [self.wumpus] + self.holes

        self.rewards = {(1, 1, True): 10}
        for c, r in self.threats:
            self.rewards[(c, r, True)] = -10
            self.rewards[(c, r, False)] = -10

    def do_action(self, state, action, agent):
        c1, r1, have_gold = state
        c2, r2 = self.action_dict[action]
        rn = r1 + r2
        cn = c1 + c2
        if not have_gold and (cn, rn) == self.gold:
            have_gold = True
        _next = (cn, rn, have_gold)
        if (1 <= rn <= 4) and (1 <= cn <= 4):
            return _next
        return state

    def is_completed(self, state):
        return state in list(self.rewards.keys())

    def reward(self, state, agent):
        return self.rewards.get(state, -0.08)


class WumpusProblem(RLProblem):

    def actions(self, state):
        actions = ['up', 'down', 'left', 'rigth']
        return actions


if __name__ == '__main__':
    agent = TDQLearner(WumpusProblem(),
                       temperature_function=make_exponential_temperature(1000, 0.01),
                       discount_factor=0.8)
    game = WumpusEnvironment(agent)

    p = PerformanceCounter([agent], ['Q-learner Agent'])

    print('Training...')
    for i in range(10000):
        game.run()

    p.show_statistics()
    game.run(viewer=WumpusViewer(game))


