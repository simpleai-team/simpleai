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

You can also specify some configuration for the ConsoleViewer when creating it.
It allows two parameters:

* **interactive**: You could disable all interactions and let the algorithm run
  until the end. This is useful when you want to use the viewer just to collect
  statistics to be analyzed after the execution, and not to debug each step.
* **output_enabled**: You could disable all output. This is useful when running
  a non-interactive viewer, to avoid flooding the console output with the
  information of each event during the execution.

Example usage:

.. code-block:: python

    from simpleai.search import breadth_first
    from simpleai.search.viewers import ConsoleViewer

    # class HelloProblem..., my_problem = ... (steps from the previous sections about search problems)

    my_viewer = ConsoleViewer(interactive=False, output_enabled=False)

    result = breadth_first(my_problem, viewer=my_viewer)


WebViewer
---------

Statistics
----------

Creating your own execution viewer
----------------------------------

