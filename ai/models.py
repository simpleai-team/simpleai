# coding=utf-8


class Problem(object):
    '''Logic of a problem.'''

    def __init__(self, initial_state):
        self.initial_state = initial_state

    def actions(self, state):
        '''Returns the list of actions available from a state.'''
        return []

    def result(self, state, action):
        '''Returns the resulting state of applying an action to a state.'''
        return None

    def cost(self, state, action, state2):
        '''Returns the cost of applying an action from state to state2.'''
        return 1

    def is_goal(self, state):
        '''Checks if a state is goal.'''
        return False


class SearchNode(object):
    '''Node of a search process.'''

    def __init__(self, state, parent=None, action=None, cost=0, problem=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.problem = problem or parent.problem

    def expand(self):
        '''Create successors.'''
        new_nodes = []
        for action in self.problem.actions(self.state):
            new_state = self.problem.result(self.state, action)
            cost = self.problem.cost(self.state,
                                     action,
                                     new_state)
            new_nodes.append(SearchNode(state=new_state,
                                        parent=self,
                                        cost=cost,
                                        problem=self.problem))
        return new_nodes

    def has_goal_state(self):
        '''Check if the state is goal.'''
        return self.problem.is_goal(self.state)

    def path(self):
        '''Path (list of nodes and actions) from root to this node.'''
        node = self
        path = []
        while node:
            path.append((node.action, node.state))
            node = node.parent

        return list(reversed(path))

    def __hash__(self):
        return hash(self.state)
