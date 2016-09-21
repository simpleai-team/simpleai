from __future__ import print_function

from simpleai.search import backtrack, CspProblem, convert_to_binary

variables = ('A', 'B', 'C')

domains = {
    'A': [1, 2, 3],
    'B': [1, 3, 4],
    'C': [1, 2],
}


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


# a constraint that requires one variable to be different than 1
def const_not_1(variables, values):
    return values[0] != 1

constraints = [
    (('A', 'B', 'C'), const_different),
    (('A', 'C'), const_one_bigger_other),
    (('A', 'C'), const_one_odd_one_even),
    (('A',), const_not_1)
]

variables, domains, constraints = convert_to_binary(variables, domains, constraints)
problem = CspProblem(variables, domains, constraints)
result = backtrack(problem)
print(result)
# result, {'A':2, 'B': 3, 'C': 1})
