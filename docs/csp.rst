Constraint satisfaction problems
================================

**Is strongly recommended to have knowledge of CSP problems. You can learn about then on the AIMA book, 3rd edition, chapter 6.**

SimpleAI provides you with a class that you will instantiate to represent your csp problems, and a few csp algorithms that you can use to find solutions for the csp problems.

You must simply create an instance of this class, specifying both the variables (with their domains) and the constraints as construction parameters.

The variables will be a dictionary with the variable names as keys, and their domains as values (in the form of any iterable you want). The constraints will be a list of tuples with two components each: a tuple with the variables involved on the constraint, and a reference to a function that checks the constraint. 

The constraint functions will receive two parameters to check the constraint: a variables tuple and a values tuple, both containing **only** the restricted variables and their values, and in the **same** order than the constrained variables tuple you provided. The function should return True if the values are "correct" (no constraint violation detected), or False if the constraint is violated (think this functions as answers to the question "can I use this values?").

Example:

    from simpleai.models import CspProblem

    variables = {
        'A': [1, 2, 3],
        'B': [1, 3],
        'C': [1, 2],
    }

    # a constraint that expects different variables to have different values
    def const_different(variables, values):
        return values[0] != values[1] != values[2]

    # a constraint that expects A to be bigger than C
    def const_a_bigger_c(variables, values):
        return values[0] > values[1]
        
    # a constraint thet expects A to be odd
    def const_a_is_odd(variables, values)
        return values[0] % 2 == 0

    constraints = [
        (('A', 'B', 'C'), const_different)
        (('A', 'C'), const_a_bigger_c)
        (('A',), const_a_is_odd)
    ]

    my_problem = CspProblem(variables, constraints)


