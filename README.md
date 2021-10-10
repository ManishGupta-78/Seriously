# Requirements

### Machine components

1. Display
- one line text display

2. Inventory Manager
- Keep all items in slots and dispense item based on position
- Could tell when an item is out of stock

3. Cash collector
- Collect cash only when instructed by main controller
- All cash collected goes to change dispenser, so could be used later to return change

4. Change dispenser
- Dispense change on request
- Can answer if change for certain amount is available

5. Selection Panel
- Can be used to select item (position), confirm or cancel transaction

6. Admin Panel
- Can be used to set item prices

7. Main Controller
- Controls all panels and listen for events from them

### Operation

1. User will first select item (position), once price is displayed, user can insert money and press ok to get the item. Remaining change would be returned.
2. User will reject cash if required change is not available.
3. All cash collected will go to change box, which can be used to provide change later.
4. Once an item is selected, all operations do have an associated timeout. If any operation is timed out, deposited cash would be returned and machine would return to its original state.
5. Any error messages displayed on display would be momentarily and would be removed after few seconds.

# Design

### Philosophy

1. Vending machine is implemented as state machine. This is very similar to how an actual machine works, where allowed operation depends at which machine is in. For this design, state machine is simple, but can easily accommodate more events and states, if more complex workflows are to be supported.
2. State Design pattern is used to implement state machine. This may look like an overkill for a small number of states. However, it allows
    1. Breaking up of code in different python modules.
    2. Easy extension if more complex workflows are required.
3. All machine components are represented by classes that will encapsulate the functionality which will be communicate with panel specific microcontroller. Main controller can send commands to this panels through public interface and/or subscribe to events from them.
4. More panels could be added in future, without modifying the existing ones, allowing for easy extension.

### Limitation
As workflow become more complex, a state machine-based implementation may become more difficult to validate against requirements as number of possible paths could be huge.

Please note that in State, handler methods are not abstract and an empty default implementation is provided for all the methods. This makes use of the fact that default behaviour for handling any event in vending state machine is to ignore it. While, this means &quot;State Design pattern&quot; is not implemented in its true spirit, this greatly reduces the number of handler methods in child classes and will help as number of states/events increases to accommodate for more complex workflows.

### States
1. Idle
    Machine is ready, user can select item
2. ItemSelected
    Item selected, user can insert money
3. AmountReceivedState
    Amount received, user can either confirm or cancel transaction

# Usage
### Using Package
1. For using vending machine from python package,
```
      from machine.machine import VendingMachine
      vm = VendingMachine()
```
2. Add stock to machine
```
vm.inventory_manager.set_stock(stock)
```
3. Add change to machine
```
vm.change_dispenser.set_change(change)
```
4. Set item prices
```
vm.admin_panel.set_price(position, price)
```
5. Select Item
```
vm.selection_panel.select_item(position)
```
6. Collect cash
```
vm.cash_collector.cash_collected(amount)
```
7. Confirm selection
```
vm.selection_panel.submit_request()
```
8. Cancel Transaction
```
vm.selection_panel.cancel_transaction()
```
### Using Simulator
    Run
       python simulator.py

| Command | Description |
| --- | --- |
| ok | Confirm item selection (after inserting money) |
| cancel | Cancel transaction |
| insert &lt;amount&gt; | Insert money |
| item &lt;position&gt; | Select an item |
| summary | Print inventory and change details |
| help | Print this help |
| exit | Close simulator |

### Run unit tests
Run
```
    python tests.py
```