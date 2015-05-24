# core Alternity concepts
import dice

PROFESSIONS = ["combat spec", "diplomat", "free agent", "tech op", "none"]
PROFESSION_ACTION_CHECK_BONUS = {"combat spec": 3, "diplomat": 1, "free agent": 2, "tech op": 1, "none": 1}

ABILITIES = ["strength", "dexterity", "constitution", "intelligence", "will", "personality"]

STEP_DICE = [
    dice.DiceSet(0, 0, 0),
    dice.DiceSet(1, 4, 0),
    dice.DiceSet(1, 6, 0),
    dice.DiceSet(1, 8, 0),
    dice.DiceSet(1, 12, 0),
    dice.DiceSet(1, 20, 0),
    dice.DiceSet(2, 20, 0),
    dice.DiceSet(3, 20, 0)
]
