"""
Implementation of ListIdentifiers verb
"""
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse


class ListIdentifiersRequest(OAIRequest):
    """
    Parse a request for the ListIdentifiersResponse verb
    raises:
        OAIErrorBadArgument
        OAIErrorBadResumptionToken
        OAIErrorCannotDisseminateFormat
        OAIErrorNoRecordsMatch
        OAIErrorNoSetHierarchy
    """
    def __init__(self):
        super().__init__()
        self.optional_args = ["from", "until", "set"]
        self.required_args = ["metadataPrefix"]
        self.exclusive_arg = "resumptionToken"

    def post_parse(self):
        """Runs after args are parsed"""

class ListIdentifiersResponse(OAIResponse):
    """Generate a resposne for the ListIdentifiers verb"""
    def body(self) -> etree.Element:
        """Response body"""
        return "TODO"
