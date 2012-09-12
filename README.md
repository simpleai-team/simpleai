Simple AI
=========

(Project home: http://github.com/fisadev/simpleai)

This packages is based and inspired in aima-python:
https://code.google.com/p/aima-python/

We implement most of the searches in aima-python plus some extra options. Besides, we make
some improvements in terms of code readability, installation, testing, and others.

Installation
============

Just get it:

    pip install simpleai


Examples
========

Simple AI allows you to define problems and look for the solution with
different strategies. Another samples are in the *samples* directory, but
here is an easy one.

This problem tries to create the string "HELLO WORLD" using the A* algorithm:


    from simpleai.models import Problem
    from simpleai.search import astar

    GOAL = 'HELLO WORLD'

    class HelloProblem(Problem):
        def actions(self, state):
            if len(state) < len(GOAL):
                return [c for c in ' ABCDEFGHIJKLMNOPQRSTUVWXYZ']
            else:
                return []

        def result(self, state, action):
            return state + action

        def is_goal(self, state):
            return state == GOAL

        def heuristic(self, state):
            # how far are we from the goal?
            wrong = sum([1 if state[i] != GOAL[i] else 0
                        for i in range(len(state))])
            missing = len(GOAL) - len(state)
            return wrong + missing


    problem = HelloProblem(initial_state='')
    result = astar(problem)

    print result
    print result.path()
    
Authors
=======

* Juan Pedro Fisanotti <fisadev@gmail.com>
* Rafael Carrascosa <rcarrascosa@machinalis.com>
* Santiago Romero <sromero@machinalis.com>

Special acknowledgements to Machinalis (http://www.machinalis.com/) for the
time provided to work on this project.
