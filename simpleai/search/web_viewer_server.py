# coding: utf-8
import json
from time import sleep
from flask import Flask, Response, render_template


def get_server(viewer):
    app = Flask(__name__,
                static_folder=viewer.static_folder)


    @app.route('/')
    def index():
        return render_template('web_viewer_server.html',
                               multiple_runs=viewer.multiple_runs)


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
