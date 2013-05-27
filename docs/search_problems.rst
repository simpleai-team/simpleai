Search algorithms
=================

*AIMA Book chapters recommended: 2 (Intelligent agents), 3 (Solving problems by searching)*

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

.. code-block:: python

    from simpleai.search import SearchProblem

    GOAL = 'HELLO WORLD'


    class HelloProblem(SearchProblem):
        def actions(self, state):
            if len(state) < len(GOAL):
                return list(' ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            else:
                return []

        def result(self, state, action):
            return state + action

        def is_goal(self, state):
            return state == GOAL

if you want to use search algorithms that consider the cost of actions on their logic (like uniform cost search), then you will have to implement an extra method in your class:

* **cost**: this methods receives two states and an action, and must return the cost of applying the action from the first state to the seccond state.

Example:

.. code-block:: python

    def cost(self, state, action, state2):
        return 1

if you want to use informed search algorithms (like A* or greedy search), then you will have to add another extra method:

* **heuristic**: this method receives a state, and must return an integer value of the estimation of the remaining cost from that state to the solution. (remember, your heuristic must be admisible, refear to AIMA for more details on how to build heuristics).

On our example, we would add:

.. code-block:: python

        def heuristic(self, state):
            # how far are we from the goal?
            wrong = sum([1 if state[i] != GOAL[i] else 0
                        for i in range(len(state))])
            missing = len(GOAL) - len(state)
            return wrong + missing

Finally, you have to create an instance of your problem to use it on the searching algorithms. The Problem class initializer receives one parameter: the initial_state from which the search will begin.

Example:

.. code-block:: python

    my_problem = HelloProblem(initial_state='')


Searching for solutions
-----------------------

Now, with your problem defined and instantiated, you can call any of the search algorithms. The classic search algorithms are located on the ``simpleai.search`` package.

For example, if you want to use breadth first search, you would do:

.. code-block:: python

    from simpleai.search import breadth_first

    # class HelloProblem..., my_problem = ... (steps from the previous section)

    result = breadth_first(my_problem)

And what will you receive on ``result``? You will receive the soultion node from the search tree if a solution was found, or None if couldn't find a solution. A solution node has this notable attributes:

.. code-block:: python

    result.state  # the goal state
    result.path()  # the path from the initial state to the goal state

All the implemented algorithms have their docstring defined with the parameters they receive and the methods from Problem they require. In any python console you can just import them and ask for their help:

.. code-block:: python

    help(breadth_first)

**IMPORTANT**: when using ``graph_search=True`` on this methods, your states must be python inmutable values to be able to have an indexed memory of visited states. So you should use strings, numbers, inmutable tuples (composed by inmutable values), or a custom class that implements the necessary to be inmutable.

The implemented algorithms are:

.. automodule:: simpleai.search.traditional
   :members:
