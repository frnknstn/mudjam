import alternity

skill_list = {}

class Skill(object):
    def __init__(self, name, ability, parent=None):
        """Object representing a skill

        :param name: str
        :param ability: str
        :param parent: str
        """
        assert ability in alternity.ABILITIES

        self.name = name
        self.ability = ability
        self.children = None
        self.children = None

        # if we have no parent, we are a broad skill
        if parent is None:
            self.parent = None
            self.children = {}
        else:
            self.parent = skill_list[parent]
            self.children = None
            self.parent.children[name] = self

        # add us to the skill list
        skill_list[name] = self

    @property
    def broad(self):
        """return true if this is a broad skill"""
        return self.parent is None

Skill("Technical Science", "intelligence")
Skill("Juryrig", "intelligence", "Technical Science")
Skill("Repair", "intelligence", "Technical Science")

Skill("Awareness", "will")
Skill("Intuition", "will", "Awareness")
Skill("Perception", "will", "Awareness")

Skill("Resolve", "will")
Skill("Mental Resolve", "will", "Resolve")
Skill("Physical Resolve", "will", "Resolve")