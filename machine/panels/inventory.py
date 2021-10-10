
class InventoryManager:
    """
    InventoryManager keep track of empty slots. It do not need to
    know about exact item count.
    However to simplify the operations, we are also keeping track
    of quantity so that count could be auto decremented when item is
    dispensed
    For test purpose, methods are provided to set stock in bulk or refill
    an item
    """

    def __init__(self):
        """
        Stock will be auto set in response to events
        In order to set stock for test purposes, use method set_stock
        """
        self.stock = {}

    def in_stock(self, position):
        """
        Check if an item is in stock before accepting request
        """
        if position in self.stock and self.stock[position] != 0:
            return True
        
        return False
    
    def dispense_item(self, position):
        """
        Action would be to instruct controller to dispense item
        This is shown as message on screen for test purposes
        """
        print(f'# ITEM DISPENSER: Dispensed Item at position {position}')

        # Update inventory
        self.stock[position] -= 1

    def refill_stock(self, position, quantity):
        """
        Admin interface
        For test, it could be used to add delpleted items
        """
        if position in self.stock:
            self.stock[position] += quantity
        else:
            self.stock[position] = quantity
    
    def set_stock(self, stock):
        """
        Admin interface
        For test, it could be used to initialize inventory
        """
        self.stock = stock
