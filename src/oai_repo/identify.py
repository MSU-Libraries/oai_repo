"""
Implementation of Identify verb
"""
from datetime import datetime
from lxml import etree
import validators
from .request import OAIRequest
from .response import OAIResponse
from .exceptions import OAIRepoInternalException
from .helpers import bytes_to_xml, granularity_format

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
        if (
            not isinstance(self.base_url, str) or
            not validators.url(self.base_url, simple_host=True)
        ):
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
            try:
                bytes_to_xml(desc)
            except etree.XMLSyntaxError as exc:
                failures.append(f"description {idx} is not valid XML: {exc}")
        return failures


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
            edvalue = granularity_format(granularity, edvalue)
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
