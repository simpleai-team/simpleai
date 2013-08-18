# -*- coding: utf-8 -*-
from simpleai.machine_learning.reinforcement_learning import TD_QLearner, \
                                                             boltzmann_exploration, make_exponential_temperature
import random


class TicTacToePlayer(TD_QLearner):

    def __init__(self, play_with):
        super(TicTacToePlayer, self).__init__(exploration_function=boltzmann_exploration, discount_factor=0.9,
                                              temperature_function=make_exponential_temperature(1000000, 0.01))
        self.play_with = play_with
        self.other_play_with = 'X' if play_with == 'O' else 'O'

    def update_state(self, percept):
        state = percept.replace(self.play_with, '1')
        state = state.replace(self.other_play_with, '2')
        return state.replace('\n', '')

    def actions(self, state):
        'actions are index where we can make a move'
        actions = []
        for index, char in enumerate(state):
            if char == '_':
                actions.append(index)
        return actions


class HumanPlayer(TicTacToePlayer):

    def set_reward(self, reward, terminal=False):
        print ('reward:', reward)

    def step(self, perception):
        print ('Current board:')
        rows = perception.split()
        s = ['+-+-+-+-+', '| |0|1|2|', '+-+-+-+-+']
        for i, row in enumerate(rows):
            row = row.replace('_', ' ')
            s.append('|%d|' % i + '|'.join(list(row)) + '|')
            s.append('+-+-+-+-+')
        print (('\n'.join(s)))
        a = input('Make your move (r, c):')
        r, c = a
        return r * 3 + c


class RandomPlayer(TicTacToePlayer):

    def step(self, perception):
        return random.choice(self.actions(self.update_state(perception)))


class TicTacToeGame(object):

    def __init__(self, players):
        self.initial_state = '___\n___\n___'
        self.players = players
        self.current_state = self.initial_state

    def play(self):
        self.current_state = self.initial_state
        random.shuffle(self.players)
        current, other = self.players
        while not self.game_over(self.current_state):
            action = current.step(self.current_state)
            self.current_state = self.update_state(self.current_state, action, current)
            other_reward = self.score(self.current_state, other)
            terminal = self.game_over(self.current_state)
            other.set_reward(other_reward, terminal)

            current, other = other, current

        other_reward = self.score(self.current_state, other)
        other.set_reward(other_reward, True)

        if other_reward == 1:
            return other.play_with
        elif other_reward == -1:
            return current.play_with
        else:
            return 'Tie!'

    def update_state(self, state, action, player):
        s = state.replace('\n', '')
        s = s[:action] + player.play_with + s[action + 1:]
        return '\n'.join([s[0:3], s[3:6], s[6:9]])

    def game_over(self, state):
        return not ('_' in state and all([self.score(state, x) == 0 for x in self.players]))

    def score(self, state, player):
        rows = state.split()
        columns = [''.join(x) for x in zip(*rows)]
        diagonals = [rows[0][0] + rows[1][1] + rows[2][2], rows[0][2] + rows[1][1] + rows[2][0]]
        to_check = rows + columns + diagonals
        for x in to_check:
            if all([c == x[0] for c in x]) and x[0] != '_':
                if x[0] == player.play_with:
                    return 1
                else:
                    return -1
        return 0


def show_reward_evolution(*players):
    import numpy
    import pylab
    trials = numpy.arange(len(players[0].accumulated_rewards))
    for player in players:
        pylab.plot(trials, numpy.array(player.accumulated_rewards), label=player.play_with)
    pylab.legend()
    pylab.xlabel('Trials')
    pylab.ylabel(u'Accumulated reward')
    pylab.title(u'Accumulated reward')
    pylab.grid(True)
    pylab.show()


if __name__ == '__main__':
    a = TicTacToePlayer('X')
    b = RandomPlayer('O')
    c = HumanPlayer('O')
    game = TicTacToeGame([a, b])
    ## train
    print ('Training, please wait...')
    game.players = [a, b]
    for i in range(30000):
        game.play()
    show_reward_evolution(a, b)
    #play again with a human...
    game.players = [a, c]
    print game.current_state
    print ('And the winner is...' + game.play())
