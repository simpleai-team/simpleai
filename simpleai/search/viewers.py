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
* write q then Enter: quit program.'''


class ConsoleViewer(object):
    def __init__(self, interactive=True):
        self.interactive = interactive

        self.last_event = ''
        self.last_event_description = ''
        self.events = []

        self.current_fringe = []
        self.last_chosen = None
        self.last_is_goal = False
        self.last_expanded = None
        self.last_successors = []

        self.chosen_color = '#00cc00'
        self.fringe_color = '#0000dd'
        self.font_size = 11

    def pause(self):
        prompt = True
        while prompt:
            prompt = False
            if self.interactive:
                option = raw_input('> ').strip()
                if option:
                    if option == 'h':
                        print HELP_TEXT
                        prompt = True
                    elif option == 'e':
                        self.interactive = False
                    elif option == 'q':
                        sys.exit()
                    elif option.startswith('g ') and len(option) > 2:
                        png_path = option[2:]
                        self.create_graph(png_path)
                        print 'graph saved to ' + png_path
                        prompt = True
                    else:
                        print 'Incorrect command'
                        print HELP_TEXT
                        self.pause()

    def event(self, event, description):
        self.last_event = event
        self.last_event_description = description
        self.events.append((event, description))

        print 'EVENT:', event
        print description

    def start(self):
        self.event('start', HELP_TEXT)
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
                c = getattr(node, 'cost', '-')
                h = getattr(node, 'heuristic', '-')
                label = '%s\nCost: %s\nHeuristic: %s'
                label = label % (node.state_representation(), c, h)

                new_g_node = Node(node_id,
                                  label=label,
                                  style='filled',
                                  fillcolor='#ffffff',
                                  fontsize=self.font_size)

                graph_nodes[node_id] = new_g_node

            g_node =  graph_nodes[node_id]

            if expanded or chosen:
                g_node.set_fillcolor(self.chosen_color)
            if in_fringe:
                g_node.set_color(self.fringe_color)
                g_node.set_fontcolor(self.fringe_color)
            if in_successors:
                g_node.set_color(self.chosen_color)
                g_node.set_fontcolor(self.chosen_color)

            return g_node

        def add_edge_to_parent(node, is_successor=False):
            g_node = add_node(node, in_successors=is_successor)
            g_parent_node = add_node(node.parent)

            edge = Edge(g_parent_node,
                        g_node,
                        label=node.action_representation(),
                        fontsize=self.font_size)

            if is_successor:
                edge.set_color(self.chosen_color)
                edge.set_labelfontcolor(self.chosen_color)

            graph_edges[id(node)] = edge

        if self.last_event == 'chosen_node':
            add_node(self.last_chosen, chosen=True)

        if self.last_event == 'expanded':
            add_node(self.last_expanded, expanded=True)
            for node in self.last_successors:
                add_edge_to_parent(node, is_successor=True)

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
        for node_id in sorted(graph_edges.keys()):
            graph.add_edge(graph_edges[node_id])

        graph.write_png(png_path)

    def new_iteration(self, fringe):
        self.current_fringe = fringe

        description = 'New iteration with %i elements in the fringe:\n%s'
        description = description % (len(fringe), str(fringe))
        self.event('new_iteration', description)

        self.pause()

    def chosen_node(self, node, is_goal):
        self.last_chosen, self.last_is_goal = node, is_goal

        goal_text = 'Is goal!' if is_goal else 'Not goal'
        description = 'Chosen node: %s\n%s'
        description = description % (node, goal_text)
        self.event('chosen_node', description)

        self.pause()

    def expanded(self, node, successors):
        self.last_expanded, self.last_successors = node, successors

        description = 'Expanded %s\n%i successors:%s'
        description = description % (node, len(successors), successors)
        self.event('expanded', description)

        self.pause()


class WebViewer(ConsoleViewer):
    def __init__(self, host='127.0.0.1', port=8000):
        super(WebViewer, self).__init__(interactive=True)
        self.host = host
        self.port = port
        self.paused = True

        web_template_path = path.join(path.dirname(__file__), 'web_viewer.html')
        self.web_template = open(web_template_path).read()

    def start(self):
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
                        events=self.events,
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
