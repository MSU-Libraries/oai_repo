"""
Handling OAI-PMH responses
"""
from __future__ import annotations      # To use non-string type hinting; can remove in Python 3.11
from typing import TYPE_CHECKING
from datetime import datetime
from lxml import etree
if TYPE_CHECKING:                       # Prevent circular imports for type hinting
    from .request import OAIRequest
    from .repository import OAIRepository


XML_HEADER = b'<?xml version="1.0" encoding="UTF-8" ?>\n'
NSMAP_BASE = {
    None: b"http://www.openarchives.org/OAI/2.0/",
    "xsi": b"http://www.w3.org/2001/XMLSchema-instance",
}
NSMAP_SCHEMA = (
    b"{" + NSMAP_BASE["xsi"] + b"}schemaLocation",
    b"http://www.openarchives.org/OAI/2.0/ "
    b"http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd"
)
OAIIDENTIFIER_SCHEMA = (
    b"{" + NSMAP_BASE["xsi"] + b"}schemaLocation",
    b"http://www.openarchives.org/OAI/2.0/oai-identifier "
    b"http://www.openarchives.org/OAI/2.0/oai-identifier.xsd"
)
NSMAP_OAIDC = {
    "xsi": b"http://www.w3.org/2001/XMLSchema-instance",
    'dc' : b'http://purl.org/dc/elements/1.1/',
    'oai_dc': b'http://www.openarchives.org/OAI/2.0/oai_dc/'
}
OAIDC_SCHEMA = (
    b"{" + NSMAP_BASE["xsi"] + b"}schemaLocation",
    b"http://www.openarchives.org/OAI/2.0/oai_dc/ "
    b"http://www.openarchives.org/OAI/2.0/oai_dc.xsd"
)

class OAIResponse:
    """
    Base class for OAI responses
    """
    def __init__(
        self,
        repository: OAIRepository,
        request: OAIRequest = None,
        response_date: datetime = None
    ):
        self.repository = repository
        self.request = request
        # root element
        self.xmlr = etree.Element("OAI-PMH", nsmap=NSMAP_BASE)
        self.xmlr.set(*NSMAP_SCHEMA)
        # responseDate element
        response_date = response_date if response_date else datetime.now()
        response_date_elem = etree.SubElement(self.xmlr, "responseDate")
        response_date_elem.text = response_date.replace(microsecond=0).isoformat() + "Z"
        # request element
        request_elem = etree.SubElement(self.xmlr, "request")
        request_elem.text = self.repository.data.get_identify().base_url
        if self and self.request:
            for argk, argv in self.request.args.items():
                request_elem.set(argk, argv)
        # add body element
        self.xmlr.append(self.body())

    def __bool__(self):
        """Default to this being a successful OAI response"""
        return True

    def body(self) -> etree.Element:
        """
        Abstract method to generate OAI response body
        returns:
            lxml.etree.Element
        """
        raise NotImplementedError("OAIResponse must implement the body() method.")

    def root(self) -> etree.Element:
        """
        Return the lxml.etree root element
        """
        return self.xmlr

    def xpath(self, query: str) -> etree.Element:
        """
        Return results of an xpath query from the root element
        """
        return self.xmlr.xpath(query)

    def __bytes__(self):
        """
        Return the XML response as bytes including an XML header line
        """
        return XML_HEADER + etree.tostring(self.xmlr, pretty_print=True)
