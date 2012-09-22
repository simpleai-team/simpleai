Local search algorithms
=======================

AIMA Book chapters recommended: 2 (Intelligent agents), 3 (Solving problems by searching), 4 (Beyond classical search)

The usage of the local search algorithms are **very** similar to the search algorithms explained on the :doc:`search` section, so you should start by reading that section and then come to this.

We will use the same example, detailing only the changes.

Differences on the problem class:
---------------------------------

To use local search you will have to implement a problem class just as the one you implemented for search algorithms (you can use the same, of course). The only differences will be this: 

* you **won't** need to implement the **is_goal** method, because local search algorithms check for states with "better values", and not for "goal states".

* you **must** implement a new method: **value**. This method receives a state, and returns a valuation ("score") of that value. Better states must have higher scores.

Example:

    def value(self, state):
        # how many correct letters there are?
        return sum(1 if state[i] == GOAL[i] else 0
                   for i in range(min(len(GOAL), len(state))))
