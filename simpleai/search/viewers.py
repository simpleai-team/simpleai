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

        def get_graph_node(node, expanded=False, chosen=False, in_fringe=False):
            node_id = id(node)
            if node_id not in graph_nodes:
                if expanded or chosen:
                    fillcolor = '#00cc00'
                else:
                    fillcolor = '#ffffff'

                new_g_node = Node('%s\n[%s]' % (repr(node), node_id),
                                  style='filled',
                                  fillcolor=fillcolor)
                graph_nodes[node_id] = new_g_node

            return graph_nodes[node_id]

        def get_edge_to_parent(node, is_successor=False):
            if is_successor:
                color = '#00cc00'
            else:
                color = '#000000'

            g_node = get_graph_node(node)
            g_parent_node = get_graph_node(node.parent)

            return Edge(g_parent_node,
                        g_node,
                        label=str(node.action),
                        color=color)

        if self.last_event == 'chosen_node':
            get_graph_node(self.last_chosen, chosen=True)

        if self.last_event == 'expanded':
            get_graph_node(self.last_expanded, expanded=True)
            for node in self.last_successors:
                graph.add_edge(get_edge_to_parent(node, is_successor=True))

        for node in self.current_fringe:
            get_graph_node(node, in_fringe=True)
            while node is not None and node not in done:
                if node.parent is not None:
                    graph.add_edge(get_edge_to_parent(node))
                else:
                    graph.add_node(get_graph_node(node))

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
