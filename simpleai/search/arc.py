# coding: utf-8
from operator import itemgetter


# The first 3 functions are exported for testing purposes.
__all__ = ['all_arcs', 'revise', 'arc_consistency_3']

fst = itemgetter(0)


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

    for neighbors, constraint in constraints:
        if len(neighbors) == 2:
            x, y = neighbors
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
