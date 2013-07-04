from StringIO import StringIO
from string import uppercase
from itertools import combinations
from collections import OrderedDict

from simpleai.search import (
    CspProblem, backtrack, min_conflicts,
    MOST_CONSTRAINED_VARIABLE, HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE)

from simpleai.search.arc import arc_concistency_3


variables = ["%s%d" % (i, j) for i in uppercase[:9] for j in xrange(1, 10)]

domains = OrderedDict((v, range(1, 10)) for v in variables)


def const_different(variables, values):
    return values[0] != values[1]  # expect the value of the neighbors to be different

sodoku = \
"""
  3 2 6
9  3 5  1
  18 64
  81 29
7       8
  67 82
  26 95
8  2 3  9
  5 1 3
"""


def parsepuzzle(puzzle):
    sodoku_lines = map(lambda s: s.rstrip("\n"), StringIO(puzzle).readlines()[1:])
    domains = {}

    for k, i in enumerate(uppercase[:9]):
        for j in xrange(1, 10):
            line = sodoku_lines[k]
            if len(line) <= (j - 1):
                continue
            val = line[j - 1]
            if val != ' ':
                var = "%s%d" % (i, j)
                domains[var] = [int(val)]

    return domains


def mkconstraints():
    constraints = []

    for j in xrange(1, 10):
        vars = ["%s%d" % (i, j) for i in uppercase[:9]]
        constraints.extend((c, const_different) for c in combinations(vars, 2))

    for i in uppercase[:9]:
        vars = ["%s%d" % (i, j) for j in xrange(1, 10)]
        constraints.extend((c, const_different) for c in combinations(vars, 2))

    for b0 in ['ABC', 'DEF', 'GHI']:
        for b1 in [[1, 2, 3], [4, 5, 6], [7, 8, 9]]:
            vars = ["%s%d" % (i, j) for i in b0 for j in b1]
            l = list((c, const_different) for c in combinations(vars, 2))
            constraints.extend(l)

    return constraints


def display_solution(sol):
    for i in uppercase[:9]:
        print "|".join([str(sol["%s%d" % (i, j)]) for j in xrange(1, 10)])
        print "-|-|-|-|-|-|-|-|-"

constraints = mkconstraints()
domains.update(parsepuzzle(sodoku))

#arc_concistency_3(domains, constraints)
my_problem = CspProblem(variables, domains, constraints)
sol = backtrack(my_problem)
display_solution(sol)


# sol = backtrack(my_problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
# display_solution(sol)

# print backtrack(my_problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE)
# print backtrack(my_problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE)
# print backtrack(my_problem, value_heuristic=LEAST_CONSTRAINING_VALUE)
# print backtrack(my_problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
# print backtrack(my_problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
# print min_conflicts(my_problem)
