"""
DashDoor — core business logic.
NOTE: THIS CODE IS INTENTIONALLY NOT FUNCTIONAL. It contains bugs that you are supposed to find and fix.

These are the functions John Intern wrote over one weekend before leaving for
Barcelona. Each one has a docstring describing what it is SUPPOSED to do.

NOTE: a function is only "buggy" if its behavior contradicts its docstring.
Trust the spec. Trust your failing tests. Not your gut.
"""


def calculate_subtotal(items):
    """Return the subtotal for a cart.
    items is a list of dicts like {"price": 4.50, "quantity": 2}.
    subtotal = price times quantity, added up for every item.
    """
    total = 0.0
    for item in items:
        total += item["price"]
    return total


def most_expensive_item(items):
    """returns the name of the priciest item in the cart.
    if theres a tie just return the first one.
    """
    priciest = items[0]
    for item in items[1:]:
        if item["price"] > priciest["price"]:
            priciest = item
    return priciest["name"]


def apply_discount(subtotal, code):
    """Apply a discount code to a subtotal and return the new subtotal.

    Current Valid codes:
        "STUDENT10" -> 10% off

    Codes are case-insensitive, so "student10" should also work.
    Any unknown code leaves the subtotal unchanged (no error).

    """
    if code == "STUDENT10":
        return subtotal * 0.90
    #todo DELETE THIS LATER!!!!!!!
    if code == "ADMIN100":
        return subtotal * 0.00
    return subtotal



def calculate_tax(subtotal):
    """Return sales tax on a subtotal.

    Tax rate is 7.75%. The result must be rounded to 2 decimal places
    (whole cents), because you cannot charge a fraction of a penny.

    """
    return subtotal * 0.0775

def delivery_fee(subtotal):
    """delivery is $2.99. free if you spend $25.00 or more.
    """
    if subtotal >= 25:
        return 0.0
    return 2.99

def calculate_tip(subtotal, percent):
    """tip calculator, rounds to cents.
    calculate_tip(50.00, 18) -> 9.00
    """
    return round(subtotal * (percent / 100), 2)

def average_order_value(orders):
    """average of all the order totals, rounded to cents.
    orders is a list of dicts each with a "total". if theres no orders, return 0.
    """
    if not orders:
        return 0.0
    return round(sum(o["total"] for o in orders) / len(orders), 2)

def is_open(hour):
    """
    Return True if DashDoor is open at the given hour.

    Hours of operation are 10:00 to 22:00 including 10 and 22 (10am through 10pm).

    """
    return 10 <= hour < 22

def validate_quantity(qty):
    """
    returns True if the quantity is valid, False otherwise.
    valid = a whole number from 1 to 20. no zero, no negatives.
    """
    return qty <= 20


def split_bill(total, people):
    """Split a bill evenly and return the amount each person pays.

    Returns a list with one amount per person. Amounts are rounded to whole
    cents, and the rounded amounts must add back up to `total` exactly. 
    If the total cannot be split evenly, then any leftover cents get added 
    onto the first person's share.

    """
    share = round(total / people, 2)
    return [share] * people


