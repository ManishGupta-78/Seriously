from .. import Event

class CashCollector:
    """
    Cash Collector Panel will register with microcontroller for input events
    Methods maked as user interface will be invoked as a response to events
    from microcontroller. However for test purpose, this will be part of
    vending machine public interface
    """

    def __init__(self, observer):
        """
        MainController aka Vending Machine register itself to receive events
        """
        self.observer = observer
        self.accept_cash = False

    def collect_cash(self):
        """
        It will instruct cash collector microcontroller to start collecting
        cash and sending events. cash_collected method will be invoked in
        response to events.
        """
        self.accept_cash = True

    def stop_collection(self):
        """
        It will instruct cash collector microcontroller to stop collecting
        cash and sending events. Any attempt to submit cash would be rejected.
        """
        self.accept_cash = False

    def cash_collected(self, amount):
        """
        User Interface
        Will be invoked by event from microcontroller when cash is inserted by user
        """
        print(f'# CASH COLLECTOR: Cash inserted: {amount}')
        self.observer(Event.CASH_COLLECTED, amount)
