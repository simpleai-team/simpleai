# coding: utf-8
from os import path
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

    def pause(self):
        if self.interactive:
            raw_input('> press Enter ')

    def output(self, *args):
        print ' '.join(map(str, args))

    def new_iteration(self, fringe):
        self.output(' **** New iteration ****')
        self.output(len(fringe), 'elements in fringe:', fringe)
        self.pause()

    def chosen_node(self, node, is_goal):
        self.output('Chosen node:', node)
        if is_goal:
            self.output('Is goal!')
        else:
            self.output('Not goal')
        self.pause()

    def expanded(self, node, successors):
        self.output('Expand:', node)
        self.output(len(successors), 'successors:', successors)
        self.pause()


class WebViewer(ConsoleViewer):
    def __init__(self, host='127.0.0.1', port=8000):
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
