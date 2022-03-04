"""
OAIRepository functionality
"""
from .request import OAIRequest
from .response import OAIResponse

class OAIRepository:
    """
    """
    def __init__(self):
        pass

    def config_from_file(self, filepath):
        pass

    def config(self, key: str, val):
        """
        Set or change a repository configuration setting
        """
        pass

    def process(self, request: OAIRequest) -> OAIResponse:
        pass
