
class DisplayPanel:
    """
    For a test system, console will act as screen on vending machine
    """

    def display(self, text):
        """
        Text would be send to microcontroller to be displayed
        on vending machine screen
        """
        print(f'# DISPLAY: {text}')
