"""
Handling OAI-PMH requests
"""
from .exceptions import OAIErrorBadArgument

class OAIRequest:
    """Base class for all OAI requests"""
    def __init__(self):
        self.verb = self.__class__.__name__.removesuffix("Request")

        # A list of all possible args
        self.optional_args = []
        # Required args (unless an exclusive arg is passed)
        self.required_args = []
        # An exclusive arg must be the only arg passed (other than verb)
        self.exclusive_arg = None
        # Mapping of set arguments and their values
        self.args = {}

    @property
    def allowed_args(self):
        """
        Auto-join all possible args into one complete list
        """
        return (
            self.optional_args +
            self.required_args +
            ([self.exclusive_arg] if self.exclusive_arg else [])
        )

    def parse(self, args: dict):
        """
        raises:
            OAIErrorBadArgument
        """
        self.args = args

        if not self.allowed_args and len(self.args) > 0:
            raise OAIErrorBadArgument(
                f"Verb {self.verb} does not allow other arguments."
            )

        if self.exclusive_arg and self.exclusive_arg in self.args and len(self.args) > 1:
            raise OAIErrorBadArgument(
                f"Argument {self.exclusive_arg} is exclusive; other arguments are not allowed."
            )

        if self.required_args and not all(rarg in self.args for rarg in self.required_args):
            raise OAIErrorBadArgument(
                f"Verb {self.verb} requires the arguments: {','.join(self.required_args)}"
            )

        if any(arg not in self.allowed_args for arg in self.args):
            raise OAIErrorBadArgument(
                f"Verb {self.verb} only allows arguments: {','.join(self.allowed_args)}"
            )
        self.post_parse()

    def post_parse(self):
        """Runs after args are parsed"""
        raise NotImplementedError("OAIRequest must implement the post_parse() method.")
