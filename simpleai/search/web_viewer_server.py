# coding: utf-8
import json
from os import path
from time import sleep
from flask import Flask, Response, url_for, redirect, send_from_directory


def run_server(viewer):
    resources = path.join(path.dirname(path.realpath(__file__)),
                          'web_viewer_resources')

    app = Flask(__name__,
                static_folder=resources,
                static_path='/static')


    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')


    @app.route('/graph/<graph_format>')
    def graph(graph_format):
        return send_from_directory(viewer.tmp_folder, 'graph.' + graph_format)


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

                    for event in viewer.events[announced:news_limit]:
                        yield 'data: %s\n\n' % json.dumps(event.__dict__)

                    announced = news_limit

        return Response(event_stream(), mimetype="text/event-stream")


    app.run(host=viewer.host, port=viewer.port, processes=5)
