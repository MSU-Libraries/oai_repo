"""
Implementation of Identify verb
"""
from datetime import datetime
from io import BytesIO
from lxml import etree
import validators
from .request import OAIRequest
from .response import OAIResponse
from .api import apicall_querypath

class IdentifyValidator:
    """Validator for the Identify class"""
    @property
    def protocol_version(self):
        """OAI Protocol version is constant"""
        return "2.0"

    def errors(self):
        """
        Verify fields are valid and present where required. Returning a list of descriptive
        errors if any issues were found.
        """
        failures = []
        if not self.repository_name or not isinstance(self.repository_name, str):
            failures.append("repository_name must be a non-empty string")
        if not isinstance(self.base_url, str) or not validators.url(self.base_url):
            failures.append("base_url must be a valid URL path")
        failures.extend(self._admin_email_failures())
        failures.extend(self._deleted_record_failures())
        failures.extend(self._granularity_failures())
        failures.extend(self._compression_failures())
        failures.extend(self._earliest_datestamp_failures())
        failures.extend(self._description_failures())
        return failures

    def _admin_email_failures(self):
        """Return a list of admin_email failures"""
        failures = []
        if not self.admin_email or not isinstance(self.admin_email, list):
            failures.append("admin_email must be a list with at list one valid email address")
        else:
            for email in self.admin_email:
                if not validators.email(email):
                    failures.append(f"invalid address for admin_email: {email}")
        return failures

    def _deleted_record_failures(self):
        """Return a list of deleted_record failures"""
        allowed_deleted_record = ["no", "persistent", "transient"]
        return [f"deleted_record  must be one of {', '.join(allowed_deleted_record)}"] \
            if self.deleted_record not in allowed_deleted_record else []

    def _granularity_failures(self):
        """Return a list of granularity failures"""
        allowed_granularity = ["YYYY-MM-DD", "YYYY-MM-DDThh:mm:ssZ"]
        return [f"granularity must be either of: {', '.join(allowed_granularity)}"] \
            if self.granularity not in allowed_granularity else []

    def _compression_failures(self):
        """Return a list of compression failures"""
        return [f"compression does not allow 'identity' as a value; it is implied"] \
            if "identity" in self.compression else []

    def _earliest_datestamp_failures(self):
        """Return a list of earliest_datestamp failures"""
        failures = []
        try:
            if not isinstance(self.granularity, datetime):
                if self.granularity == "YYYY-MM-DD":
                    datetime.strptime(self.earliest_datestamp, "%Y-%m-%d")
                elif self.granularity == "YYYY-MM-DDThh:mm:ssZ":
                    datetime.strptime(self.earliest_datestamp, "%Y-%m-%dT%H:%M:%SZ")
        except (TypeError, ValueError):
            failures.append(
                "earliest_datestamp must be a valid datestamp "
                "in the format specified by granularity"
            )
        return failures

    def _description_failures(self):
        """Return a list of description failures"""
        failures = []
        for idx, desc in enumerate(self.description):
            if not isinstance(desc, etree._Element):
                if isinstance(desc, BytesIO):
                    desc.seek(0)
                    desc = desc.read()
                try:
                    etree.fromstring(desc)
                except etree.XMLSyntaxError:
                    failures.append(f"description {idx} is not valid XML")
        return failures


class IdentifyRequest(OAIRequest):
    """
    Parse a request for the Idenfify verb
    raises:
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
