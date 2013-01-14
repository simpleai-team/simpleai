Local search algorithms
=======================

*AIMA Book chapters recommended: 2 (Intelligent agents), 3 (Solving problems by searching), 4 (Beyond classical search)*

The usage of the local search algorithms are **very** similar to the search algorithms explained on the :doc:`search_problems` section, so you should start by reading that section and then come to this.

We will use the same example, detailing only the changes.

Differences on the problem class
--------------------------------

To use local search you will have to implement a problem class just as the one you implemented for search algorithms (you can use the same, of course). The only differences will be this: 

* you **won't** need to implement the **is_goal** method, because local search algorithms check for states with "better values", and not for "goal states".

* you **must** implement a new method called **value**: This method receives a state, and returns a valuation ("score") of that value. Better states must have higher scores.

Example:

.. code-block:: python

    # class Problem...

        def value(self, state):
            # how many correct letters there are?
            return sum(1 if state[i] == GOAL[i] else 0
                       for i in range(min(len(GOAL), len(state))))

For algorithms that require generation of random initial states (like hill climbing with random restarts, or genetic search), you must define a new method:

* **generate_random_state**: this method receives nothing, and must return a randomly generated state.

Example:

.. code-block:: python

    import random

    # class Problem...

        def generate_random_state(self):
            # generate a random initial string
            # note that with this example, not always we will find a solution
            letters = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            return random.choice(letters)


Special case: genetic search
----------------------------

For the genetic search algorithm, your problem will be quite different from the search and local search problems. In this case it must only define the following methods:

* **generate_random_state**: same as explained before, but notice that in this case, the generated random state must be **complete**, because genetic algorithms require that.

* **crossover**: this method receives two (complete) states, and must return a new state as a result of "crossing" both parent states (the resulting state must be complete too).

Example:

.. code-block:: python

    import random

    # class Problem...

        def crossover(self, state1, state2):
            # cross both strings, at a random point
            cut_point = random.randint(0, len(GOAL))
            child = state1[:cut_point] + state2[cut_point:]
            return child

* **mutate**: this method receives a (complete) state, and must return a new (also complete) state as result of generating a random mutation on the original state.

Example:

.. code-block:: python

    import random

    # class Problem...

        def mutate(self, state):
            # cross both strings, at a random point
            mutation = random.choice(' ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            mutation_point = random.randint(0, len(GOAL))
            mutated = ''.join([state[i] if i != mutation_point else mutation
                               for i in range(len(state))])
            return mutated

* **value**: same as the other local search algorithms.


Searching for solutions
-----------------------

This works exactly as for search algorithms.

They have help like the search algorithms, and return the same type of result.

The implemented local search algorithms are:

.. automodule:: simpleai.search.local
   :members:
