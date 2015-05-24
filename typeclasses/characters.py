"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from __future__ import division

import random

from evennia import DefaultCharacter

from world import alternity
from world.alternity import PROFESSIONS, PROFESSION_ACTION_CHECK_BONUS
from world.dice import roll

from commands.default_cmdsets import SkillCmdSet

class Character(DefaultCharacter):
    """
    The Character defaults to implementing some of its hook methods with the
    following standard functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead)
    at_after_move - launches the "look" command
    at_post_puppet(player) -  when Player disconnects from the Character, we
                    store the current location, so the "unconnected" character
                    object does not need to stay on grid but can be given a
                    None-location while offline.
    at_pre_puppet - just before Player re-connects, retrieves the character's
                    old location and puts it back on the grid with a "charname
                    has connected" message echoed to the room

    """

    def at_object_creation(self):
        # basic Alternity ideas
        self.db.profession = random.choice(PROFESSIONS)

        # abilities
        self.db.strength = roll(2, 6, +2)
        self.db.dexterity = roll(2, 6, +2)
        self.db.constitution = roll(2, 6, +2)
        self.db.intelligence = roll(2, 6, +2)
        self.db.will = roll(2, 6, +2)
        self.db.personality = roll(2, 6, +2)

        # durability
        self.db.stun_max = self.db.constitution
        self.db.wound_max = self.db.constitution
        self.db.mortal_max = self.db.constitution // 2

        self.db.stun = self.db.stun_max
        self.db.wound = self.db.wound_max
        self.db.mortal = self.db.mortal_max

        # skills
        self.cmdset.add(SkillCmdSet, permanent=True)

    # resistance modifiers
    @property
    def strength_res(self): return self.resisitance_modifier(self.db.strength)
    @property
    def dexterity_res(self): return self.resisitance_modifier(self.db.dexterity)
    @property
    def constitution_res(self): return self.resisitance_modifier(self.db.constitution)
    @property
    def intelligence_res(self): return self.resisitance_modifier(self.db.intelligence)
    @property
    def will_res(self): return self.resisitance_modifier(self.db.will)
    @property
    def personality_res(self): return self.resisitance_modifier(self.db.personality)

    @staticmethod
    def calc_resistance_modifier(score):
        """Calculate the base resistance modifier for an ability score

        :type score: int
        :returns: int
        """
        if score >=7 and score <= 10:
            return 0
        elif score >=11 and score <= 12:
            return 1
        elif score >=13 and score <= 14:
            return 2
        elif score >=15 and score <= 16:
            return 3
        elif score >=17 and score <= 18:
            return 4
        elif score >= 19:
            return 5
        elif score >= 5 and score <= 6:
            return -1
        elif score <= 4:
            return -2

    @property
    def action_check_score(self):
        return self.calc_action_check_score(self.db.dexterity, self.db.intelligence, self.db.profession)

    @staticmethod
    def calc_action_check_score(dexterity, intelligence, profession):
        """Calculate a base action check score

        :param dexterity: int
        :param intelligence: int
        :param profession: string
        :return: int
        """
        return dexterity + intelligence // 2 + PROFESSION_ACTION_CHECK_BONUS[profession]

