"""
Apply structured transformations to data using a linear set of rules.
"""

class Transform:
    """
    Given a set of ordered transform rules, use them to transform a string forward
    either following those rules in order, apply rules in backward order to
    reverse the transformation.

    Args:
        rules (list): A list of rules in forward order. Each rule being a dict
                      with a single key describing the rule type, and a value which
                      is a list of arguments to that rule.

    **Examples:**
    ```python
    rules = [
        { "replace": [":", "_"] },
        { "prefix": ["add", "oai:"] },
        { "suffix": ["del", ".edu"] },
        { "case": ["upper"] }
    ]
    val = "abcd:5678:example.edu"
    tr = Transform(rules)
    val = tr.forward(val)
    # val is now "OAI:ABCD_5678_EXAMPLE"
    val = tr.reverse(val)
    # val is now "abcd:5678:example.edu" again
    ```

    **Rules:**

    | Type      | Parameters               | Example                                              |
    |-----------|--------------------------|------------------------------------------------------|
    | `replace` | [`find`, `replace_with`] | `[":", "_"]` (replace all `:` with `_`)              |
    | `prefix`  | [`add`\\|`del`, `string`] | `["del", "oai:"]` (remove `oai:` at start of value) |
    | `suffix`  | [`add`\\|`del`, `string`] | `["add", ".id"]` (add `.id` to end of value)        |
    | `case`    | [`upper`\\|`lower`]       | `["upper"]` (convert value to upper case)           |

    Important:
        Applying rules in reverse may not always return the original value!
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
