"""
Implementation of ListMetadataFormats verb
"""
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse
from .api import apicall_querypath
from .exceptions import OAIErrorIdDoesNotExist, OAIErrorNoMetadataFormats


class ListMetadataFormatsRequest(OAIRequest):
    """
    Parse a request for the ListMetadataFormats verb
    raises:
        OAIErrorBadArgument
        OAIErrorIdDoesNotExist
        OAIErrorNoMetadataFormats
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
        return f"ListMetadataFormatsResponse(identifier={self.identifier})"


class ListMetadataFormatsResponse(OAIResponse):
    """
    Generate a resposne for the ListMetadataFormats verb
    raises:
        OAIErrorIdDoesNotExist
        OAIErrorNoMetadataFormats
    """
    VALID_ELEMENTS = ["metadataPrefix", "schema", "metadataNamespace"]

    def __repr__(self):
        return f"ListMetadataFormatsResponse(identifier={self.request.identifier})"

    def body(self) -> etree.Element:
        """Response body"""
        xmlb = etree.Element("ListMetadataFormats")
        if not self.request.identifier:
            for mdformat in self.repository.config.metadataformats:
                self.add_format(xmlb, mdformat)
        else:
            local_id = self.repository.local_id(self.request.identifier)
            mdquery = self.repository.config.metadataformatsquery
            # Check if identifier exists
            idexists = mdquery["idExists"]
            idexists["url"] = idexists["url"].replace("$LOCAL_ID$", local_id)
            id_match = apicall_querypath(**idexists)
            if not id_match:
                raise OAIErrorIdDoesNotExist("The given identifier does not exist.")

            # Query to get list of formats
            fieldvalues = mdquery["fieldValues"]
            fieldvalues["url"] = fieldvalues["url"].replace("$LOCAL_ID$", local_id)
            metadata_formats = apicall_querypath(**fieldvalues)
            if not metadata_formats:
                raise OAIErrorNoMetadataFormats("No metadata fomats found for given identifier.")

            for mdformat in self.repository.config.metadataformats:
                if mdformat["fieldValue"] not in metadata_formats:
                    continue
                self.add_format(xmlb, mdformat)
        return xmlb

    def add_format(self, xmlb: etree.Element, mdformat: dict):
        """
        Add the given metadta format to the provided xml element
        """
        mdf_elem = etree.SubElement(xmlb, "metadataFormat")
        for mkey, mval in mdformat.items():
            if mkey not in self.VALID_ELEMENTS:
                continue
            elem = etree.SubElement(mdf_elem, mkey)
            elem.text = mval
