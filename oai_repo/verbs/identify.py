"""
Implementation of Identify verb
"""
from .oaiverb import OAIVerb
from ..exceptions import OAIErrorBadArgument

class Identify(OAIVerb):
    """
    raises:
        OAIErrorBadArgument
    """
    def __init__(self):
        super().__init__(__class__.__name__)
