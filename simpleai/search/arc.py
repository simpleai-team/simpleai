from collections import deque
from operator import itemgetter


# First two functions are exported for testing purposes.
__all__ = ['neighbors', 'all_arcs', 'revise', 'arc_concistency_3']

fst = itemgetter(0)
snd = itemgetter(1)


def neighbors(xi, constraints, exclude):

    def _neighbor(variables):
        assert len(variables) == 2
        idx_i = variables.index(xi)
        idx_j = 1 - idx_i
        neighbor = variables[idx_j]
        return neighbor

    seen = set()
    for t in constraints:
        variables, constraint = t
        if not xi in variables:
            continue
        xk = _neighbor(variables)
        if xk == exclude:
            continue
        if xk in seen:
            continue
        seen.add(xk)
        yield xk


def revise(domains, variables, constraint):
    """
    Expects the domains to be specified in a list
    """
    xi, xj = variables
    di = domains[xi]  # domain of variable X_i
    dj = domains[xj]  # domain of variable X_j
    revised = False

    for x in di:
        if not any(constraint(variables, (x, y)) for y in dj):
            di.remove(x)
            revised = True
    return revised


def all_arcs(constraints):
    seen = set()
    seen_add = seen.add
    for vars_, const in constraints:
        x, y = vars_

        # arcs
        fwd = (x, y)
        bck = (y, x)

        if not fwd in seen:
            yield (fwd, const)

        if not bck in seen:
            yield (bck, const)

        map(seen_add, (fwd, bck))


def arc_concistency_3(domains, constraints):
    """
    Assumes that constraints contains binary relations
    that the constraints are symmetrical, that is:

       constraint(x, y) == constraint(y, x).
    """
    arcs = deque(all_arcs(constraints))

    while arcs:
        variables, constraint = arcs.popleft()
        print variables
        xi, xj = variables
        if revise(domains, variables, constraint):
            if len(domains[xi]) == 0:
                return False
            for xk in neighbors(xi, constraints, xj):
                arcs.append(((xk, xi), constraint))
    return True
