from abc import ABC, abstractmethod
from .events import Event

class State(ABC):
    """
    Base State for main controller state machine
    All subclasses must handle events by overidding event handlers
    """

    def __init__(self):
        self.context = None

    def handle_event(self, event, *event_args):
        """
        Event dispatcher
        """
        if event == Event.CASH_COLLECTED:
            self.handle_cash_collected(*event_args)
        elif event == Event.REQUEST_SUBMITTED:
            self.handle_request_submitted(*event_args)
        elif event == Event.POSITION_SELECTED:
            self.handle_position_selected(*event_args)
        elif event == Event.TIMER_EXPIRED:
            self.handle_timer_expired(*event_args)
        elif event == Event.TXN_CANCELLED:
            self.handle_cancel_transaction(*event_args)
        elif event == Event.PRICE_SET:
            self.handle_price_set(*event_args)

    def transition_to(self, state):
        """
        Transition to new state and carry over context
        """
        self.context.state = state
        state.context = self.context

    def handle_price_set(self, *event_args):
        """
        Prices are set by admin
        """
        position = event_args[0]
        price = event_args[1]

        self.context.prices[position] = price

    def handle_cash_collected(self, *event_args):
        pass

    def handle_cancel_transaction(self, *event_args):
        pass

    def handle_timer_expired(self, *event_args):
        pass

    def handle_position_selected(self, *event_args):
        pass

    def handle_request_submitted(self, *event_args):
        pass
