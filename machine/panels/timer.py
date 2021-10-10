import threading
from functools import partial
from .. import Event

class MachineTimer:
    """
    MachineTimer can manager multiple timers
    It notify timer expiry event to main controller along with
    stored context
    """

    def __init__(self, observer):
        """
        MainController aka Vending Machine register itself to receive events
        """
        self.observer = observer
        self.timers = {}
    
    def start_timer(self, id, duration):
        """
        Starts timer for a specific duration
        If already running, timer will be restarted
        """
        if id in self.timers:
            self.timers[id].cancel()
        
        timer = threading.Timer(duration, partial(self.notifier, id))
        self.timers[id] = timer
        timer.start()

    def notifier(self, id):
        """
        Notify main controller that timer has expired
        """
        self.observer(Event.TIMER_EXPIRED, id)

    def cancel(self, id):
        """
        Cancel timer if running
        """
        if id in self.timers:
            self.timers[id].cancel()
            del self.timers[id]
