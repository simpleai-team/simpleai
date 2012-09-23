# coding=utf-8
import random
from copy import deepcopy


MOST_CONSTRAINED_VARIABLE = 'mcv'
HIGHEST_DEGREE_VARIABLE = 'degree'
LEAST_CONSTRAINING_VALUE = 'lvc'


def backtrack(problem, variable_heuristic='', value_heuristic=''):
    '''
    Backtracking search.

    variable_heuristic is the heuristic for variable choosing, can be
    MOST_CONSTRAINED_VARIABLE, HIGHEST_DEGREE_VARIABLE, or blank for simple
    ordered choosing.
    value_heuristic is the heuristic for value choosing, can be
    LEAST_CONSTRAINING_VALUE or blank for simple ordered choosing.
    '''
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
    '''
    Choose the next variable in order.
    '''
    return variables[0]


def _most_constrained_variable_chooser(problem, variables, domains):
    '''
    Choose the variable that has less available values.
    '''
    # the variable with fewer values available
    return sorted(variables, key=lambda v: len(domains[v]))[0]


def _highest_degree_variable_chooser(problem, variables, domains):
    '''
    Choose the variable that is involved on more constraints.
    '''
    # the variable involved in more constraints
    return sorted(variables, key=lambda v: problem.var_degrees[v], reverse=True)[0]


def _count_conflicts(problem, assignment, variable=None, value=None):
    '''
    Count the number of violated constraints on a given assignment.
    '''
    return len(_find_conflicts(problem, assignment, variable, value))

def _find_conflicts(problem, assignment, variable=None, value=None):
    '''
    Find violated constraints on a given assignment, with the possibility
    of specifying a new variable and value to add to the assignment before
    checking.
    '''
    if variable and value:
        assignment = deepcopy(assignment)
        assignment[variable] = value

    conflicts = []
    for neighbors, constraint in problem.constraints:
        # if all the neighbors on the constraint have values, check if conflict
        if all(n in assignment for n in neighbors):
            variables, values = zip(*[(n, assignment[n])
                                      for n in neighbors])
            if not constraint(variables, values):
                conflicts.append((neighbors, constraint))

    return conflicts


def _basic_values_sorter(problem, assignment, variable, domains):
    '''
    Sort values in the same original order.
    '''
    return domains[variable][:]


def _least_constraining_values_sorter(problem, assignment, variable, domains):
    '''
    Sort values based on how many conflicts they generate if assigned.
    '''
    # the value that generates less conflicts
    def update_assignment(value):
        new_assignment = deepcopy(assignment)
        new_assignment[variable] = value
        return new_assignment

    values = sorted(domains[variable][:],
                    key=lambda v: _count_conflicts(problem, assignment,
                                                   variable, v))
    return values


def _backtracking(problem, assignment, domains, variable_chooser,
                  values_sorter):
    '''
    Internal recursive backtracking algorithm.
    '''
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

            result = _backtracking(problem,
                                   new_assignment,
                                   new_domains,
                                   variable_chooser,
                                   values_sorter)
            if result:
                return result

    return None


def _min_conflicts_value(problem, assignment, variable):
    '''
    Return the value generate the less number of conflicts.
    '''
    return _least_constraining_values_sorter(problem,
                                             assignment,
                                             variable,
                                             problem.domains)[0]


def min_conflicts(problem, initial_assignment=None, iterations_limit=0):
    '''
    Min conflicts search.

    initial_assignment the initial assignment, or None to generate a random
    one.
    If iterations_limit is specified, the algorithm will end after that
    number of iterations. Else, it will continue until if finds an assignment
    that doesn't generate conflicts (a solution).
    '''
    assignment = {}
    if initial_assignment:
        assignment.update(initial_assignment)
    else:
        for variable in problem.variables:
            value = _min_conflicts_value(problem, assignment, variable)
            assignment[variable] = value

    iteration = 0
    run = True
    while run:
        conflicts = _find_conflicts(problem, assignment)

        conflict_variables = [v for v in problem.variables
                              if any(v in conflict[0] for conflict in conflicts)]

        if conflict_variables:
            variable = random.choice(conflict_variables)
            value = _min_conflicts_value(problem, assignment, variable)
            assignment[variable] = value

        iteration += 1

        if iterations_limit and iteration >= iterations_limit:
            run = False
        elif not _count_conflicts(problem, assignment):
            run = False

    return assignment
