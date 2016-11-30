from __future__ import print_function

from time import time

from copy import deepcopy

from simpleai.search import (
    backtrack, MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE,
    convert_to_binary, CspProblem)

variables = ('F', 'T', 'U', 'W', 'R', 'O', 'C_10', 'C_100', 'C_1000')

domains = dict((v, list(range(1, 10))) for v in variables)


def const_different(variables, values):
    return len(values) == len(set(values))  # remove repeated values and count

constraints = [
    (('F', 'T', 'U', 'W', 'R', 'O'), const_different),
    (('O', 'R', 'C_10'), lambda vars_, values: values[0] + values[0] == values[1] + 10 * values[2]),
    (('C_10', 'W', 'U', 'C_100'), lambda vars_, values: values[0] + values[1] + values[1] == values[2] + 10 * values[3]),
    (('C_100', 'T', 'O', 'C_1000'), lambda vars_, values: values[0] + values[1] + values[1] == values[2] + 10 * values[3]),
    (('C_1000', 'F'), lambda vars_, values: values[0] == values[1])
]

original_constraints = deepcopy(constraints)
original_domains = deepcopy(domains)

start = time()
problem = CspProblem(variables, original_domains, original_constraints)
result = backtrack(problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
elapsed = time() - start
print(result)
print("Took %d seconds to finish using n-ary constraints" % elapsed)


start = time()
variables, domains, constraints = convert_to_binary(variables, domains, constraints)
problem = CspProblem(variables, domains, constraints)
result = backtrack(problem, value_heuristic=LEAST_CONSTRAINING_VALUE)
elapsed = time() - start
print(result)
print("Took %d seconds to finish using binary constraints" % elapsed)
