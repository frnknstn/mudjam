from commands.command import Command

class CmdRepair(Command):
    """
    Attempt the repair of an object
    """

    key = "repair"
    help_category = "skills"

    def func(self):
        args = self.args.strip()
        caller = self.caller

        if args == "":
            self.caller.msg("Usage: %s <object>" % self.cmdstring)
            return

        obj = caller.search(args)

        if obj is None:
            return

        required_repairs = obj.db.required_repairs
        if required_repairs is None or required_repairs <= 0:
            self.caller.msg("The %s does not need repairs." % obj.key)
            return

        self.caller.msg("You attempt to repair %s." % obj.key)
        caller.location.msg_contents("%s attempts to repair %s." %
                                        (caller.name,
                                         obj.name),
                                     exclude=caller)

        caller.msg("Your repair skill score is %d (%+d steps)" % caller.get_skill_score("Repair"))

        obj.attempt_repair(caller)