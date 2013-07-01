# coding: utf-8
import json
from os import path, _exit
from time import sleep
from flask import Flask, Response, send_file


def run_server(viewer):
    resources = path.join(path.dirname(path.realpath(__file__)),
                          'web_viewer_resources')

    app = Flask(__name__,
                static_folder=resources,
                static_path='/static')

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


    @app.route('/')
    def index():
        return send_file(path.join(resources, 'index.html'))


    @app.route('/graph')
    def graph():
        while viewer.creating_graph:
            sleep(0.1)
        return send_file(viewer.graph_path)


    @app.route('/control/<order>')
    def control(order):
        if order == 'play':
            viewer.status = 'running'
        elif order == 'step':
            viewer.status = 'running_step'
        elif order == 'pause':
            viewer.status = 'paused'
        elif order == 'stop':
            _exit(1)

        return 'ok' # TODO should be a json or something


    @app.route('/event_stream')
    def stream():
        def event_stream():
            announced = 0
            while True:
                sleep(0.1)
                if len(viewer.events) > announced:
                    news_limit = len(viewer.events)

                    for event in viewer.events[announced:news_limit]:
                        yield 'data: %s\n\n' % json.dumps(event.__dict__)

                    announced = news_limit

        return Response(event_stream(), mimetype="text/event-stream")


    app.run(host=viewer.host, port=viewer.port, threaded=True)
