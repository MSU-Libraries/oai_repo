"""
Validators for oai_repo interface data classes
"""
import re
from datetime import datetime
from lxml import etree
import validators
from .helpers import bytes_to_xml


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


class MetadataFormatValidator:
    """Validator for the MetadataFormat class"""
    def errors(self):
        """
        Verify fields are valid and present where required. Returning a list of descriptive
        errors if any issues were found.
        """
        failures = []
        failures.extend(self._metadata_prefix_failures())
        failures.extend(self._schema_failures())
        failures.extend(self._metadata_namespace_failures())
        return failures

    def _metadata_prefix_failures(self):
        """Return a list of metadata_prefix failures"""
        pattern = re.compile(r"^[A-Za-z0-9-_.!~*'\(\)]+$")
        return [] if pattern.search(self.metadata_prefix) is not None else \
            ["metadata_prefix contains invalid character(s); allowed chars: A-Za-z0-9-_.!~*'()"]

    def _schema_failures(self):
        """Return a list of schema failures"""
        return ["schema must be a valid URL"] \
            if not validators.url(self.schema, simple_host=True) else []

    def _metadata_namespace_failures(self):
        """Return a list of metadata_namespace failures"""
        return ["metadata_namespace must be a valid URL"] \
            if not validators.url(self.metadata_namespace, simple_host=True) else []


class RecordHeaderValidator:
    """Validator for the RecordHeader class"""
    def errors(self):
        """
        Verify fields are valid and present where required. Returning a list of descriptive
        errors if any issues were found.
        """
        failures = []
        failures.extend(self._identifier_failures())
        failures.extend(self._datestamp_failures())
        failures.extend(self._setspecs_failures())
        failures.extend(self._status_failures())
        return failures

    def _metadata_identifier_failures(self):
        """Return a list of identifier failures"""
        # TODO
        return []

    def _datestamp_failures(self):
        """Return a list of datestamp failures"""
        # TODO
        return []

    def _setspecs_failures(self):
        """Return a list of setspecs failures"""
        # TODO
        return []

    def _status_failures(self):
        """Return a list of setspecs failures"""
        return ["RecordHeader.status can only be None or 'deleted'"] \
            if self.status and self.status != "deleted" else []


class SetValidator:
    """Validator for the Set class"""
    def errors(self):
        """
        Verify fields are valid and present where required. Returning a list of descriptive
        errors if any issues were found.
        """
        failures = []
        failures.extend(self._spec_failures())
        failures.extend(self._name_failures())
        failures.extend(self._description_failures())
        return failures

    def _spec_failures(self):
        """Return a list of spec failures"""
        # TODO
        return []

    def _name_failures(self):
        """Return a list of name failures"""
        # TODO
        return []

    def _description_failures(self):
        """Return a list of description failures"""
        # TODO
        return []
