"""
Implementation of Identify verb
"""
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse
from .api import apicall_querypath


class IdentifyRequest(OAIRequest):
    """
    Parse a request for the Idenfify verb
    raises:
        OAIErrorBadArgument
    """
    # pylint: disable=useless-super-delegation
    def __init__(self):
        super().__init__()

    def post_parse(self):
        """Runs after args are parsed"""

class IdentifyResponse(OAIResponse):
    """Generate a resposne for the Identify verb"""
    def __repr__(self):
        return "IdentifyResponse()"

    def body(self):
        """Response body"""
        xmlb = etree.Element("Identify")
        repository_name = etree.SubElement(xmlb, "repositoryName")
        repository_name.text = self.repository.config.repositoryname
        baseurl = etree.SubElement(xmlb, "baseUrl")
        baseurl.text = self.repository.config.baseurl
        protocol_version = etree.SubElement(xmlb, "protocolVersion")
        protocol_version.text = "2.0"
        for email in self.repository.config.adminemail:
            adminemail = etree.SubElement(xmlb, "adminEmail")
            adminemail.text = email
        deletedrecord = etree.SubElement(xmlb, "deletedRecord")
        deletedrecord.text = self.repository.config.deletedrecord
        granularity = etree.SubElement(xmlb, "granularity")
        granularity.text = self.repository.config.granularity
        for compress_type in self.repository.config.compression:
            compression = etree.SubElement(xmlb, "compression")
            compression.text = compress_type
        self.add_earliest_datestamp_element(xmlb)
        self.add_description_elements(xmlb)
        return xmlb

    def add_earliest_datestamp_element(self, xmlb: etree.Element):
        """
        Add the earliestDatestamp field to the xml element based on config settings
        Raises:
            OAIRepoInternalError on API call or parse failure
        """
        edconfig = self.repository.config.earliestdatestamp
        earliestdatestamp = etree.SubElement(xmlb, "earliestDatestamp")
        if "static" in edconfig:
            earliestdatestamp.text = edconfig["static"]
        else:
            earliestdatestamp.text = apicall_querypath(**edconfig)

    def add_description_elements(self, xmlb: etree.Element):
        """
        Load XML files from config settings and add them as description elements to the xml element
        Raises:
            OAIRepoInternalError on failure
        """
        for desc_filepath in self.repository.config.description:
            desc_root = etree.parse(desc_filepath)
            for child_elem in desc_root.getroot():
                desc_element = etree.SubElement(xmlb, "description")
                desc_element.append(child_elem)
        # TODO catch xml errors
