# coding: utf-8
from operator import itemgetter


# The first 3 functions are exported for testing purposes.
__all__ = ['neighbors', 'all_arcs', 'revise', 'arc_consistency_3']

fst = itemgetter(0)


def neighbors(xi, constraints, exclude):
    '''
    Returns all variables that are related, through a constraint, to @xi

    @constraints is a list of tuples, each tuple having
    a tuple of variables and a callable which serves as
    the constraint between the variables. e.g:

    [(('X', 'Y'), lambda vars, values: values[0] == values[1]), .. ]

    If the constraint was as above, 'Y' would be a neighbor of 'X'.
    '''
    def _neighbor(variables):
        idx_i = variables.index(xi)
        idx_j = 1 - idx_i
        neighbor = variables[idx_j]
        return neighbor

    seen = set()
    for t in constraints:
        variables, func = t

        if len(variables) != 2:  # ignore constraints that are not binary
            continue

        if not xi in variables:
            continue
        xk = _neighbor(variables)
        if xk == exclude:
            continue
        if xk in seen:
            continue
        seen.add(xk)
        yield ((xk, xi), func)


def revise(domains, variables, constraint):
    """
    Given variables X_i, X_j = variables, removes the values from X_i's domain that
    do not meet the constraint between X_i and X_j.

    That is, given x in X_i's domain, x will be removed from the domain, if
    there is no value y in X_j's domain that makes constraint(x,y) True.

    ``constraint`` is a callable from the constraint list.
    """
    xi, xj = variables
    di = domains[xi]  # domain of variable X_i
    dj = domains[xj]  # domain of variable X_j
    revised = False

    for x in di:
        if not any(constraint(variables, (x, y))  # constraint is a callable
                   for y in dj):
            di.remove(x)
            revised = True
    return revised


def all_arcs(constraints):
    """
    For each constraint ((X, Y), const) adds:
        ((X, Y), const)
        ((Y, X), const)
    """
    arcs = set()

    for vars_, const in constraints:
        if len(vars_) == 2:
            x, y = vars_
            map(arcs.add, ((x, y), (y, x)))

    return arcs


def arc_consistency_3(domains, constraints):
    """
    Makes a CSP problem arc consistent.

    Ignores any constraint that is not binary.
    """
    arcs = list(all_arcs(constraints))
    pending_arcs = set(arcs)

    while pending_arcs:
        x, y = pending_arcs.pop()
        if revise(domains, (x, y), constraints):
            if len(domains[x]) == 0:
                return False
            pending_arcs = pending_arcs.union((x2, y2) for x2, y2 in arcs
                                              if y2 == x)
    return True
