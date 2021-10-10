
class ChangeDispenser:
    """
    ChangeDispenser keeps track of change and dispense change when asked
    """

    def __init__(self):
        """
        Coins available for each dominition will be auto set in response to events
        In order to fill change for test purposes, use method set_change
        """
        self.change = {}

    def get_change(self, amount, change):
        """
        Get domination and quantity required for returning change
        """
        if amount == 0:
            return {}

        for size in change:
            if change[size] > 0 and size <= amount:
                remaining_change = dict(change)
                remaining_change[size] -= 1
                breakup = self.get_change(amount-size, remaining_change)
                if breakup is not None:
                    if size in breakup:
                        breakup[size] += 1
                    else:
                        breakup[size] = 1

                    return breakup

        return None

    def change_available(self, amount):
        """
        Check if change can be dispensed for given amount
        """
        if self.get_change(amount, self.change) is not None:
            return True
        
        return False

    def dispense_change(self, amount):
        """
        Change status will be updated by events from controller
        However, for test purposes, we are updating it here along
        with dispense change
        """
        breakup = self.get_change(amount, self.change)
        
        print(f'# DISPENSE CHANGE: {breakup}')

        for size, quantity in breakup.items():
            self.change[size] -= quantity

    def set_change(self, change):
        """
        Admin interface
        To be used by test unit
        """
        self.change = change

    def add_change(self, size, quantity):
        """
        Cash collected from user is also added to change dispenser
        """
        if size in self.change:
            self.change[size] += quantity
        else:
            self.change[size] = quantity
