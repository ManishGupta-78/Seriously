from .. import Event

class SelectionPanel:
    """
    Selection Panel will register with microcontroller for input events
    Methods maked as user interface will be invoked as a response to events
    from microcontroller. However for test purpose, this will be part of
    vending machine public interface
    """

    def __init__(self, observer):
        """
        MainController aka Vending Machine register itself to receive events
        """
        self.observer = observer
    
    def select_item(self, position):
        """
        User Interface
        Will be invoked by event from microcontroller
        """
        self.observer(Event.POSITION_SELECTED, position)

    def cancel_transaction(self):
        """
        User Interface
        Will be invoked by event from microcontroller
        """
        self.observer(Event.TXN_CANCELLED)

    def submit_request(self):
        """
        User Interface
        Will be invoked by event from microcontroller
        """
        self.observer(Event.REQUEST_SUBMITTED)
