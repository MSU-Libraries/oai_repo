"""
Implementation of ListMetadataFormats verb
"""
from lxml import etree
from .exceptions import OAIErrorBadArgument, OAIErrorIdDoesNotExist, OAIErrorNoMetadataFormats
from .request import OAIRequest
from .response import OAIResponse


class ListMetadataFormatsRequest(OAIRequest):
    """
    raises:
        OAIErrorBadArgument
        OAIErrorIdDoesNotExist      # Here or Response?
        OAIErrorNoMetadataFormats   # Here or Response?
    """
    def __init__(self):
        super().__init__()
        self.optional_args = ['identifier']


class ListMetadataFormatsResponse(OAIResponse):
    """
    """
    def __repr__(self):
        return f"ListMetadataFormatsResponse()"

    def body(self):
        """Response body"""
        xmlb = etree.Element("ListMetadataFormats")
        # With no identifer given
        if not self.request.args:
            for mformat in self.repository.config.metadataformats:
                metadataformat = etree.SubElement(xmlb, "metadataFormat")
                for mkey, mval in mformat.items():
                    elem = etree.SubElement(metadataformat, mkey)
                    elem.text = mval
        # TODO Invalid identifier
        # TODO Valid identifier
        return xmlb
