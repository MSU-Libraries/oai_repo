"""
Handling OAI-PMH requests
"""
from .exceptions import OAIErrorBadVerb


class OAIRequest:
    allowed_verbs = [
        'GetRecord',
        'Identify',
        'ListIdentifiers',
        'ListMetadataFormats',
        'ListRecords',
        'ListSets'
    ]

    def __init__(self, verb: str):
        if verb not in OAIRequest.allowed_verbs:
            raise OAIErrorBadVerb("The value of the 'verb' argument in the request is not legal.")

        # A list of all possible args
        self.allowed_args = []
        # Required args (unless an exclusive arg is passed)
        self.required_args = []
        # An exclusive arg must be the only arg passed (other than verb)
        self.exclusive_args = []
        # Mapping of set arguments and their values
        self.args = {}
