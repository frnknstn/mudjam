"""dice and dice rolling helpers"""

from __future__ import division

from random import randint as _randint

# standard rollers
def roll(dice, sides, bonus):
    """
    Roll xDy + z, and returns the total.

    :param dice: int
    :param sides: int
    :param bonus: int
    :return: int
    """
    total = 0
    for i in range(dice):
        total += _randint(1, sides) + bonus

    return total

def alternity_check():
    pass

