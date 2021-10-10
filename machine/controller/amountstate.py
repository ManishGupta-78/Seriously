from .state import State
from .events import Event, TimerEvent
from .. import config

class AmountReceivedState(State):
    """
    User has already inserted cash, User an now either press Ok or Cancel
    """

    def handle_request_submitted(self, *event_args):
        """
        User pressed ok
        """
        # To avoid circular dependency
        from .idlestate import IdleState

        # Dispense Item
        self.context.inventory_manager.dispense_item(self.context.position)

        # Display message
        self.context.display.display('Please collect your item')
        self.context.timer_manager.start_timer(TimerEvent.RESET_MESSAGE,
                                               config.ERROR_FLASH_DURATION)

        # Return change
        change = self.context.amount - self.context.price
        if change > 0:
            self.context.change_dispenser.dispense_change(change)

        # Reset context
        self.context.amount = 0
        self.context.price = 0
        self.context.position = None
        self.transition_to(IdleState())

    def handle_cancel_transaction(self, *event_args):
        """
        User cancelled transaction
        """
        # Clear any running timer
        self.context.timer_manager.cancel(TimerEvent.TXN_EXPIRED)

        # Display message
        self.context.display.display('Transaction cancelled')
        self.context.timer_manager.start_timer(TimerEvent.RESET_MESSAGE,
                                               config.ERROR_FLASH_DURATION)

        # Move to idle
        self.cancel_transaction()

    def cancel_transaction(self):
        """
        Transaction could be cancelled either by user or due to timeout
        """
        # To avoid circular dependency
        from .idlestate import IdleState

        # Return collected amount
        self.context.change_dispenser.dispense_change(self.context.amount)

        # Reset context
        self.context.amount = 0
        self.context.price = 0
        self.context.position = None
        self.transition_to(IdleState())

    def handle_timer_expired(self, *event_args):
        """
        We have displayed error for too long, resetting error
        """
        timer_event = event_args[0]
        if timer_event == TimerEvent.RESET_MESSAGE:
            self.context.display.display('Press OK to dispense item')
        elif timer_event == TimerEvent.TXN_EXPIRED:
            self.context.display.display(f'Timeout. No selection made')
            self.context.timer_manager.start_timer(TimerEvent.RESET_MESSAGE,
                                                    config.ERROR_FLASH_DURATION)
            self.cancel_transaction()
