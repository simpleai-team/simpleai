# coding=utf-8
from copy import deepcopy


MOST_CONSTRAINED_VARIABLE = 'mcv'
HIGHEST_DEGREE_VARIABLE = 'degree'
LEAST_CONSTRAINING_VALUE = 'lvc'


def backtrack(problem, variable_heuristic='', value_heuristic=''):
    assignment = {}
    domains = deepcopy(problem.domains)

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

    return _backtracking(problem,
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


def _count_conflicts(problem, assignment, variable=None, value=None):
    if variable and value:
        assignment = deepcopy(assignment)
        assignment[variable] = value

    conflicts = 0
    for neighbors, constraint in problem.constraints:
        # if all the neighbors on the constraint have values, check if conflict
        if all(n in assignment for n in neighbors):
            variables, values = zip(*[(n, assignment[n])
                                      for n in neighbors])
            if not constraint(variables, values):
                conflicts += 1

    return conflicts


def _basic_values_sorter(problem, assignment, variable, domains):
    return domains[variable][:]


def _least_constraining_values_sorter(problem, assignment, variable, domains):
    # the value that generates less conflicts
    def update_assignment(value):
        new_assignment = deepcopy(assignment)
        new_assignment[variable] = value
        return new_assignment

    values = sorted(domains[variable][:],
                    key=lambda v: _count_conflicts(problem, assignment, variable, v))
    return values


def _backtracking(problem, assignment, domains, variable_chooser,
                  values_sorter):
    if len(assignment) == len(problem.variables):
        return assignment

    pending = [v for v in problem.variables
               if v not in assignment]
    variable = variable_chooser(problem, pending, domains)

    values = values_sorter(problem, assignment, variable, domains)

    for value in values:
        new_assignment = deepcopy(assignment)
        new_assignment[variable] = value

        if not _count_conflicts(problem, new_assignment): # TODO on aima also checks if using fc
            new_domains = deepcopy(domains)

            # TODO propagation and inferences

            return _backtracking(problem,
                                 new_assignment,
                                 new_domains,
                                 variable_chooser,
                                 values_sorter)

    return None
