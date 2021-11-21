# coding: utf-8

from __future__ import print_function

from os import path
import sys
from tempfile import mkdtemp
from time import sleep
from threading import Thread


class Event(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name


CONSOLE_HELP_TEXT = '''After each step, a prompt will be shown.
On the prompt, you can just press Enter to continue to the next step.
But you can also have this commands:
(write the command you want to use and then press Enter)
* h: get help.
* e: run non-interactively to the end of the algorithm.
* s: show statistics of the execution (max fringe size, visited nodes).
* q: quit program.'''


class BaseViewer(object):
    def __init__(self):
        self.successor_color = '#DD4814'
        self.fringe_color = '#20a0c0'
        self.solution_color = '#adeba8'
        self.font_size = "11"

        self.last_event = None
        self.events = []

        self.stats = {
            'max_fringe_size': 0,
            'visited_nodes': 0,
            'iterations': 0,
            'max_depth': 0,
        }

        self.clear_nodes_data()

    def clear_nodes_data(self):
        self.current_fringe = []
        self.last_chosen = None
        self.last_expandeds = []
        self.last_successors = []

    def event(self, name, *params):
        getattr(self, 'handle_' + name)(*params)

    def log_event(self, name, description):
        self.last_event = Event(name=name,
                                description=description)
        self.events.append(self.last_event)

    def handle_started(self):
        self.clear_nodes_data()
        self.log_event('started', 'Algorithm just started.')

    def handle_new_iteration(self, fringe):
        self.current_fringe = fringe
        self.stats['max_fringe_size'] = max(self.stats['max_fringe_size'], len(fringe))
        self.stats['iterations'] += 1

        description = 'New iteration with %i elements in the fringe:\n%s'
        description = description % (len(fringe), str(fringe))
        self.log_event('new_iteration', description)

    def handle_chosen_node(self, node, is_goal=None):
        self.last_chosen = node
        self.stats['visited_nodes'] += 1

        goal_text = 'Is goal!' if is_goal else 'Not goal'
        description = 'Chosen node: %s' % node
        if is_goal is not None:
            description += '\n' + goal_text
        self.log_event('chosen_node', description)

    def handle_expanded(self, nodes, successors):
        self.last_expandeds, self.last_successors = nodes, successors

        description = 'Expanded %s\nSuccessors: %s'
        description = description % (nodes, successors)
        for successors_group in successors:
            self.stats["max_depth"] = max(
                self.stats["max_depth"],
                *[node.depth for node in successors_group],
            )
        self.log_event('expanded', description)

    def handle_finished(self, fringe, node, solution_type):
        self.clear_nodes_data()
        self.solution_node = node
        if node:
            self.current_fringe = [node]
        self.solution_type = solution_type

        description = 'Finished algorithm returning %s.\nSolution type: %s'
        description = description % (node, solution_type)

        if node is not None and node.parent is not None:
            description += '\nPath from initial to goal: %s' % str(node.path())
        self.log_event('finished', description)

    def handle_no_more_runs(self, node, solution_type):
        self.clear_nodes_data()
        self.solution_node = node
        if node:
            self.current_fringe = [node]
        self.solution_type = solution_type

        description = 'Finished all of the runs of the inner algorithm returning %s.\nSolution type: %s'
        description = description % (node, solution_type)

        if node is not None and node.parent is not None:
            description += '\nPath from initial to goal: %s' % str(node.path())
        self.log_event('no_more_runs', description)


class ConsoleViewer(BaseViewer):
    def __init__(self, interactive=True):
        super(ConsoleViewer, self).__init__()
        self.interactive = interactive

    def event(self, name, *params):
        if name == 'started':
            self.output(CONSOLE_HELP_TEXT)

        super(ConsoleViewer, self).event(name, *params)

        self.output('EVENT: %s' % self.last_event.name)
        self.output(self.last_event.description)

        self.pause()

    def pause(self):
        prompt = True
        while prompt and self.interactive:
            prompt = False
            option = input('> ').strip()
            if option:
                if option == 'h':
                    self.output(CONSOLE_HELP_TEXT)
                    prompt = True
                elif option == 'e':
                    self.interactive = False
                elif option == 's':
                    self.output('Statistics:')
                    for stat, value in list(self.stats.items()):
                        self.output('%s: %i' % (stat.replace('_', ' '), value))
                    prompt = True
                elif option == 'q':
                    sys.exit()
                else:
                    self.output('Incorrect command')
                    self.output(CONSOLE_HELP_TEXT)
                    self.pause()

    def output(self, text):
        print(text)


class WebViewer(BaseViewer):
    def __init__(self, host='0.0.0.0', port=8000):
        super(WebViewer, self).__init__()
        self.host = host
        self.port = port
        self.status = 'paused'
        self.updating_graph_data = False
        self.server_running = False

    def event(self, name, *params):
        if name == 'started':
            self.start_server()

        super(WebViewer, self).event(name, *params)

        self.updating_graph_data = True
        self.update_graph_data()
        self.updating_graph_data = False

        if self.status == 'running_step':
            self.status = 'paused'

        while self.status == 'paused':
            sleep(0.5)

        sleep(0.5)

    def update_graph_data(self):
        """
        Update the graph data used by the interactive graph in the UI.
        """
        # visualizer nodes by search node id
        vis_nodes = {}
        root_vis_nodes = []

        def node_to_visualizer(search_node):
            """
            If the searh node isn't known, add a visualizer node to the
            visualizer nodes dict with the correct text, tooltip, etc.
            """
            search_node_id = id(search_node)
            if search_node_id not in vis_nodes:
                name = search_node.state_representation()
                tooltip = ""
                if hasattr(search_node, "cost"):
                    tooltip += f"\nCost: {search_node.cost}"
                if hasattr(search_node, 'heuristic'):
                    tooltip += f"\nHeuristic: {search_node.heuristic}"
                if hasattr(search_node, 'value'):
                    tooltip += f"\nValue: {search_node.value}"

                vis_node = {
                    "name": name,
                    "tooltip": tooltip,
                }
                vis_nodes[search_node_id] = vis_node

                if search_node.parent is None:
                    root_vis_nodes.append(vis_node)
                else:
                    parent_vis_node = node_to_visualizer(search_node.parent)
                    children = parent_vis_node.setdefault("children", [])
                    children.append(vis_node)

            return vis_nodes[search_node_id]

        if self.last_event.name == 'chosen_node':
            # add node and its full path if not present
            vis_node = node_to_visualizer(self.last_chosen)
            # mark it as chosen node
            vis_node["chosen"] = True

        if self.last_event.name == 'finished':
            if self.solution_node:
                # add node and its full path if not present
                vis_node = node_to_visualizer(self.solution_node)
                # mark it as solution node
                vis_node["solution_node"] = True

        if self.last_event.name == 'expanded':
            for node, successors in zip(self.last_expandeds,
                                        self.last_successors):
                # add expanded node and its full path if not present
                vis_node = node_to_visualizer(node)
                # mark it as expanded node
                vis_node["expanded"] = True
                for successor_node in successors:
                    # add new child node and its full path if not present
                    vis_node = node_to_visualizer(successor_node)
                    # mark it as new child node
                    vis_node["new_child"] = True

        # and finally, add the rest of the graph starting from the pending
        # nodes in the fringe
        for node in self.current_fringe:
            vis_node = node_to_visualizer(node)
            # mark it as fringe node
            vis_node["in_fringe"] = True

        self.graph_data = {
            "nodes": root_vis_nodes,
            "nodes_count": len(vis_nodes),
            "max_depth": self.stats["max_depth"],
        }

    def start_server(self):
        if not self.server_running:
            from simpleai.search.web_viewer_server import run_server

            t = Thread(target=run_server, args=[self])
            t.daemon = True
            t.start()

            self.server_running = True
