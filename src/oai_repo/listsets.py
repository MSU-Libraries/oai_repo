"""
Implementation of ListSets verb
"""
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse


class OAISetValidator:
    """
    """


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
        self.resumptiontoken: str = None

    def post_parse(self):
        """Runs after args are parsed"""
        if "resumptionToken" in self.args:
            self.resumptiontoken = self.args["resumptionToken"]

class ListSetsResponse(OAIResponse):
    """Generate a resposne for the ListSets verb"""
    def body(self) -> etree.Element:
        """Response body"""
        #TODO alternate ideas: class implemented and registerd externally?

        setspecs = self.repository.apiqueries.list_sets(self.resuptiontoken)
        xmlb = etree.Element("ListSets")
        for setspec in setspecs:
            xset = etree.SubElement(xmlb, "set")
            xsetspec = etree.SubElement(xset, "setSpec")
            xsetspec.text = setspec
        return xmlb
