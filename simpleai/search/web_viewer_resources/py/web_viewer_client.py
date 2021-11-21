from enum import Enum

from browser import aio, window


jq = window.jQuery


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

        self.switch_to_tab(Tab.HELP)

        print("Web Viewer Client ready")

    def switch_to_tab(self, tab):
        """
        Show a specific tab to the user, and remember the active tab.
        """
        self.current_tab = Tab.HELP
        jq(".tab").hide()
        jq(f"#{tab.value}").show()

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
