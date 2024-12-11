"""
Implementation of ListMetadataFormats verb
"""
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse
from .exceptions import (
    OAIErrorIdDoesNotExist,
    OAIErrorNoMetadataFormats,
    OAIRepoInternalException
)


class ListMetadataFormatsRequest(OAIRequest):
    """
    Parse a request for the ListMetadataFormats verb

    Raises:
        OAIErrorBadArgument
    """
    def __init__(self):
        super().__init__()
        self.optional_args = ['identifier']
        self.identifier: str = None

    def post_parse(self):
        """Runs after args are parsed"""
        if self.args:
            self.identifier = self.args["identifier"]

    def __repr__(self):
        return f"ListMetadataFormatsRequest(identifier={self.identifier})"


class ListMetadataFormatsResponse(OAIResponse):
    """
    Generate a resposne for the ListMetadataFormats verb

    Raises:
        OAIErrorIdDoesNotExist
        OAIErrorNoMetadataFormats
    """
    def __repr__(self):
        return f"ListMetadataFormatsResponse(identifier={self.request.identifier})"

    def body(self) -> etree.Element:
        """Response body"""
        identifier = self.request.identifier
        if identifier and not self.repository.data.is_valid_identifier(identifier):
            raise OAIErrorIdDoesNotExist("The given identifier does not exist.")

        mdformats = self.repository.data.get_metadata_formats(identifier)
        if not mdformats:
            raise OAIErrorNoMetadataFormats("No metadata fomats found for given identifier.")

        xmlb = etree.Element("ListMetadataFormats")
        for mdformat in mdformats:
            # Report errors if any MetadataFormat object were invalid
            errors = mdformat.errors()
            if errors:
                raise OAIRepoInternalException(f"Invalid MetadataFormat instance: {errors}")
            self.add_format(xmlb, mdformat)
        return xmlb

    def add_format(self, xmlb: etree.Element, mdformat: dict):
        """
        Add the given metadta format to the provided xml element
        """
        mdf_elem = etree.SubElement(xmlb, "metadataFormat")
        elem = etree.SubElement(mdf_elem, "metadataPrefix")
        elem.text = mdformat.metadata_prefix
        elem = etree.SubElement(mdf_elem, "schema")
        elem.text = mdformat.schema
        elem = etree.SubElement(mdf_elem, "metadataNamespace")
        elem.text = mdformat.metadata_namespace
