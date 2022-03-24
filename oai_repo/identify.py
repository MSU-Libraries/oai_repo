"""
Implementation of Identify verb
"""
import json
import requests
from lxml import etree
from .exceptions import OAIErrorBadArgument
from .request import OAIRequest
from .response import OAIResponse
from . import helpers


class IdentifyRequest(OAIRequest):
    """
    Parse a request for the Idenfify verb
    raises:
        OAIErrorBadArgument
    """
    def __init__(self):
        super().__init__()


class IdentifyResponse(OAIResponse):
    """Generate a resposne for the Identify verb"""
    def __repr__(self):
        return f"IdentifyResponse()"

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
        Raises:
            OAIRepoInternalError on API call or parse failure
        """
        edconfig = self.repository.config.earliestdatestamp
        earliestdatestamp = etree.SubElement(xmlb, "earliestDatestamp")
        if "static" in edconfig:
            earliestdatestamp.text = edconfig["static"]
        else:
            try:
                resp = requests.get(edconfig["url"], timeout=10)
            except requests.RequestException as exc:
                raise OAIRepoInternalError(f"Call to API failed: {edconfig['url']}")
            if not resp.status_code == 200:
                raise OAIRepoInternalError(f"Call to API returned {resp.status_code}: {edconfig['url']}")
            if 'jsonpath' in edconfig:
                loaded = json.loads(resp.text)
                earliestdatestamp.text = helpers.jsonpath_find_first(loaded, edconfig["jsonpath"])
                # TODO json load failure and jsonpath syntax failure
            elif 'xpath' in edconfig:
                loaded = etree.fromstring(resp.content)
                earliestdatestamp.text = helpers.xpath_find_first(loaded, edconfig["xpath"])
                # TODO xml load failure and xpath syntax failure

    def add_description_elements(self, xmlb: etree.Element):
        """
        """
