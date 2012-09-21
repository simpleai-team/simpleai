Search algorithms
=================

AIMA Book chapters recommended: 2 (Intelligent agents), 3 (Solving problems by searching)

To solve a search problem using SimpleAI, you will first need to program the specifics of your particular search problem. To do this, we provide you with a Problem class that you will inherit and then populate with the problem specifics.

After you have your problem defined, you can call any of the search algorithms to find a solution to the problem (if exists).

We will use a very simple example to illustrate this, the example is the problem of constructing the "hello world" string.

Creating your problem
---------------------

("why would anybody want to create a problem?")

Your problem class will need to implement several methods, some of them depending on the algorithms you want to use.

You will always have to implement:

* **actions**: this method receives a state, and must return the list of actions that can be performed from that particular state.
* **result**: this method receives a state and an action, and must return the resulting state of applying that particular action from that particular state.
* **is_goal**: this method receives a state, and must return True if the state is a goal state, or False if don't.

Example:

    from simpleai.models import Problem

    GOAL = 'HELLO WORLD'

    class HelloProblem(Problem):
        def actions(self, state):
            if len(state) < len(GOAL):
                return [c for c in ' ABCDEFGHIJKLMNOPQRSTUVWXYZ']
            else:
                return []

        def result(self, state, action):
            return state + action

        def is_goal(self, state):
            return state == GOAL

if you want to use informed search algorithms (like A* or greedy search), then you will have to add an extra method to your class:

* **heuristic**: this method receives a state, and must return an integer value of the estimation of the remaining cost from that state to the solution. (remember, your heuristic must be admisible, refear to AIMA for more details on how to build heuristics).

On our example, we would add:

        def heuristic(self, state):
            # how far are we from the goal?
            wrong = sum([1 if state[i] != GOAL[i] else 0
                        for i in range(len(state))])
            missing = len(GOAL) - len(state)
            return wrong + missing

Finally, you have to create an instance of your problem to use it on the searching algorithms. The Problem class initializer receives one parameter: the initial_state from which the search will begin.

Example:

    my_problem = HelloProblem(initial_state='')
