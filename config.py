"""
Intital State of vending machine
"""

# Position to price mapping
prices = {
    'a1': 5.,
    'a2': 3.,
    'a3': 10.,
    'b1': 6.,
    # b2 price not set
    'b3': 8.,
    'c1': 10.,
    'c2': 2.,
    'c3': 5.
}

# Position to quantity mapping
# for some positions price may be set but they may be empty
items = {
    'a1': 10,
    'a2': 3,
    'a3': 0, # we ran out of a3
    'b1': 4,
    'b2': 2, # b2 is present but admin forgot to set price, user can't buy
    'b3': 1,
    # c1 is missing/empty
    'c2': 2,
    'c3': 7
}

# Denominations to quantity mapping
change = {
    1: 20,
    2: 10,
    5: 3
}
