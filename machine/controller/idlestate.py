from .state import State
from .itemstate import ItemSelectedState
from .events import Event, TimerEvent
from .. import config

class IdleState(State):
    """
    Vending Machine is in Ready state
    """

    def handle_position_selected(self, *event_args):
        """
        Handle user selection an item
        """
        # Clear any running timer
        self.context.timer_manager.cancel(TimerEvent.RESET_MESSAGE)

        # Get Event details
        position = event_args[0]

        # Check if item is available
        if position not in self.context.prices or \
            self.context.prices[position] == 0 or \
            not self.context.inventory_manager.in_stock(position):
            self.context.display.display('Item not available. Select Item...')
            self.context.timer_manager.start_timer(TimerEvent.RESET_MESSAGE,
                                                    config.ERROR_FLASH_DURATION)
            return

        # If available, transition state
        self.context.price = self.context.prices[position]
        self.context.position = position
        self.context.display.display(f'Item {position} price: {self.context.price}...')
        self.context.cash_collector.collect_cash()
        self.context.timer_manager.start_timer(TimerEvent.TXN_EXPIRED,
                                                config.MONEY_WAIT_DURATION)
        self.transition_to(ItemSelectedState())

    def handle_timer_expired(self, *event_args):
        """
        We have displayed error for too long, resetting error
        """
        timer_event = event_args[0]
        if timer_event == TimerEvent.RESET_MESSAGE:
            self.context.display.display('Select Item...')
