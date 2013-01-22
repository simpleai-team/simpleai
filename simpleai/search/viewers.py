# coding: utf-8
from threading import Thread


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

    def new_iteration(self, fringe):
        print ' **** New iteration ****'
        print len(fringe), 'elements in fringe:', fringe
        self.pause()

    def chosen_node(self, node, is_goal):
        print 'Chosen node:', node
        if is_goal:
            print 'Is goal!'
        else:
            print 'Not goal'
        self.pause()

    def expanded(self, node, successors):
        print 'Expand:', node
        print len(successors), 'successors:', successors
        self.pause()


class WebViewer(DummyViewer):
    def __init__(self):
        self.paused = True
        self.events = []

    def start(self):
        from bottle import route, run, redirect

        @route('/')
        def status():
            return '<a href="/next">Next</a> <br />Status:<br />' + '<br />'.join(self.events)

        @route('/next')
        def next():
            self.paused = False
            redirect('/')

        t = Thread(target=run)
        t.daemon = True
        t.start()

        self.pause()

    def pause(self):
        self.paused = True
        while self.paused:
            pass

    def event(self, *args):
        self.events.append(' '.join(map(str, args)))

    def new_iteration(self, fringe):
        self.event(' **** New iteration ****')
        self.event(len(fringe), 'elements in fringe:', fringe)
        self.pause()

    def chosen_node(self, node, is_goal):
        self.event('Chosen node:', node)
        if is_goal:
            self.event('Is goal!')
        else:
            self.event('Not goal')
        self.pause()

    def expanded(self, node, successors):
        self.event('Expand:', node)
        self.event(len(successors), 'successors:', successors)
        self.pause()
