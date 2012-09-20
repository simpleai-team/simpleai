# coding=utf-8
from copy import deepcopy


MOST_CONSTRAINED_VARIABLE = 'mcv'
HIGHEST_DEGREE_VARIABLE = 'degree'
LEAST_CONSTRAINING_VALUE = 'lvc'


def backtrack(csp_problem, variable_heuristic='', value_heuristic=''):
    assignment = {}
    domains = deepcopy(csp_problem.domains)

    if variable_heuristic == MOST_CONSTRAINED_VARIABLE:
        variable_chooser = _most_constrained_variable_chooser
    elif variable_heuristic == HIGHEST_DEGREE_VARIABLE:
        variable_chooser = _highest_degree_variable_chooser
    else:
        variable_chooser = _basic_variable_chooser

    if value_heuristic == LEAST_CONSTRAINING_VALUE:
        values_sorter = _least_constraining_values_sorter
    else:
        values_sorter = _basic_values_sorter

    return _backtracking(csp_problem,
                         assignment,
                         domains,
                         variable_chooser,
                         values_sorter)


def _basic_variable_chooser(problem, variables, domains):
    return variables[0]


def _most_constrained_variable_chooser(problem, variables, domains):
    # the variable with fewer values available
    return sorted(variables, key=lambda v: len(domains[v]))[0]


def _highest_degree_variable_chooser(problem, variables, domains):
    # the variable involved in more constraints
    return sorted(variables, key=lambda v: problem.var_degrees[v], reverse=True)[0]


def _count_conflicts(problem, assignment, variable, value):
    conflicts = 0
    new_assignment = deepcopy(assignment)
    new_assignment[variable] = value

    for neighbors, constraint in problem.var_contraints[variable]:
        # if all the neighbors on the constraint have values, check if conflict
        if all(n in new_assignment for n in neighbors):
            variables, values = zip(*[(n, new_assignment[n])
                                      for n in neighbors])
            if not constraint(variables, values):
                conflicts += 1

    return conflicts


def _basic_values_sorter(problem, variable, domains):
    return domains[variable][:]


def _least_constraining_values_sorter(problem, variable, domains):
    # the value that generates less conflicts
    values = sorted(domains[variable][:],
                    key=lambda v: _count_conflicts(variable, v))
    return values


def _backtracking(problem, assignment, domains, variable_chooser,
                  values_sorter):
    if len(assignment) == len(problem.variables):
        return assignment

    pending = [v for v in problem.variables
               if v not in assignment]
    variable = variable_chooser(problem, pending, domains)

    values = values_sorter(problem, variable, domains)

    for value in values:
        if not _count_conflicts(problem, assignment, variable, value): # TODO on aima also checks if using fc
            new_assignment = deepcopy(assignment)
            new_domains = deepcopy(domains)

            new_assignment[variable] = value

            # TODO propagation and inferences

            return _backtracking(problem,
                                 new_assignment,
                                 new_domains,
                                 variable_chooser,
                                 values_sorter)

    return None
