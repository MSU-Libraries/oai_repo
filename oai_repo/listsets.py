"""
Implementation of ListSets verb
"""
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse


class ListSetsRequest(OAIRequest):
    """
    Parse a request for the ListSets verb
    raises:
        OAIErrorBadArgument
        OAIErrorBadResumptionToken
        OAIErrorNoSetHierarchy
    """
    def __init__(self):
        super().__init__()
        self.exclusive_arg = "resumptionToken"

    def post_parse(self):
        """Runs after args are parsed"""

class ListSetsResponse(OAIResponse):
    """Generate a resposne for the ListSets verb"""
    def body(self) -> etree.Element:
        """Response body"""
        return "TODO"
