import enum

class Event(enum.Enum):
    POSITION_SELECTED = 0
    TXN_CANCELLED = 1
    REQUEST_SUBMITTED = 2
    CASH_COLLECTED = 3
    PRICE_SET = 4
    TIMER_EXPIRED = 5

class TimerEvent(enum.Enum):
    RESET_MESSAGE = 0
    TXN_EXPIRED = 1
