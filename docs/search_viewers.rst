Search algorithms interactive viewers
=====================================

A common issue when solving search problems, is debugging the search
algorithms to find out why our problems aren't being solved as expected.

And most of the time this is somewhat frustrating, because the algorithms don't
follow a "linear" path of execution. They construct a tree, and walk this tree
by jumping and choosing specific nodes on each iteration. 
This makes harder to understand where we are while debugging function calls, 
because we don't have that tree in our minds. 
It becomes difficult to understand "where" the algorithm is at a given moment.

SimpleAI provides you with a tool to overcome that issue. A "map" for you to understand
where you are on the search tree at any moment. The **visual execution
viewers**.

How do they work? The basic idea is this: you attach a viewer to your algorithm 
call, and then you are able to follow the algorithm step by step, while looking 
at the search tree (and more useful information) in real time.

These viewers are meant to be used as a debugging tool, the may slow down the
algorithms a little. But are also useful to collect statistics during the
execution of the algorithms, like maximum size of the fringe, or number of
expanded nodes.

Basic usage
-----------

SimpleAI implements two execution viewers: the WebViewer, and the
ConsoleViewer. From the code point of view, both viewers are used the same
way: you just need to give the search method an extra parameter called
"viewer".

Example:

.. code-block:: python

    from simpleai.search import breadth_first
    from simpleai.search.viewers import WebViewer

    # class HelloProblem..., my_problem = ... (steps from the previous sections about search problems)

    my_viewer = WebViewer()

    result = breadth_first(problem, viewer=my_viewer)


Once you run your program and the search algorithm is called with the attached
viewer, you will be able to interact with the execution on the way the viewer
implements it.

ConsoleViewer
-------------

The ConsoleViewer, by default, will stop on each event of the algorithm (new
iteration, node expanded, ...), print some information about the event, 
and wait for your input. You can just press enter to continue to the next 
event, or use any of the several commands available to get information about 
the execution. You could generate a PNG file with the current search tree, show 
statistics, and more. These commands are explained on the interactive prompt 
shown when you run the algorithm using the ConsoleViewer, so they won't be 
explained here.

For more information about the graph, see the next section.

You can also specify some configuration for the ConsoleViewer when creating it.
It allows two parameters:

* **interactive** (boolean, optional, default to True): You can disable all
  interactions and let the algorithm run until the end. This is useful when you
  want to use the viewer just to collect statistics to be analyzed after the
  execution, and not to debug each step.
* **output_enabled** (boolean, optional, default to True): You can disable all
  output. This is useful when running a non-interactive viewer, to avoid
  flooding the console output with the information of each event during the
  execution.

Example usage:

.. code-block:: python

    from simpleai.search import breadth_first
    from simpleai.search.viewers import ConsoleViewer

    # class HelloProblem..., my_problem = ... (steps from the previous sections about search problems)

    my_viewer = ConsoleViewer(interactive=False, output_enabled=False)

    result = breadth_first(my_problem, viewer=my_viewer)


WebViewer
---------

The WebViewer will start a small website, and keep waiting for interactions
done on the website (this website runs locally, so don't worry, you don't need
an internet connection, and no data is being sent outside your computer. You
can check the WebViewer class code if you are suspicious).

When you run your program you will see a message indicating the web server is
up, and instructions on how to stop it if you don't want it anymore. Once the
server is up, to access the website open a web browser and navigate to `this
address <http://localhost:8000/>`_.

By default, you will see a welcome message, and you will be able to start
running the algorithm by clicking on the "Next step" link. Similar to the
ConsoleViewer, the execution will stop on each event of the algorithm (new
iteration, node expanded, ...) and wait for you to click on the "Next step"
link to run until the next event.  But on each step, you will see a graph
showing the current search tree. Below the graph you will also have useful
information about the last event (the information box is expanded when hovering
with the mouse). And also, you can access a log of all the past events,
clicking on the "Log" link.

The colors of the nodes on the graph have special meanings:

* Blue border, white background: node that are currently part of the fringe
  (waiting to be visited).  
* Blue border, blue background: current node, being analyzed or expanded.
* Orange border, white background: newly created nodes, after expanding a
  parent node.
* Black border, white background: the rest of the nodes kept in memory, needed
  to keep the search tree from the fringe to the initial node.

Like the ConsoleViewer, the WebViewer can receive some configuration parameters
(they are all optional, if you don't understand them just leave them with their
default values):

* **host** (string, optional, default to '127.0.0.1'): by default, the website
  will only allow connections coming from the same machine. If you want to use
  the viewer website from a machine which isn't the one running your program,
  then you can specify that using this parameter.
* **port** (integer, optional, default to 8000): the port where the website
  will be listening.

Example usage:

.. code-block:: python

    from simpleai.search import breadth_first
    from simpleai.search.viewers import WebViewer

    # class HelloProblem..., my_problem = ... (steps from the previous sections about search problems)

    my_viewer = ConsoleViewer(host='0.0.0.0', port=9090)

    result = breadth_first(my_problem, viewer=my_viewer)


Statistics and Logs
-------------------

After running the algorithm, the viewer (Console or Web) will have some
interesting statistics and logs, that may be useful to analyze:

* **max_fringe_size**: the maximum reached size of the fringe.
* **visited_nodes**: number of nodes that were visited.
* **events**: a list of all the events ocurred during the algorithm execution.
  Each event is a tuple with the following structure: (event_name,
  event_description).

You can access those statistics and logs as attributes of the viewer instance,
like this:

.. code-block:: python

    from simpleai.search import breadth_first
    from simpleai.search.viewers import ConsoleViewer

    # class HelloProblem..., my_problem = ... (steps from the previous sections about search problems)

    my_viewer = ConsoleViewer(interactive=False, output_enabled=False)

    result = breadth_first(my_problem, viewer=my_viewer)

    print 'Max fringe size:', my_viewer.max_fringe_size
    print 'Visited nodes:', my_viewer.visited_nodes

    print 'Events:'
    print my_viewer.events


Creating your own execution viewer
----------------------------------

