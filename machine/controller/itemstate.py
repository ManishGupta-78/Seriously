from .state import State
from .events import Event, TimerEvent
from .amountstate import AmountReceivedState
from .. import config

class ItemSelectedState(State):
    """
    User has selected item. It is now waiting for money to be inserted
    """

    def handle_cash_collected(self, *event_args):
        """
        Watch for if enough cash is collected
        """
        # Clear any running timer
        self.context.timer_manager.cancel(TimerEvent.TXN_EXPIRED)

        # Add to existing amount
        amount = event_args[0]
        self.context.amount += amount

        # coins/cash goes to common box used by change dispenser
        self.context.change_dispenser.add_change(amount, 1)

        if self.context.amount < self.context.price:
            # More cash/coin need to be collected
            self.context.display.display(f'Amount: {self.context.amount}')
            self.context.timer_manager.start_timer(TimerEvent.TXN_EXPIRED,
                                                config.MONEY_WAIT_DURATION)
            return

        # required amount is collected, check if we can provide change
        # if not, give back the last collected amount
        change_required = self.context.amount - self.context.price

        if not self.context.change_dispenser.change_available(change_required):
            # Display error
            self.context.display.display(f'Change not available. Try smaller denomination')
            
            # Return last collection
            self.context.change_dispenser.dispense_change(amount)
            self.context.amount -= amount
            
            self.context.timer_manager.start_timer(TimerEvent.TXN_EXPIRED,
                                                    config.MONEY_WAIT_DURATION)

            # Error displayed must be cleared out after few seconds
            self.context.timer_manager.start_timer(TimerEvent.RESET_MESSAGE,
                                                    config.ERROR_FLASH_DURATION)
            return

        # Display amount on screen
        self.context.display.display('Press OK to dispense item')

        # Stop display reset timer (if running)
        self.context.timer_manager.cancel(TimerEvent.RESET_MESSAGE)

        # Stop collection
        self.context.cash_collector.stop_collection()

        # Start timer for the response from user (select or cancel)
        self.context.timer_manager.start_timer(TimerEvent.TXN_EXPIRED,
                                               config.SELECTION_WAIT_DURATION)
        self.transition_to(AmountReceivedState())

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

        # Stop collection
        self.context.cash_collector.stop_collection()

        # Return collected amount (if any)
        if self.context.amount > 0:
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
            self.context.display.display(f'Amount: {self.context.amount}')
        elif timer_event == TimerEvent.TXN_EXPIRED:
            self.context.display.display(f'Timeout. Money not inserted')
            self.context.timer_manager.start_timer(TimerEvent.RESET_MESSAGE,
                                                    config.ERROR_FLASH_DURATION)
            self.cancel_transaction()
