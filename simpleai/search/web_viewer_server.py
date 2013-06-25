# coding: utf-8
from time import sleep
from flask import Flask, Response, render_template


def get_server(viewer):
    app = Flask(__name__,
                static_folder=viewer.static_folder)


    @app.route('/')
    def index():
        return render_template('web_viewer_server.html')


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
                        # TODO the event should inform something like this:
                        #max_fringe_size
                        #visited_nodes
                        #last_event
                        #last_event_description
                        #multiple_runs
                        #events
                        #status_type
                        yield 'data: %s\n\n' % 'lipe puto'

                    announced = news_limit

        return Response(event_stream(), mimetype="text/event-stream")


    return app
