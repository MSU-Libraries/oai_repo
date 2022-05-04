"""
Implementation of GetRecord verb
"""
from datetime import datetime
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse
from .exceptions import OAIErrorIdDoesNotExist, OAIErrorCannotDisseminateFormat
from .helpers import granularity_format


class RecordHeaderValidator:
    """Validator for the RecordHeader class"""
    def errors(self):
        """
        Verify fields are valid and present where required. Returning a list of descriptive
        errors if any issues were found.
        """
        failures = []
        failures.extend(self._identifier_failures())
        failures.extend(self._datestamp_failures())
        failures.extend(self._setspecs_failures())
        failures.extend(self._status_failures())
        return failures

    def _metadata_identifier_failures(self):
        """Return a list of identifier failures"""
        # TODO
        return []

    def _datestamp_failures(self):
        """Return a list of datestamp failures"""
        # TODO
        return []

    def _setspecs_failures(self):
        """Return a list of setspecs failures"""
        # TODO
        return []

    def _status_failures(self):
        """Return a list of setspecs failures"""
        return ["RecordHeader.status can only be None or 'deleted'"] \
            if self.status and self.status != "deleted" else []


class GetRecordRequest(OAIRequest):
    """
    Parse a request for the GetRecord verb
    raises:
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
    raises:
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

        granularity = self.repository.data.get_identify().granularity
        xmlb = etree.Element("GetRecord")
        # Header
        header(self.repository, identifier, xmlb)
        # Metadata
        xmeta = etree.SubElement(xmlb, "metadata")
        xmeta.append(
            self.repository.data.get_record_metadata(identifier, metadataprefix)
        )
        # About
        abouts = self.repository.data.get_record_abouts(identifier)
        for about in abouts:
            xabout = etree.SubElement(xmlb, "about")
            xabout.append(about)

        return xmlb

def header(repository: "OAIRepository", identifier: str, xmlb: etree._Element):
    """
    Generate and append a <header> OAI element to and XML doc.
    Args:
        identifier (str): A valid identifier string
        xmlb (lxml.etree._Element): The element to add the header to
    Returns:
        A lxml.etree._Element for the root of the header
    """
    head = repository.data.get_record_header(identifier)
    xhead = etree.SubElement(xmlb, "header")
    xident = etree.SubElement(xhead, "identifier")
    xident.text = head.identifier
    xstamp = etree.SubElement(xhead, "datestamp")
    xstamp.text = granularity_format(
        repository.data.get_identify().granularity,
        head.datestamp
    ) if isinstance(head.datestamp, datetime) else head.datestamp
    for setspec in head.setspecs:
        xset = etree.SubElement(xhead, "setSpec")
        xset.text = setspec
