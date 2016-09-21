# -*- coding: utf-8 -*-

from __future__ import print_function

from simpleai.machine_learning.reinforcement_learning import TDQLearner, RLProblem, \
                                                             make_exponential_temperature, \
                                                             PerformanceCounter
import random
from simpleai.environments import RLEnvironment


class TicTacToeProblem(RLProblem):

    def actions(self, state):
        'actions are index where we can make a move'
        actions = []
        for index, char in enumerate(state):
            if char == '_':
                actions.append(index)
        return actions

    def update_state(self, percept, agent):
        state = percept.replace(agent.play_with, '1')
        state = state.replace(agent.other_play_with, '2')
        return state.replace('\n', '')


class TicTacToePlayer(TDQLearner):

    def __init__(self, play_with):
        super(TicTacToePlayer, self).__init__(TicTacToeProblem(),
                                              temperature_function=make_exponential_temperature(1000000, 0.01),
                                              discount_factor=0.4)
        self.play_with = play_with
        self.other_play_with = 'X' if play_with == 'O' else 'O'


class HumanPlayer(TicTacToePlayer):

    def set_reward(self, reward, terminal=False):
        print(('reward:', reward))

    def program(self, perception):
        print('Current board:')
        rows = perception.split()
        s = ['+-+-+-+-+', '| |0|1|2|', '+-+-+-+-+']
        for i, row in enumerate(rows):
            row = row.replace('_', ' ')
            s.append('|%d|' % i + '|'.join(list(row)) + '|')
            s.append('+-+-+-+-+')
        print(('\n'.join(s)))
        a = input('Make your move (r, c):')
        r, c = a
        return r * 3 + c


class RandomPlayer(TicTacToePlayer):

    def program(self, perception):
        try:
            return random.choice(self.problem.actions(self.problem.update_state(perception, self)))
        except:
            return None


class TicTacToeGame(RLEnvironment):

    def __init__(self, agents):
        super(TicTacToeGame, self).__init__(agents, '___\n___\n___')

    def do_action(self, state, action, agent):
        if action is not None:
            s = state.replace('\n', '')
            s = s[:action] + agent.play_with + s[action + 1:]
            return '\n'.join([s[0:3], s[3:6], s[6:9]])
        return state

    def is_completed(self, state):
        return not ('_' in state and all([self.reward(state, x) == 0 for x in self.agents]))

    def reward(self, state, agent):
        rows = state.split()
        columns = [''.join(x) for x in zip(*rows)]
        diagonals = [rows[0][0] + rows[1][1] + rows[2][2], rows[0][2] + rows[1][1] + rows[2][0]]
        to_check = rows + columns + diagonals
        for x in to_check:
            if all([c == x[0] for c in x]) and x[0] != '_':
                if x[0] == agent.play_with:
                    return 1
                else:
                    return -1
        return 0


if __name__ == '__main__':
    a = TicTacToePlayer('X')
    b = RandomPlayer('O')
    c = HumanPlayer('O')
    game = TicTacToeGame([a, b])
    print('Training with a random player, please wait...')
    game.agents = [a, b]
    for i in range(3000):
        game.run()

    a.dump('qlearner_agent')

    d = TicTacToePlayer.load('qlearner_agent')
    d.play_with = 'O'

    game.agents = [a, d]
    per = PerformanceCounter(game.agents, ['QLearnerA', 'QLearnerD'])
    for i in range(3000):
        game.run()
    per.show_statistics()

    game.agents = [a, c]
    print('Do you like to play?')
    game.run()
    print(game.state)
