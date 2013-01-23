# coding: utf-8
from os import path
import sys
from threading import Thread
from time import sleep


class ConsoleViewer(object):
    def __init__(self, interactive=True):
        self.interactive = interactive

        self.last_event = ''
        self.current_fringe = []
        self.last_chosen = None
        self.last_is_goal = False
        self.last_expanded = None
        self.last_successors = []

        self.chosen_color = '#00cc00'
        self.fringe_color = '#0000dd'

    def start(self):
        self.last_event = 'start'
        self.help()
        self.pause()

    def help(self):
        self.output('After each step, a prompt will be shown.')
        self.output('On the prompt, you can just press Enter to continue to the next step.')
        self.output('But you can also:')
        self.output('* write h then Enter: get help.')
        self.output('* write g PATH_TO_PNG_IMAGE then Enter: create png with graph of the current state.')
        self.output('* write e then Enter: run non-interactively to the end of the algorithm.')
        self.output('* write q then Enter: quit program.')
        self.output('---')

    def pause(self):
        prompt = True
        while prompt:
            prompt = False
            if self.interactive:
                option = raw_input('> ').strip()
                if option:
                    if option == 'h':
                        self.help()
                        prompt = True
                    elif option == 'e':
                        self.interactive = False
                    elif option == 'q':
                        sys.exit()
                    elif option.startswith('g ') and len(option) > 2:
                        png_path = option[2:]
                        self.create_graph(png_path)
                        self.output('graph saved to ' + png_path)
                        prompt = True
                    else:
                        self.output('Incorrect command')
                        self.help()
                        self.pause()

    def output(self, *args):
        print ' '.join(map(str, args))

    def create_graph(self, png_path):
        from pydot import Dot, Edge, Node

        graph = Dot(graph_type='digraph')

        graph_nodes = {}
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
                                  fillcolor='#ffffff')

                graph_nodes[node_id] = new_g_node
                graph.add_node(new_g_node)

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
                        label=node.action_representation())

            if is_successor:
                edge.set_color(self.chosen_color)
                edge.set_labelfontcolor(self.chosen_color)

            graph.add_edge(edge)

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

        graph.write_png(png_path)

    def new_iteration(self, fringe):
        self.last_event = 'new_iteration'
        self.current_fringe = fringe
        self.output(' **** New iteration ****')
        self.output(len(fringe), 'elements in fringe:', fringe)
        self.pause()

    def chosen_node(self, node, is_goal):
        self.last_event = 'chosen_node'
        self.last_chosen, self.last_is_goal = node, is_goal
        self.output('Chosen node:', node)
        if is_goal:
            self.output('Is goal!')
        else:
            self.output('Not goal')
        self.pause()

    def expanded(self, node, successors):
        self.last_event = 'expanded'
        self.last_expanded, self.last_successors = node, successors
        self.output('Expand:', node)
        self.output(len(successors), 'successors:', successors)
        self.pause()


class WebViewer(ConsoleViewer):
    def __init__(self, host='127.0.0.1', port=8000):
        super(WebViewer, self).__init__(interactive=True)
        self.host = host
        self.port = port
        self.paused = True
        self.events = []

        web_template_path = path.join(path.dirname(__file__), 'web_viewer.html')
        self.web_template = open(web_template_path).read()

    def start(self):
        from bottle import route, run

        route('/')(self.web_status)
        route('/next')(self.web_next)
        route('/graph')(self.web_graph)

        t = Thread(target=run, kwargs=dict(host=self.host, port=self.port))
        t.daemon = True
        t.start()

        self.pause()

    def web_status(self):
        from bottle import template
        return template(self.web_template, events=self.events)

    def web_graph(self):
        from bottle import static_file
        graph_name = 'graph.png'
        self.create_graph(graph_name)
        return static_file(graph_name, root='.')

    def web_next(self):
        from bottle import redirect

        self.paused = False
        while not self.paused:
            sleep(0.1)
        redirect('/')

    def pause(self):
        self.paused = True
        while self.paused:
            sleep(0.1)

    def output(self, *args):
        self.events.append(' '.join(map(str, args)))
