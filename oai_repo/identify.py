"""
Implementation of Identify verb
"""
from .exceptions import OAIErrorBadArgument


class IdentifyRequest(OAIRequest):
    """
    raises:
        OAIErrorBadArgument
    """
    def __init__(self):
        super().__init__(__class__.__name__)


class IdentifyResponse(OAIResponse):
    """
    """
