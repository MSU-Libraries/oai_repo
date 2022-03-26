"""
Implementation of GetRecord verb
"""
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse


class GetRecordRequest(OAIRequest):
    """
    Parse a request for the GetRecord verb
    raises:
        OAIErrorBadArgument
        OAIErrorIdDoesNotExist
        OAIErrorCannotDisseminateFormat
    """
    def __init__(self):
        super().__init__()
        self.required_args = ["identifier", "metadataPrefix"]

    def post_parse(self):
        """Runs after args are parsed"""


class GetRecordResponse(OAIResponse):
    """Generate a resposne for the GetRecord verb"""
    def body(self) -> etree.Element:
        """Response body"""
        return "TODO"
