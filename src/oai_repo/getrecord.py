"""
Implementation of GetRecord verb
"""
from datetime import datetime
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse
from .exceptions import OAIErrorIdDoesNotExist, OAIErrorCannotDisseminateFormat
from .helpers import granularity_format
from .interfacedata import RecordHeader


class GetRecordRequest(OAIRequest):
    """
    Parse a request for the GetRecord verb

    Raises:
        OAIErrorBadArgument
    """
    def __init__(self):
        super().__init__()
        self.required_args: list = ["identifier", "metadataPrefix"]
        self.identifier: str = None
        self.metadataprefix: str = None

    def post_parse(self):
        """Runs after args are parsed"""
        self.identifier = self.args.get("identifier")
        self.metadataprefix = self.args.get("metadataPrefix")

    def __repr__(self):
        return f"GetRecordRequest(identifier={self.identifier},"\
               f"metadataprefix={self.metadataprefix})"

class GetRecordResponse(OAIResponse):
    """
    Generate a resposne for the GetRecord verb

    Raises:
        OAIErrorIdDoesNotExist
        OAIErrorCannotDisseminateFormat
    """
    def __repr__(self):
        return f"GetRecordResponse(identifier={self.request.identifier},"\
               f"metadataprefix={self.request.metadataprefix})"

    def body(self) -> etree.Element:
        """Response body"""
        identifier, metadataprefix = self.request.identifier, self.request.metadataprefix
        if not self.repository.data.is_valid_identifier(identifier):
            raise OAIErrorIdDoesNotExist("The given identifier does not exist.")

        mdformats = self.repository.data.get_metadata_formats(identifier)
        if metadataprefix not in [mdf.metadata_prefix for mdf in mdformats]:
            raise OAIErrorCannotDisseminateFormat(
                "The requested metadataPrefix does not exist for the given identifier."
            )

        xmlb = etree.Element("GetRecord")
        add_records(self.repository, [identifier], metadataprefix, xmlb)
        return xmlb

def add_header(repository: "OAIRepository", header: RecordHeader, xmlb: etree._Element):
    """
    Append a OAI <header> element for a given RecordHeader to an XML element.

    Args:
        repository (OAIRepository): An instantiated repository class
        header (RecordHeader): A RecordHeader instance
        xmlb (lxml.etree._Element): The element to add the header to
    """
    xhead = etree.SubElement(xmlb, "header")
    xident = etree.SubElement(xhead, "identifier")
    xident.text = header.identifier
    xstamp = etree.SubElement(xhead, "datestamp")
    xstamp.text = granularity_format(
        repository.data.get_identify().granularity,
        header.datestamp
    ) if isinstance(header.datestamp, datetime) else header.datestamp
    for setspec in header.setspecs:
        xset = etree.SubElement(xhead, "setSpec")
        xset.text = setspec

def add_records(
    repository: "OAIRepository",
    identifiers: list[str],
    metadataprefix: str,
    xmlb: etree._Element
):
    """
    Generate and append <record> OAI elements to an XML doc. If the requested
    metadata prefix is not valid for the identifier, then nothing is added for
    that identifer.

    Args:
        repository (OAIRepository): An instantiated repository class
        identifiers (list[str]): A list of valid identifier strings
        xmlb (lxml.etree._Element): The element to add the records to

    Returns:
        int The count of records added to the XML
    """
    count = 0
    recmetas = repository.data.get_records_metadata(identifiers, metadataprefix)
    recheads = repository.data.get_records_header(identifiers)
    recabouts = repository.data.get_records_abouts(identifiers)

    for recmeta, rechead, recabout in zip(recmetas, recheads, recabouts):
        if recmeta is None:
            continue
        xrec = etree.SubElement(xmlb, "record")
        # Header
        add_header(repository, rechead, xrec)
        # Metadata
        xmeta = etree.SubElement(xrec, "metadata")
        xmeta.append(recmeta)
        # About
        for about in recabout:
            xabout = etree.SubElement(xrec, "about")
            xabout.append(about)
        count += 1
    return count
