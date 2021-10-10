from .panels.adminpanel import AdminPanel
from .panels.cashcollector import CashCollector
from .panels.display import DisplayPanel
from .panels.inventory import InventoryManager
from .panels.selectionpanel import SelectionPanel
from .panels.timer import MachineTimer
from .panels.changedispenser import ChangeDispenser
from .controller.idlestate import IdleState

class VendingMachine:
    def __init__(self):
        """
        Intitialize all components and start state machine
        """
        self.admin_panel = AdminPanel(self)
        self.cash_collector = CashCollector(self)
        self.change_dispenser = ChangeDispenser()
        self.display = DisplayPanel()
        self.inventory_manager = InventoryManager()
        self.selection_panel = SelectionPanel(self)
        self.timer_manager = MachineTimer(self)

        # Initialize machine
        self.state = IdleState()
        self.state.context = self
        self.display.display('Select Item...')

        # Context
        self.amount = 0
        self.position = None
        self.price = 0
        self.prices = {}

    def __call__(self, event, *args):
        """
        Handle events from different controllers and dispatch
        further to state machine
        """
        self.state.handle_event(event, *args)
