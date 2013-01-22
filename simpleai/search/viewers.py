# coding: utf-8

class DummyViewer(object):
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
