"""
Ways to apply structured transformations to data
"""

class Transform:
    """
    Given a set of ordered transform rules, use them to transform a string.
    """
    def __init__(self, rules: list):
        self.rules = rules

    def forward(self, value):
        """Apply the set of rules to the provided value in original order."""
        for rule in self.rules:
            ruletype = next(iter(rule))
            rulemethod = getattr(self, f"_{ruletype}")
            value = rulemethod(value, *rule[ruletype])
        return value

    def reverse(self, value):
        """Apply the set of rules to the provided value in reverse order."""
        for rule in reversed(self.rules):
            ruletype = next(iter(rule))
            rulemethod = getattr(self, f"_{ruletype}")
            value = rulemethod(value, *rule[ruletype], reverse=True)
        return value

    def _replace(self, value, find, substitute, *, reverse=False):
        """Apply the "replace" transform."""
        if reverse:
            find, substitute = substitute, find
        return value.replace(find, substitute)

    def _prefix(self, value, action, prefix, *, reverse=False):
        """Apply the "prefix" transform."""
        if reverse:
            action = ["add", "del"]["add" == action]
        if action == "add":
            value = prefix + value
        elif action == "del":
            value = value.removeprefix(prefix)
        return value

    def _suffix(self, value, action, suffix, *, reverse=False):
        """Apply the "suffix" transform."""
        if reverse:
            action = ["add", "del"]["add" == action]
        if action == "add":
            value = value + suffix
        elif action == "del":
            value = value.removesuffix(suffix)
        return value

    def _case(self, value, action, *, reverse=False):
        """Apply the "case" transform."""
        if reverse:
            action = ["upper", "lower"]["upper" == action]
        if action == "upper":
            value = value.upper()
        elif action == "lower":
            value = value.lower()
        return value
