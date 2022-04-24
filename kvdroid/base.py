from kvdroid.event import EventDispatcher
from kvdroid import activity


class EventLoop(EventDispatcher):
    def __init__(self):
        super(EventLoop, self).__init__()
        from kvdroid.app import App
        self.app = App.get_running_app()
        self.quit = False
        self.status = "idle"
        self.resume = False
        self.destroyed = False
        self.paused = False

    def mainloop(self):
        while not self.quit and self.status == "created":
            self.poll()

    def poll(self):
        if activity.isResumed() and not self.resume:
            self.app.dispatch("on_resume")
            self.resume = activity.resume
            self.paused = False

        if activity.isDestroyed() and not self.destroyed:
            self.app.dispatch("on_destroy")
            self.destroyed = activity.destroyed
            self.resume = False

        if not activity.hasWindowFocus() and not self.paused:
            self.app.dispatch("on_pause")
            self.paused = True
            self.resume = False

    def close(self):
        self.quit = True
        self.status = "destroyed"


