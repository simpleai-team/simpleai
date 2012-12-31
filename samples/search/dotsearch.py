from pygraphviz import AGraph
import base64
import tempfile
from simpleai.search import SearchProblem


class BadInputGraph(Exception):
    pass


class DotGraphSearchProblem(SearchProblem):
    """
    Playground for stuff in the library... eats a .dot graph and allows you
    to try it with the search methods.
    """
    def __init__(self, filename):
        self.G = AGraph(filename)
        xs = [(nodo, nodo.attr.get("initial", None))
              for nodo in self.G.iternodes()]
        xs = [x for x in xs if x[1]]
        if len(xs) == 0:
            raise BadInputGraph("Missing 'initial' node")
        elif len(xs) > 1:
            raise BadInputGraph("Cannot have two initial nodes")
        if not any(nodo.attr.get("goal", None) for nodo in self.G.iternodes()):
            raise BadInputGraph("Missing a goal state '[goal=\"1\"]'")
        super(DotGraphSearchProblem, self).__init__(xs[0][0])
        self.initial_state.attr["shape"] = "doublecircle"
        for node in self.G.iternodes():
            if self.is_goal(node):
                node.attr["shape"] = "hexagon"
                node.attr["color"] = "blue"
        self.seen = set()
        self.visit(self.initial_state)
        for edge in self.G.iteredges():
            edge.attr["style"] = "dotted"
            x = edge.attr.get("weight", None)
            if x:
                x = int(x)
            else:
                x = 1
            edge.attr["weight"] = x
            edge.attr["label"] = x

    def actions(self, state):
        assert state in self.G
        if self.G.is_directed():
            return self.G.itersucc(state)
        else:
            assert self.G.is_undirected()
            return self.G.iterneighbors(state)

    def result(self, state, action):
        assert state in self.G and action in self.G
        self.visit(state)
        return action

    def cost(self, state1, action, state2):
        assert state1 in self.G and action in self.G and action == state2
        x = self.G.get_edge(state1, state2).attr["weight"]
        if float(x) == int(x):
            return int(x)
        else:
            return float(x)

    def visit(self, state):
        if state in self.seen:
            return
        self.seen.add(state)
        attr = self.G.get_node(state).attr
        attr["color"] = "firebrick"

    def is_goal(self, state):
        return bool(state.attr.get("goal", False))

    def value(self, state):
        assert state in self.G
        value = self.G.get_node(state).attr.get("value", None)
        if not value:
            return 0
        return float(value)


def run_algorithm(algorithm, filename):
    problem = DotGraphSearchProblem(filename)
    goal = algorithm(problem)
    if goal:
        problem.visit(goal.state)
        prev = None
        for _, state in goal.path():
            if prev:
                edge = problem.G.get_edge(prev, state)
                edge.attr["style"] = "solid"
            prev = state
        return problem.G, goal.state, goal.cost, problem.value(goal.state), \
               len(problem.seen)
    return problem.G, None, None, None, len(problem.seen)


HTML_TEMPLATE = """
<html><body>
<table style="border:0" align="center">
    <tr><td colspan="2"><h2 style="text-align: center">{graph}</h2></td></tr>
    <tr><td colspan="2"><hr /></td></tr>
    {rows}
</table>
</body></html>
"""

RUN_TEMPLATE = """
<tr>
    <td>
      <b style="text-align: center"> {algorithm} </b> <br /> <br />
      Nodes expanded(or 'visited') = {visited}
      <br /> Path cost = {cost}
      <br /> Final node value = {value} </td>
    {image_column}
</tr>
<tr>
    <td colspan="2"><hr /></td>
</tr>
"""

IMAGE_TEMPLATE = """<td style="padding-left: 50px">
<img src="data:image/png;base64,{image}" /> </td>"""

#
#  Credits to Gonzalo Garcia Berrotaran (j0hn) for the clever way of putting
#  this into HTML.
#


def report(infile=None, algorithms=None, outfile="report.html",
           with_images=True):
    assert infile and algorithms
    rows = []
    for algorithm in algorithms:
        G, goal, cost, value, visited = run_algorithm(algorithm, infile)
        image = ""
        if with_images:
            out = tempfile.NamedTemporaryFile(delete=False)
            G.draw(out, format="png", prog="dot")
            out.seek(0)
            image = base64.b64encode(out.read())
            out.close()
            image = IMAGE_TEMPLATE.format(image=image)
        s = RUN_TEMPLATE.format(algorithm=algorithm.__name__,
                                visited=visited, cost=cost, value=value,
                                image_column=image, )
        rows.append(s)
    s = HTML_TEMPLATE.format(graph=infile, rows="".join(rows))
    open(outfile, "w").write(s)
