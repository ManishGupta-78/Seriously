from .. import Event

class AdminPanel:
    """
    Panel for setting inventory prices
    Accessible only to admin
    """

    def __init__(self, observer):
        """
        MainController aka Vending Machine register itself to receive events
        """
        self.observer = observer
    
    def set_price(self, position, price):
        """
        Admin Interface
        Will be invoked by event from microcontroller
        Item at position with missing price would not be available
        """
        self.observer(Event.PRICE_SET, position, price)
