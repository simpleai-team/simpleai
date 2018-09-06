# coding: utf-8

from __future__ import print_function

import json
from os import path, _exit
from time import sleep
from flask import Flask, Response, send_file


def run_server(viewer):
    resources = path.join(path.dirname(path.realpath(__file__)),
                          'web_viewer_resources')

    app = Flask(__name__,
                static_folder=resources,
                static_url_path='/static')

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
            stop_server()

        return 'ok' # TODO should be a json or something


    @app.route('/event_stream')
    def stream():
        def event_stream():
            announced = 0
            while True:
                sleep(0.1)
                if len(viewer.events) > announced:
                    news_limit = len(viewer.events)

                    data = {}
                    data['stats'] = [{'name': stat.replace('_', ' '), 'value': value}
                                     for stat, value in list(viewer.stats.items())]

                    for event in viewer.events[announced:news_limit]:
                        data['event'] = event.__dict__
                        yield 'data: %s\n\n' % json.dumps(data)

                    announced = news_limit

        return Response(event_stream(), mimetype="text/event-stream")


    try:
        print('Starting the WebViewer, access it from your web browser, navigating to the address:')
        print('http://localhost:%i' % viewer.port)
        print('To stop the WebViewer, use the "Stop running" link (on the viewer site, from the browser)')

        app.run(host=viewer.host, port=viewer.port, threaded=True)
    except Exception as err:
        print('Failed to start the WebViewer. Error:')
        print(err)
        stop_server()


def stop_server():
    _exit(1)
