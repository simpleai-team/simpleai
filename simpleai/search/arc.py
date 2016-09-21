# coding: utf-8
from operator import itemgetter

from simpleai.search.csp import _call_constraint


# The first 3 functions are exported for testing purposes.
__all__ = ['all_arcs', 'revise', 'arc_consistency_3']

fst = itemgetter(0)


def revise(domains, arc, constraints):
    """
    Given the arc X, Y (variables), removes the values from X's domain that
    do not meet the constraint between X and Y.

    That is, given x1 in X's domain, x1 will be removed from the domain, if
    there is no value y in Y's domain that makes constraint(X,Y) True, for
    those constraints affecting X and Y.
    """
    x, y = arc
    related_constraints = [(neighbors, constraint)
                           for neighbors, constraint in constraints
                           if set(arc) == set(neighbors)]

    modified = False

    for neighbors, constraint in related_constraints:
        for x_value in domains[x]:
            constraint_results = (_call_constraint({x: x_value, y: y_value},
                                                   neighbors, constraint)
                                  for y_value in domains[y])

            if not any(constraint_results):
                domains[x].remove(x_value)
                modified = True

    return modified


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
            list(map(arcs.add, ((x, y), (y, x))))

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
