# coding: utf-8
from os import path
import sys
from threading import Thread
from time import sleep

HELP_TEXT = '''After each step, a prompt will be shown.
On the prompt, you can just press Enter to continue to the next step.
But you can also:
* write h then Enter: get help.
* write g PATH_TO_PNG_IMAGE then Enter: create png with graph of the current state.
* write e then Enter: run non-interactively to the end of the algorithm.
* write s then Enter: show statistics of the execution (max fringe size, visited nodes).
* write q then Enter: quit program.'''


class ConsoleViewer(object):
    def __init__(self, interactive=True, output_enabled=True,
                 multiple_runs=False):
        self.interactive = interactive
        self.multiple_runs = multiple_runs
        self.output_enabled = output_enabled

        self.successor_color = '#DD4814'
        self.fringe_color = '#20a0c0'
        self.font_size = 11

        self.clean()

    def clean(self):
        self.last_event = ''
        self.last_event_description = ''
        self.events = []

        self.max_fringe_size = 0
        self.visited_nodes = 0

        self.current_fringe = []
        self.last_chosen = None
        self.last_is_goal = False
        self.last_expandeds = []
        self.last_successors = []

    def pause(self):
        prompt = True
        while prompt:
            prompt = False
            if self.interactive:
                option = raw_input('> ').strip()
                if option:
                    if option == 'h':
                        self.output(HELP_TEXT)
                        prompt = True
                    elif option == 'e':
                        self.interactive = False
                    elif option == 's':
                        self.output('Statistics:')
                        self.output('Max fringe size: %i' % self.max_fringe_size)
                        self.output('Visited nodes: %i' % self.visited_nodes)
                        prompt = True
                    elif option == 'q':
                        sys.exit()
                    elif option.startswith('g ') and len(option) > 2:
                        png_path = option[2:]
                        self.create_graph(png_path)
                        self.output('graph saved to %s' % png_path)
                        prompt = True
                    else:
                        self.output('Incorrect command')
                        self.output(HELP_TEXT)
                        self.pause()

    def event(self, event, description):
        self.last_event = event
        self.last_event_description = description
        self.events.append((event, description))

        self.output('EVENT: %s' % event)
        self.output(description)

    def output(self, text):
        if self.output_enabled:
            print text

    def started(self):
        self.event('started', HELP_TEXT)
        self.pause()

    def create_graph(self, png_path):
        from pydot import Dot, Edge, Node

        graph = Dot(graph_type='digraph')

        graph_nodes = {}
        graph_edges = {}
        done = set()

        def add_node(node, expanded=False, chosen=False, in_fringe=False,
                     in_successors=False):
            node_id = id(node)
            if node_id not in graph_nodes:
                label = node.state_representation()
                if hasattr(node, 'cost'):
                    label += '\nCost: %s' % node.cost
                if hasattr(node, 'heuristic'):
                    label += '\nHeuristic: %s' % node.heuristic
                if hasattr(node, 'value'):
                    label += '\nValue: %s' % node.value

                new_g_node = Node(node_id,
                                  label=label,
                                  style='filled',
                                  shape='circle',
                                  fillcolor='#ffffff',
                                  fontsize=self.font_size)

                graph_nodes[node_id] = new_g_node

            g_node =  graph_nodes[node_id]

            if expanded or chosen:
                g_node.set_fillcolor(self.fringe_color)
            if in_fringe:
                g_node.set_color(self.fringe_color)
                g_node.set_penwidth(3)
            if in_successors:
                g_node.set_color(self.successor_color)
                g_node.set_fontcolor(self.successor_color)

            return g_node

        def add_edge_to_parent(node, is_successor=False, parent=None):
            if parent is None:
                parent = node.parent

            g_node = add_node(node, in_successors=is_successor)
            g_parent_node = add_node(parent)

            edge = Edge(g_parent_node,
                        g_node,
                        label=node.action_representation(),
                        fontsize=self.font_size)

            if is_successor:
                edge.set_color(self.successor_color)
                edge.set_labelfontcolor(self.successor_color)

            graph_edges[id(node), id(parent)] = edge

        if self.last_event == 'chosen_node':
            add_node(self.last_chosen, chosen=True)

        if self.last_event == 'expanded':
            for node, successors in zip(self.last_expandeds,
                                        self.last_successors):
                add_node(node, expanded=True)
                for successor_node in successors:
                    add_edge_to_parent(successor_node,
                                       is_successor=True,
                                       parent=node)

        for node in self.current_fringe:
            add_node(node, in_fringe=True)
            while node is not None and node not in done:
                if node.parent is not None:
                    add_edge_to_parent(node)
                else:
                    add_node(node)

                done.add(node)
                node = node.parent

        for node_id in sorted(graph_nodes.keys()):
            graph.add_node(graph_nodes[node_id])
        for node_id, parent_id in sorted(graph_edges.keys()):
            graph.add_edge(graph_edges[node_id, parent_id])

        graph.write_png(png_path)

    def new_iteration(self, fringe):
        self.current_fringe = fringe
        self.max_fringe_size = max(self.max_fringe_size, len(fringe))

        description = 'New iteration with %i elements in the fringe:\n%s'
        description = description % (len(fringe), str(fringe))
        self.event('new_iteration', description)

        self.pause()

    def chosen_node(self, node, is_goal=None):
        self.last_chosen, self.last_is_goal = node, is_goal
        self.visited_nodes += 1

        goal_text = 'Is goal!' if is_goal else 'Not goal'
        description = 'Chosen node: %s' % node
        if is_goal is not None:
            description += '\n' + goal_text
        self.event('chosen_node', description)

        self.pause()

    def expanded(self, nodes, successors):
        self.last_expandeds, self.last_successors = nodes, successors

        description = 'Expanded %s\nSuccessors: %s'
        description = description % (nodes, successors)
        self.event('expanded', description)

        self.pause()

    def finished(self, fringe, node, solution_type):
        self.current_fringe = fringe
        self.solution_node = node
        self.solution_type = solution_type

        if self.multiple_runs:
            description = 'Finished one of the runs of the inner algorithm returning %s\nSolution type: %s'
        else:
            description = 'Finished algorithm returning %s\nSolution type: %s'
        description = description % (node, solution_type)

        if node is not None and node.parent is not None:
            description += '\nPath from initial to goal: %s' % str(node.path())
        self.event('finished', description)

        self.pause()

    def no_more_runs(self, node, solution_type):
        self.solution_node = node
        self.solution_type = solution_type

        description = 'Finished all of the runs of the inner algorithm returning %s\nSolution type: %s'
        description = description % (node, solution_type)

        if node is not None and node.parent is not None:
            description += '\nPath from initial to goal: %s' % str(node.path())
        self.event('no_more_runs', description)

        self.pause()


class WebViewer(ConsoleViewer):
    def __init__(self, host='127.0.0.1', port=8000):
        super(WebViewer, self).__init__(interactive=True, output_enabled=False)
        self.host = host
        self.port = port
        self.paused = True

        web_template_path = path.join(path.dirname(__file__), 'web_viewer.html')
        self.web_template = open(web_template_path).read()

    def started(self):
        self.event('started', 'Started running')
        from bottle import route, run

        route('/')(self.web_index)
        route('/view/:status_type')(self.web_view)
        route('/next/:status_type')(self.web_next)
        route('/graph')(self.web_graph)

        t = Thread(target=run, kwargs=dict(host=self.host, port=self.port))
        t.daemon = True
        t.start()

        self.pause()

    def web_index(self):
        from bottle import redirect
        return redirect('/view/graph')

    def web_view(self, status_type='graph'):
        from bottle import template
        return template(self.web_template,
                        max_fringe_size=self.max_fringe_size,
                        visited_nodes=self.visited_nodes,
                        last_event = self.last_event,
                        last_event_description = self.last_event_description,
                        multiple_runs=self.multiple_runs,
                        events=self.events[:-1],
                        status_type=status_type)

    def web_graph(self):
        from bottle import static_file
        graph_name = 'graph.png'
        self.create_graph(graph_name)
        return static_file(graph_name, root='.')

    def web_next(self, status_type='graph'):
        from bottle import redirect

        self.paused = False
        while not self.paused:
            sleep(0.1)

        redirect('/view/' + status_type)

    def pause(self):
        self.paused = True
        while self.paused:
            sleep(0.1)

    def output(self, text):
        pass
