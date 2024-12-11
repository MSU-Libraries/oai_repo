"""
Implementation of Identify verb
"""
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse
from .exceptions import OAIRepoInternalException
from .helpers import bytes_to_xml, granularity_format


class IdentifyRequest(OAIRequest):
    """
    Parse a request for the Idenfify verb

    Raises:
        OAIErrorBadArgument
    """
    def post_parse(self):
        """Runs after args are parsed"""


class IdentifyResponse(OAIResponse):
    """Generate a resposne for the Identify verb"""
    def __repr__(self):
        return "IdentifyResponse()"

    def body(self):
        """Response body"""
        identify = self.repository.data.get_identify()
        errors = identify.errors()
        if errors:
            raise OAIRepoInternalException(f"Invalid Identify instance: {errors}")

        # Assemble the XML body
        xmlb = etree.Element("Identify")
        repository_name = etree.SubElement(xmlb, "repositoryName")
        repository_name.text = identify.repository_name
        baseurl = etree.SubElement(xmlb, "baseURL")
        baseurl.text = identify.base_url
        protocol_version = etree.SubElement(xmlb, "protocolVersion")
        protocol_version.text = identify.protocol_version
        for email in identify.admin_email:
            adminemail = etree.SubElement(xmlb, "adminEmail")
            adminemail.text = email
        edvalue = identify.earliest_datestamp
        if not isinstance(edvalue, str):
            edvalue = granularity_format(identify.granularity, edvalue)
        earliestdatestamp = etree.SubElement(xmlb, "earliestDatestamp")
        earliestdatestamp.text = edvalue
        deletedrecord = etree.SubElement(xmlb, "deletedRecord")
        deletedrecord.text = identify.deleted_record
        granularity = etree.SubElement(xmlb, "granularity")
        granularity.text = identify.granularity
        for compress_type in identify.compression:
            compression = etree.SubElement(xmlb, "compression")
            compression.text = compress_type
        for desc in identify.description:
            desc_elem = etree.SubElement(xmlb, "description")
            desc_elem.append(bytes_to_xml(desc))
        return xmlb
