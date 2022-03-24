"""
Implementation of Identify verb
"""
from lxml import etree
from .exceptions import OAIErrorBadArgument
from .request import OAIRequest
from .response import OAIResponse


class IdentifyRequest(OAIRequest):
    """
    raises:
        OAIErrorBadArgument
    """
    def __init__(self):
        super().__init__()


class IdentifyResponse(OAIResponse):
    """
    """
    def __repr__(self):
        return f"IdentifyResponse()"

    def body(self):
        """Response body"""
        xmlb = etree.Element("Identify")
        repository_name = etree.SubElement(xmlb, "repositoryName")
        repository_name.text = self.repository.config.name
        baseurl = etree.SubElement(xmlb, "baseUrl")
        baseurl.text = self.repository.config.baseurl
        protocol_version = etree.SubElement(xmlb, "protocolVersion")
        protocol_version.text = "2.0"
        admin_email = etree.SubElement(xmlb, "adminEmail")
        admin_email.text = self.repository.config.admin_email
        # TODO earlieestDatestamp
        # TODO deletedRecord
        # TODO granularity
        # TODO compression
        # TODO description
        return xmlb
