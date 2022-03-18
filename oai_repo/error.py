"""
OAI Error
"""
from .response import OAIResponse
from .exceptions import OAIException

class OAIErrorResponse(OAIResponse):
    """
    Reponse for an request that generated an OAI error.
    """
    def __init__(self, exc: OAIException):
        self.code = exc.code()
        self.message = str(exc)

    def __repr__(self):
        return f"OAIErrorResponse(code={self.code})"
