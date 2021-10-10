from collections import namedtuple
import sys
from machine.machine import VendingMachine
import config

CommandDetails = namedtuple('CommandDetails',
                            ['usage', 'description', 'handler'])

class Simulator:
    """
    Vending machine simulator
    """

    def __init__(self):
        """
        Create vending machine and arm command handlers
        """
        self.machine = VendingMachine()
        self.command_details = {
            'ok':  CommandDetails('ok', 'Confirm item selection (after inserting money)', self.handle_ok),
            'cancel':  CommandDetails('cancel', 'Cancel transaction', self.handle_cancel),
            'insert':  CommandDetails('insert <amount>','Insert money', self.handle_insert_money),
            'item':    CommandDetails('item <position>', 'Select an item', self.handle_select_item),
            'summary': CommandDetails('summary', 'Print inventory and change details', self.handle_summary),
            'help':    CommandDetails('help', 'Print this help', self.handle_help),
            'exit':    CommandDetails('exit', 'Close simulator', self.handle_exit)
        }
        self.fill_machine()

    def fill_machine(self):
        """
        Fill vending machine based on intial configuration
        """
        # Set Prices
        for position, price in config.prices.items():
            self.machine.admin_panel.set_price(position, price)

        # Stock items
        self.machine.inventory_manager.set_stock(config.items)

        # Add change
        self.machine.change_dispenser.set_change(config.change)

    def handle_ok(self, args):
        """
        Confirm current transaction
        """
        if len(args) != 0:
            self.print_command_help('ok')
            return

        self.machine.selection_panel.submit_request()

    def handle_cancel(self, args):
        """
        Cancel current transaction
        """
        if len(args) != 0:
            self.print_command_help('cancel')
            return

        self.machine.selection_panel.cancel_transaction()

    def handle_insert_money(self, args):
        """
        User inserted money (single bill/coin)
        """
        amount = 0

        # Amount must be specified and must be greater than 0
        if len(args) == 1:
            try:
                amount = int(args[0])
            except ValueError:
                pass
        
        if amount <= 0:
            self.print_command_help('insert')
            return

        if self.machine.cash_collector.accept_cash:
            self.machine.cash_collector.cash_collected(amount)
        else:
            print('# CASH COLLECTOR: Not accepting cash')

    def handle_select_item(self, args):
        """
        User selected item
        """
        if len(args) != 1 or len(args[0]) == 0:
            self.print_command_help('item')
            return

        position = args[0]
        self.machine.selection_panel.select_item(position)

    def handle_summary(self, args):
        """
        Print summary of inventory and change
        """
        if len(args) != 0:
            self.print_command_help('summary')
            return

        print('Prices')
        print('------')
        for position, price in self.machine.prices.items():
            print(f'Position: {position}, Price: {price}')

        print('\nStock')
        print('------')
        for position, quantity in self.machine.inventory_manager.stock.items():
            print(f'Position: {position}, Quantity: {quantity}')

        print('\nChange')
        print('------')
        for denomination, quantity in self.machine.change_dispenser.change.items():
            print(f'Denomination: {denomination}, Quantity: {quantity}')

    def handle_help(self, args):
        """
        Print command's desciption
        """
        if len(args) != 0:
            self.print_command_help('help')
            return

        print('Usage: python simulator.py')
        print('\nCommands')
        for command_detail in self.command_details.values():
            print(f'\n  {command_detail.usage}')
            print(f'    {command_detail.description}')

    def handle_exit(self, args):
        """
        Quit simulator
        """
        if len(args) != 0:
            self.print_command_help('exit')
            return

        sys.exit()

    def print_command_help(self, command):
        """
        Print a single command help usage instructions
        """
        print(f'Correct usage: {self.command_details[command].usage}')
        print(f'  {self.command_details[command].description}')

    def run(self):
        """
        Display prompt, get and dispatch commands
        """
        while True:
            # Get command
            user_input = input('> ')
            cmd_with_args = user_input.split()

            # No command entered
            if not cmd_with_args:
                continue

            command = cmd_with_args[0]
            args = cmd_with_args[1:]

            # Dispatch commands
            if command in self.command_details:
                self.command_details[command].handler(args)
            else:
                print('command not found')
                self.handle_help([])

if __name__ == '__main__':
    simulator = Simulator()
    simulator.run()
