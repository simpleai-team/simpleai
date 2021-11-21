from enum import Enum

from browser import aio, window


jq = window.jQuery
EventSource = window.EventSource
jsjson = window.JSON


class Tab(Enum):
    """
    The tabs that the user can view.
    """
    HELP = "help"
    GRAPH = "graph"
    LOG = "log"
    STATS = "stats"


class AlgorithmAction(Enum):
    """
    The actions that we can cask to the algorithm running in the background.
    """
    PLAY = "play"
    STEP = "step"
    PAUSE = "pause"
    STOP = "stop"


class WebViewerClient:
    """
    The Web Viewer client side app itself.
    """
    def __init__(self):
        """
        Initialize the client side app.
        """
        print("Initializing Web Viewer Client...")

        jq(".control-algorithm-btn").on("click", self.on_control_algorithm_click)
        jq(".show-tab-btn").on("click", self.on_show_tab_click)

        self.last_event = None
        self.event_log = []
        self.stats = {}

        self.stats_display = jq("#stats-display")
        self.last_event_display = jq("#last-event-display")
        self.log_display = jq("#log-display")

        self.switch_to_tab(Tab.HELP)
        self.initialize_event_stream()

        print("Web Viewer Client ready")

    def switch_to_tab(self, tab):
        """
        Show a specific tab to the user, and remember the active tab.
        """
        self.current_tab = Tab.HELP
        jq(".tab").hide()
        jq(f"#{tab.value}").show()

    def initialize_event_stream(self):
        """
        Start listening to the event stream from the running algorithm.
        """
        self.event_source = EventSource.new("/event_stream")
        self.event_source.onmessage = self.on_message

    def on_message(self, event):
        """
        Message received from the running algorithm.
        The "event" parameter here isn't an algorithm event, but a message
        from the web event stream.
        """
        message = jsjson.parse(event.data)
        self.register_event(message.event)
        self.register_stats(message.stats)

    def register_event(self, event):
        """
        Register and show an algorithm event.
        """
        self.last_event = event
        self.event_log.append(event)

        event_html = self.event_as_html(event)
        self.last_event_display.html(event_html)
        self.log_display.append(event_html)
        window.render()

    def register_stats(self, stats):
        """
        Register new stats from the algorithm.
        """
        self.stats = stats
        self.stats_display.html("".join(
            f"""<h2>{stat.name}</h2>
                <p>{stat.value}</p>"""
            for stat in stats
        ))

    def event_as_html(self, event):
        """
        Build the html for a single event.
        """
        return f"""<h2>{event.name}</h2>
                   <p>{event.description}</p>"""

    def on_control_algorithm_click(self, e):
        """
        Tell the running algorithm to do something.
        """
        action = e.target.getAttribute("data-action")
        jq.ajax({"url": f"/control/{action}"})

    def on_show_tab_click(self, e):
        """
        Show a specific tab, defined by the clicked control.
        """
        tab_to_show = e.target.getAttribute("data-tab")
        jq(".tab").hide()
        jq(f"#{tab_to_show}").show()
