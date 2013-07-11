from collections import deque
from operator import itemgetter


# The first 3 functions are exported for testing purposes.
__all__ = ['constraint_wrapper', 'neighbors', 'all_arcs', 'revise', 'arc_consistency_3']

fst = itemgetter(0)


def constraint_wrapper(vars_, constraint):
    '''
    Returns a callable that switches the values argument of @constraint
    acording to the varibles passed to the wrapper returned.

    @constraint is a callable representing the constraint between @vars_.

    Say @vars_ have (X_i, X_j) because we assume the constraint to be
    symmetrical, that is constraint must apply to (X_j, X_i) we need
    to be able to call constraint with the values swapped, according to
    how the variables of the constraint are.
    '''

    if getattr(constraint, 'no_wrap', False):  # constraints made for hidden variables shouldn't be wrapped.
        return constraint

    X_i, X_j = vars_

    def wrapper(variables, values):
        if variables == (X_i, X_j):
            return constraint(variables, values)
        elif variables == (X_j, X_i):
            return constraint(variables, (values[1], values[0]))
        else:
            raise ValueError("This constraint does not work with %s", ", ".join(vars_))
    return wrapper


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
    For each constraint ((X, Y), const) adds ((Y, X), wrapped(const)).

    For why it's wrapped please see constraint_wrapper.
    """

    seen = set()
    seen_add = seen.add
    for vars_, const in constraints:
        try:
            x, y = vars_
        except ValueError:
            continue

        # arcs
        fwd = (x, y)
        bck = (y, x)

        wrapped = constraint_wrapper(vars_, const)

        if not fwd in seen:
            yield (fwd, wrapped)

        if not bck in seen:
            yield (bck, wrapped)

        map(seen_add, (fwd, bck))


def arc_consistency_3(domains, constraints):
    """
    Makes a CSP problem arc consistent.

    Assumes that the constraints are symmetrical, that is:
       constraint(x, y) == constraint(y, x).

    Ignores any constraint that is not binary.
    """
    arcs = deque(all_arcs(constraints))

    while arcs:
        variables, func = arcs.popleft()
        xi, xj = variables
        if revise(domains, variables, func):
            if len(domains[xi]) == 0:
                return False
            for arc in neighbors(xi, constraints, xj):
                arcs.append(arc)
    return True
