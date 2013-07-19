# coding=utf-8


class SearchProblem(object):
    '''Abstract base class to represent and manipulate the search space of a
       problem.
       In this class, the search space is meant to be represented implicitly as
       a graph.
       Each state corresponds with a problem state (ie, a valid configuration)
       and each problem action (ie, a valid transformation to a configuracion)
       corresponds with an edge.

       To use this class you should implement the methods required by the search
       algorithm you will use.
       '''

    def __init__(self, initial_state=None):
        self.initial_state = initial_state

    def actions(self, state):
        '''Returns the actions available to perform from `state`.
           The returned value is an iterable over actions.
           Actions are problem-specific and no assumption should be made about
           them.
        '''
        raise NotImplementedError

    def result(self, state, action):
        '''Returns the resulting state of applying `action` to `state`.'''
        raise NotImplementedError

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        return 1

    def is_goal(self, state):
        '''Returns `True` if `state` is a goal state and `False` otherwise'''
        raise NotImplementedError

    def value(self, state):
        '''Returns the value of `state` as it is needed by optimization
           problems.
           Value is a number (integer or floating point).'''
        raise NotImplementedError

    def heuristic(self, state):
        '''Returns an estimate of the cost remaining to reach the solution
           from `state`.'''
        return 0

    def crossover(self, state1, state2):
        """
        Crossover method for genetic search. It should return a new state that
        is the 'mix' (somehow) of `state1` and `state2`.
        """
        raise NotImplementedError

    def mutate(self, state):
        """
        Mutation method for genetic search. It should return a new state that
        is a slight random variation of `state`.
        """
        raise NotImplementedError

    def generate_random_state(self):
        """
        Generates a random state for genetic search. It's mainly used for the
        seed states in the initilization of genetic search.
        """
        raise NotImplementedError

    def state_representation(self, state):
        """
        Returns a string representation of a state.
        By default it returns str(state).
        """
        return str(state)

    def action_representation(self, action):
        """
        Returns a string representation of an action.
        By default it returns str(action).
        """
        return str(action)


class SearchNode(object):
    '''Node of a search process.'''

    def __init__(self, state, parent=None, action=None, cost=0, problem=None,
                 depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.problem = problem or parent.problem
        self.depth = depth

    def expand(self, local_search=False):
        '''Create successors.'''
        new_nodes = []
        for action in self.problem.actions(self.state):
            new_state = self.problem.result(self.state, action)
            cost = self.problem.cost(self.state,
                                     action,
                                     new_state)
            nodefactory = self.__class__
            new_nodes.append(nodefactory(state=new_state,
                                         parent=None if local_search else self,
                                         problem=self.problem,
                                         action=action,
                                         cost=self.cost + cost,
                                         depth=self.depth + 1))
        return new_nodes

    def path(self):
        '''Path (list of nodes and actions) from root to this node.'''
        node = self
        path = []
        while node:
            path.append((node.action, node.state))
            node = node.parent
        return list(reversed(path))

    def __eq__(self, other):
        return isinstance(other, SearchNode) and self.state == other.state

    def state_representation(self):
        return self.problem.state_representation(self.state)

    def action_representation(self):
        return self.problem.action_representation(self.action)

    def __repr__(self):
        return 'Node <%s>' % self.state_representation().replace('\n', ' ')


class SearchNodeCostOrdered(SearchNode):
    def __lt__(self, other):
        return self.cost < other.cost


class SearchNodeValueOrdered(SearchNode):
    def __init__(self, *args, **kwargs):
        super(SearchNodeValueOrdered, self).__init__(*args, **kwargs)
        self.value = self.problem.value(self.state)

    def __lt__(self, other):
        # value must work inverted, because heapq sorts 1-9
        # and we need 9-1 sorting
        return -self.value < -other.value


class SearchNodeHeuristicOrdered(SearchNode):
    def __init__(self, *args, **kwargs):
        super(SearchNodeHeuristicOrdered, self).__init__(*args, **kwargs)
        self.heuristic = self.problem.heuristic(self.state)

    def __lt__(self, other):
        return self.heuristic < other.heuristic


class SearchNodeStarOrdered(SearchNodeHeuristicOrdered):
    def __lt__(self, other):
        return self.heuristic + self.cost < other.heuristic + other.cost


class CspProblem(object):
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

        # variable-based constraints dict
        self.var_contraints = dict([(v, [constraint
                                         for constraint in constraints
                                         if v in constraint[0]])
                                    for v in variables])

        # calculate degree of each variable
        self.var_degrees = dict([(v, len(self.var_contraints[v]))
                                 for v in variables])
