Constraint satisfaction problems
================================

AIMA Book chapters recommended: 2 (Intelligent agents), 3 (Solving problems by searching), 4 (Beyond classical search), 6 (Constraint satisfaction problems)

SimpleAI provides you with a class that you will instantiate to represent your csp problems, and a few csp algorithms that you can use to find solutions for the csp problems.

Defining your problem
---------------------

You must simply create an instance of this class, specifying the variables, the variable domains, and the constraints as construction parameters:

* **variables** will be a tuple with the variable names. 
* **domains** will be a dictionary with the variable names as keys, and the domains as values (in the form of any iterable you want).
* **constraints** will be a list of tuples with two components each: a tuple with the variables involved on the constraint, and a reference to a function that checks the constraint. 

**FAQ** why not merge variables and domains on one single dict? Answer: because we need to preserve the order of the variables, and dicts don't have order. We could use an OrderedDict to solve this, but it's only present on python 2.7.

The constraint functions will receive two parameters to check the constraint: a variables tuple and a values tuple, both containing **only** the restricted variables and their values, and in the **same** order than the constrained variables tuple you provided. The function should return True if the values are "correct" (no constraint violation detected), or False if the constraint is violated (think this functions as answers to the question "can I use this values?").

We will illustrate with a simple example that tries to assign numbers to 3 variables (letters), but with a few restrictions.

Example:

    from simpleai.models import CspProblem

    variables = ('A', 'B', 'C')

    domains = {
        'A': [1, 2, 3],
        'B': [1, 3],
        'C': [1, 2],
    }

    # a constraint that expects different variables to have different values
    def const_different(variables, values):
        return len(values) == len(set(values))  # remove repeated values and count

    # a constraint that expects one variable to be bigger than other
    def const_one_bigger_other(variables, values):
        return values[0] > values[1]
        
    # a constraint thet expects two variables to be one odd and the other even, 
    # no matter which one is which type
    def const_one_odd_one_even(variables, values):
        if values[0] % 2 == 0:
            return values[1] % 2 == 1  # first even, expect second to be odd
        else:
            return values[1] % 2 == 0  # first odd, expect second to be even

    constraints = [
        (('A', 'B', 'C'), const_different),
        (('A', 'C'), const_one_bigger_other),
        (('A', 'C'), const_one_odd_one_even),
    ]

    my_problem = CspProblem(variables, domains, constraints)


Searching for solutions
-----------------------

Now, with your csp problem instantiated, you can call the csp search algorithms. They are located on the ``simpleai.csp`` package.

For example, if you want to use backtracking search, you would do:

    from simpleai.csp import backtrack

    # my_problem = ... (steps from the previous section)

    result = backtrack(problem)

And what will you receive on ``result``? You will receive a dictionary with the assigned values to the variables if a solution was found, or None if couldn't find a solution.

All the implemented algorithms have their docstring defined. In any python console you can just import them and ask for their help:

    help(backtrack)

The implemented algorithms are: ``backtrack``, ``min_conflicts``.

Using heuristics
----------------

TODO

Using constraint propagation (inference)
----------------------------------------

TODO
