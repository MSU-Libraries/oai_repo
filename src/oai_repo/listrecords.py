"""
Implementation of ListRecords verb
"""
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse


class ListRecordsRequest(OAIRequest):
    """
    Parse a request for the ListRecords verb
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

class ListRecordsResponse(OAIResponse):
    """Generate a resposne for the ListRecords verb"""
    def body(self) -> etree.Element:
        """Response body"""
        return "TODO"
