"""
Implementation of ListMetadataFormats verb
"""
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse


class MetadataFormatValidator:
    """
    """


class ListMetadataFormatsRequest(OAIRequest):
    """
    Parse a request for the ListMetadataFormats verb
    raises:
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
    raises:
        OAIErrorIdDoesNotExist
        OAIErrorNoMetadataFormats
    """
    def __repr__(self):
        return f"ListMetadataFormatsResponse(identifier={self.request.identifier})"

    def body(self) -> etree.Element:
        """Response body"""
        xmlb = etree.Element("ListMetadataFormats")
        if not self.request.identifier:
            for mdf in self.repository.config.metadataformats:
                self.add_format(xmlb, mdf)
        else:
            self.repository.apiqueries.assert_identifier(self.request.identifier)
            metadataformats = self.repository.apiqueries.metadata_formats(self.request.identifier)
            for mdf in self.repository.config.metadataformats:
                localmetadataid = self.repository.localmetadataid(mdf["metadataPrefix"])
                if localmetadataid not in metadataformats:
                    continue
                self.add_format(xmlb, mdf)
        return xmlb

    def add_format(self, xmlb: etree.Element, mdformat: dict):
        """
        Add the given metadta format to the provided xml element
        """
        mdf_elem = etree.SubElement(xmlb, "metadataFormat")
        for mkey, mval in mdformat.items():
            elem = etree.SubElement(mdf_elem, mkey)
            elem.text = mval
