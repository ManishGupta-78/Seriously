import io
import unittest
import unittest.mock
import time
from machine.machine import VendingMachine

class TestMachine(unittest.TestCase):
    """
    Test vending state machine
    """

    def setUp(self):
        self.machine = VendingMachine()
        self.machine.admin_panel.set_price('b5', 10.)
        self.machine.inventory_manager.refill_stock('b5', 10)
        self.machine.change_dispenser.set_change({1: 2, 2: 0})
    
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_item_purchase(self, mock_stdout):
        """
        Test successfully purchasing an item
        """
        expected_display= ''
        # Select Item
        self.machine.selection_panel.select_item('b5')
        expected_display += '# DISPLAY: Item b5 price: 10.0...\n'
        self.assertEqual(mock_stdout.getvalue(), expected_display)
        
        # Insert money
        self.machine.cash_collector.cash_collected(5)
        expected_display += '# CASH COLLECTOR: Cash inserted: 5\n'
        expected_display += '# DISPLAY: Amount: 5\n'
        self.assertEqual(mock_stdout.getvalue(), expected_display)

        # Insert more money
        self.machine.cash_collector.cash_collected(6)
        expected_display += '# CASH COLLECTOR: Cash inserted: 6\n'
        expected_display += '# DISPLAY: Press OK to dispense item\n'
        self.assertEqual(mock_stdout.getvalue(), expected_display)

        # User pressed Ok
        self.machine.selection_panel.submit_request()
        expected_display += '# ITEM DISPENSER: Dispensed Item at position b5\n'
        expected_display += '# DISPLAY: Please collect your item\n'
        expected_display += '# DISPENSE CHANGE: {1: 1}\n'
        self.assertEqual(mock_stdout.getvalue(), expected_display)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_no_change(self, mock_stdout):
        """
        Test if user submitted cash for there is no change
        """
        expected_display= ''
        # Select Item
        self.machine.selection_panel.select_item('b5')
        expected_display += '# DISPLAY: Item b5 price: 10.0...\n'
        self.assertEqual(mock_stdout.getvalue(), expected_display)
        
        # Insert money
        self.machine.cash_collector.cash_collected(14)
        expected_display += '# CASH COLLECTOR: Cash inserted: 14\n'
        expected_display += '# DISPLAY: Change not available. Try smaller denomination\n'
        expected_display += '# DISPENSE CHANGE: {14: 1}\n'
        self.assertEqual(mock_stdout.getvalue(), expected_display)

        # Cancel request
        self.machine.selection_panel.cancel_transaction()

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_cancel_transaction_before_money(self, mock_stdout):
        """
        Test if user cancel transaction after selecting item
        """
        expected_display= ''
        # Select Item
        self.machine.selection_panel.select_item('b5')
        expected_display += '# DISPLAY: Item b5 price: 10.0...\n'
        self.assertEqual(mock_stdout.getvalue(), expected_display)

        # Cancel request
        self.machine.selection_panel.cancel_transaction()
        expected_display += '# DISPLAY: Transaction cancelled\n'
        self.assertEqual(mock_stdout.getvalue(), expected_display)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_cancel_transaction_after_money(self, mock_stdout):
        """
        Test if user cancel transaction after inserting money
        """
        expected_display= ''
        # Select Item
        self.machine.selection_panel.select_item('b5')
        expected_display += '# DISPLAY: Item b5 price: 10.0...\n'
        self.assertEqual(mock_stdout.getvalue(), expected_display)
        
        # Insert money
        self.machine.cash_collector.cash_collected(5)
        expected_display += '# CASH COLLECTOR: Cash inserted: 5\n'
        expected_display += '# DISPLAY: Amount: 5\n'
        self.assertEqual(mock_stdout.getvalue(), expected_display)

        # Insert more money
        self.machine.cash_collector.cash_collected(6)
        expected_display += '# CASH COLLECTOR: Cash inserted: 6\n'
        expected_display += '# DISPLAY: Press OK to dispense item\n'
        self.assertEqual(mock_stdout.getvalue(), expected_display)

        # User pressed Cancel
        self.machine.selection_panel.cancel_transaction()
        expected_display += '# DISPLAY: Transaction cancelled\n'
        expected_display += '# DISPENSE CHANGE: {6: 1, 5: 1}\n'
        self.assertEqual(mock_stdout.getvalue(), expected_display)

if __name__ == '__main__':
    unittest.main()
