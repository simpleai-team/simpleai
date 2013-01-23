# coding: utf-8
from os import path
import sys
from threading import Thread
from time import sleep


class DummyViewer(object):
    def start(self):
        pass

    def new_iteration(self, fringe):
        pass

    def chosen_node(self, node, is_goal):
        pass

    def expanded(self, node, successors):
        pass


class ConsoleViewer(DummyViewer):
    def __init__(self, interactive=True):
        self.interactive = interactive

        self.current_fringe = []
        self.last_chosen = None
        self.last_is_goal = False
        self.last_expanded = None
        self.last_successors = []

    def start(self):
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
        from pydot import Dot
        g = Dot(graph_type='digraph')
        pending = self.current_fringe[:]
        while pending:
            node = pending.pop()
            if node.parent:
                g.add_edge(id(node), id(node.parent))

        g.write_png(png_path)

    def new_iteration(self, fringe):
        self.current_fringe = fringe
        self.output(' **** New iteration ****')
        self.output(len(fringe), 'elements in fringe:', fringe)
        self.pause()

    def chosen_node(self, node, is_goal):
        self.last_chosen, self.last_is_goal = node, is_goal
        self.output('Chosen node:', node)
        if is_goal:
            self.output('Is goal!')
        else:
            self.output('Not goal')
        self.pause()

    def expanded(self, node, successors):
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

        t = Thread(target=run, kwargs=dict(host=self.host, port=self.port))
        t.daemon = True
        t.start()

        self.pause()

    def web_status(self):
        from bottle import template
        return template(self.web_template, events=self.events)

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
