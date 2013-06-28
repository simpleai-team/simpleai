# coding: utf-8
import json
from os import path
from shutil import copy
from time import sleep
from flask import Flask, Response, url_for, redirect


def get_server(viewer):
    app = Flask(__name__,
                static_folder=viewer.tmp_folder)

    html_name = 'web_viewer.html'

    source = path.join(path.dirname(path.realpath(__file__)),
                       html_name)
    destination = path.join(viewer.tmp_folder,
                            html_name)
    copy(source, destination)


    @app.route('/')
    def index():
        return redirect(url_for('static', filename=html_name))

    @app.route('/play')
    def play():
        viewer.status = 'running'
        return 'ok' # TODO should be a json or something


    @app.route('/step')
    def step():
        viewer.status = 'running_step'
        return 'ok' # TODO should be a json or something


    @app.route('/stop')
    def stop():
        viewer.status = 'paused'
        return 'ok' # TODO should be a json or something


    @app.route('/event_stream')
    def stream():
        def event_stream():
            announced = 0
            while True:
                sleep(0.1)
                if len(viewer.events) > announced:
                    news_limit = len(viewer.events)

                    for event, description in viewer.events[announced:news_limit]:
                        event_data = {
                            'event': event,
                            'description': description,
                            'last_event': viewer.last_event[0],
                            'last_event_description': viewer.last_event[1],
                            'max_fringe_size': viewer.max_fringe_size,
                            'visited_nodes': viewer.visited_nodes,
                        }
                        yield 'data: %s\n\n' % json.dumps(event_data)

                    announced = news_limit

        return Response(event_stream(), mimetype="text/event-stream")


    return app
