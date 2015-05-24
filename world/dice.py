"""dice and dice rolling helpers"""

from __future__ import division

from random import randint as _randint


# standard rollers
def roll(count, sides, bonus):
    """Basic xDy + z dice

    :param count: int
    :param sides: int
    :param bonus: int
    :return: int
    """
    total = 0
    for i in range(count):
        total += _randint(1, sides) + bonus

    return total


class DiceSet(object):
    def __init__(self, count, sides, bonus):
        """Basic xDy + z dice

        :param count: int
        :param sides: int
        :param bonus: int
        """
        self.count = count
        self.sides = sides
        self.bonus = bonus

    def roll(self):
        """
        Roll the dice set, and returns the total.

        :return: int
        """
        total = 0
        for i in range(self.count):
            total += _randint(1, self.sides) + self.bonus

        return total

# Alternity
from alternity import STEP_DICE


class AlternityCheck(object):
    control_dice = DiceSet(1, 20, 0)

    def __init__(self, target_value, situation_step, trivial=False):
        """Perform a new Alternity check

        :param target_value: int
        :param situation_step: int
        :param trivial: bool
        """

        # parse parameters
        if situation_step < -5:
            situation_step = -5 # PHB pg. 49

        self.target_value = target_value
        self.situation_step = situation_step
        self.trivial = trivial  # If a test is trivial, then it will have a 'marginal' result instead of a failure

        # variables to hold the results
        self.situation_dice = None
        self.control_result = None
        self.situation_result = None
        self.result = None

        self.is_success = False
        self.is_failure = False
        self.is_critical_hit = False
        self.is_amazing = False
        self.is_good = False
        self.is_ordinary = False
        self.is_marginal = False
        self.is_critical_miss = False

        self.roll()

    def roll(self):
        """Perform an Alternity check"""
        self.situation_dice = STEP_DICE[abs(self.situation_step)]

        target_value = self.target_value
        control_result = self.control_dice.roll()
        situation_result = self.situation_dice.roll()

        result = control_result
        if self.situation_step < 0:
            # bonus
            result -= situation_result
        elif self.situation_step > 0:
            # penalty
            result += situation_result

        if control_result != 20:
            if result > target_value:
                # failure
                if not self.trivial:
                    self.is_failure = True
                else:
                    self.is_success = True
                    self.is_marginal = True
            elif result <= (target_value // 4):
                # amazing
                self.is_success = True
                self.is_amazing = True
            elif result <= (target_value // 2):
                # good
                self.is_success = True
                self.is_good = True
            elif result <= target_value:
                # ordinary
                self.is_success = True
                self.is_ordinary = True

            # critical hit
            if self.is_success and control_result == 1:
                self.is_critical_hit = True
        else:
            # critical miss
            self.is_critical_miss = True
            if self.trivial:
                # yeah, a critical miss on a trivial test is still a success unless you specifically want otherwise
                self.is_success = True
            else:
                self.is_failure = True

        # set the values on the object
        self.control_result = control_result
        self.situation_result = situation_result
        self.result = result

    def situation_description(self):
        """return a string describing the situation step.

        For example, a +2 would result in the string:
           '+2 step penalty'
        """
        situation_step = self.situation_step
        favor = ""
        color = ""

        if situation_step > 0:
            favor = " penalty"
            color = "{r"
        elif situation_step < 0:
            favor = " bonus"
            color = "{g"

        desc = "%s%+d{n step%s" % (color, situation_step, favor)
        return desc

    def result_description(self):
        """return a string describing the result.

        For example, an amazing result would return the string:
           'amazing success'
        """

        if not self.is_critical_hit:
            success_string = "success"
        else:
            success_string = "critical!"

        if self.is_critical_miss:
            desc = "{RCritical failure{n"
        elif self.is_failure:
            desc = "{rfailure{n"
        elif self.is_marginal:
            desc = "{xmarginal{n %s" % success_string
        elif self.is_ordinary:
            desc = "{Yordinary{n %s" % success_string
        elif self.is_good:
            desc = "{ygood{n %s" % success_string
        elif self.is_amazing:
            desc = "{gamazing{n %s" % success_string
        else:
            desc = "unknown??!"

        return desc

    def roll_description(self):
        """return a string representing the component dice of the result

        For example, a control die of 14 and a situation die of -6 would return:
          '14 - 6 = 8'
        """

        if self.situation_step < 0:
            sign = "-"
        else:
            sign = "+"

        desc = "%d %s %d = %d" % (self.control_result, sign, self.situation_result, self.result)
        return desc


