"""
OAIRepository functionality
"""
from .identify import IdentifyRequest, IdentifyResponse
from .listmetadataformats import ListMetadataFormatsRequest, ListMetadataFormatsResponse


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
        """
        Given a request, route to appropriate action and return a response
        """
        pass
