"""
Implementation of ListSets verb
"""
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse
from .exceptions import OAIErrorNoSetHierarchy

class SetValidator:
    """Validator for the Set class"""
    def errors(self):
        """
        Verify fields are valid and present where required. Returning a list of descriptive
        errors if any issues were found.
        """
        failures = []
        failures.extend(self._spec_failures())
        failures.extend(self._name_failures())
        failures.extend(self._description_failures())
        return failures

    def _spec_failures(self):
        """Return a list of spec failures"""
        # TODO
        return []

    def _name_failures(self):
        """Return a list of name failures"""
        # TODO
        return []

    def _description_failures(self):
        """Return a list of description failures"""
        # TODO
        return []


class ListSetsRequest(OAIRequest):
    """
    Parse a request for the ListSets verb

    Raises:
        OAIErrorBadArgument
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
    """
    Generate a response for the ListSets verb

    Raises:
        OAIErrorBadResumptionToken
        OAIErrorNoSetHierarchy
    """
    def body(self) -> etree.Element:
        """Response body"""
        # TODO identifier, cursor, total count, resumption token
        setspecs, size, unhashed = self.repository.data.list_set_specs()
        if setspecs is None:
            raise OAIErrorNoSetHierarchy("Repository does not support sets.")

        xmlb = etree.Element("ListSets")
        for setspec in setspecs:
            setobj = self.repository.data.get_set(setspec)
            xset = etree.SubElement(xmlb, "set")
            xspec = etree.SubElement(xset, "setSpec")
            xspec.text = setobj.spec
            xname = etree.SubElement(xset, "setName")
            xname.text = setobj.name
            for desc in setobj.description:
                xname = etree.SubElement(xset, "setDescription")
                xname.append(desc)
        return xmlb
