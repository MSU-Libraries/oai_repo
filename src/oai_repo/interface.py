"""
Interface to be implemented by OAI instance developer
"""
from io import BytesIO
from dataclasses import dataclass, field
from datetime import datetime
import lxml
from .identify import IdentifyValidator
from .listmetadataformats import MetadataFormatValidator
from .getrecord import RecordHeaderValidator
from .listsets import OAISetValidator


@dataclass
class Identify(IdentifyValidator):
    """
    The info needed for the Identify verb. In your OAIInterface.get_identify_instance() method
    create an instance of this class, set appropriate data, and return it.
    """
    repository_name: str = None
    base_url: str = None
    admin_email: list = field(default_factory=list)
    deleted_record: str = None
    granularity: str = None
    compression: list = field(default_factory=list)
    earliest_datestamp: str|datetime = None
    """earliest_datestamp: either a string in the granularity format, or a datetime object"""
    description: list[BytesIO|bytes|lxml.etree._Element] = field(default_factory=list)
    """description: can be bytes data or a pre-loaded lxml Element"""


@dataclass
class MetadataFormat(MetadataFormatValidator):
    """
    Class to define fields necessary for an OAI metadata format. Your definition of the
    OAIInterface.get_metadata_formats() method should return a list of these.
    """
    metadata_prefix: str = None
    schema: str = None
    metadata_namespace: str = None


@dataclass
class RecordHeader(RecordHeaderValidator):
    """
    Class to define a record header for an identifier. Your definition of the
    OAIInterface.get_record_header() method should one of these.
    """
    #TODO

@dataclass
class OAISet(OAISetValidator):
    """
    Class to define fields for an OAI set. Your definition of the
    OAIInterface.get_metadata_formats() method should return a list of these.
    """
    spec: str = None
    name: str = None
    description: list = None
    """A list of lxml.etree.Elements to populate `<setDescription>` tags for the set."""


class OAIInterface:
    """
    Class in which all required OAI metadata queries must be implemented.
    The instantiated instance of this class is then passed to the
    OAI repository.
    """
    def get_identify_instance(self) -> Identify:
        """
        Create and return an instantiated Identify object.
        Returns:
            The Identify object with all properties set appropriately
        """
        raise NotImplementedError

    def is_valid_identifier(self, identifier: str) -> bool:
        """
        Determine if an identifier string is valid format and exists.
        Args:
            identifier (str): A string to check for being an identifier
        Returns:
            True if given string is an identifier that exists.
        """
        raise NotImplementedError

    def list_metadata_prefixes(self, identifier: str|None = None) -> list[str]:
        """
        Return a list of metadata prefixes for the identifier. If no identifier
        identifieris passed, then list must contain all possible prefixes for the repository.
        Args:
            identifier (str|None): An identifer string
        Returns:
            A list of metadata prefixes for the passed identifier.
            A list of metadata prefixes for the entire reposiory if passed identifer was None.
            An empty list if no prefixes found or identifier did not exist.
        """
        raise NotImplementedError

    def get_metadata_format(self, metadata_prefix: str) -> MetadataFormat:
        """
        TODO
        Args:
            metadata_prefix (str):
        Returns:
            An instantiated MetadataFormat with all properties set appropriately.
        """
        raise NotImplementedError

    def get_record_header(self, identifier: str) -> RecordHeader:
        """
        TODO
        Args:
            identifier (str): A valid identifier string
        Returns:
            The RecordHeader object with all properties set appropriately.
        """
        raise NotImplementedError

    def get_record_metadata(self, identifier: str, metadataprefix: str) -> lxml.etree._Element|None:
        """
        Return a lxml.etree.Element representing the root element of the
        metadata found for the given prefix.
        Args:
            identifier (str): A valid identifer string
            metadataprefix (str): A metadata prefix
        Returns:
            The lxml.etree.Element for the requested record metadata,
            or None if record has no metadata for provided prefix.
        Important:
            oai_repo will wrap the response with a `<metadata>` tag; do not add it yourself.
        """
        raise NotImplementedError

    def get_record_abouts(self, identifier: str) -> list[lxml.etree._Element]:
        """
        TODO
        Args:
            identifier (str): A valid identifier string
        Returns:
            A list of lxml.etree.Elements to populate `<about>` tags for the record.
        Important:
            oai_repo will wrap the response with a `<about>` tag; do not add it yourself.
        """
        raise NotImplementedError

    def list_set_specs(self, identifier: str=None, cursor: int=0, limit: int=100) -> list[str]|None:
        """
        Return a list of setSpec string for the given identifier string if provided,
        or the list of all valid setSpec strings for the repository if no identifier is None.
        Args:
            identifier (str): a valid identifier string
            cursor (int): position in results to start from
            limit (int): maximum number of results to return, starting from cursor position
        Returns:
            A tuple of length 3.
             1. A list of setSpec strings or None if the repository does not support sets.
             2. A `cursor` (int) to send with a `resumptionToken`,
                or -1 if no `cursor` should be sent,
                or None if no `resuptionToken` is needed.
             3. The `completeListSize` to send with a `resuptionToken` or Null to not send.
        """
        raise NotImplementedError

    def get_set(self, setspec: str) -> OAISet:
        """
        Retrn an instatiated OAI Set object for the provided setSpect string.
        Args:
            setspec (str): a setSpec string
        Returns:
            The OAISet object with all properties set appropriately,
            or None if the setspec is not valid or does not exist.
        """
        raise NotImplementedError

    def list_identifiers(self,
        metadataprefix: str,
        filter_from: datetime = None,
        filter_until: datetime = None,
        filter_set: str = None,
        cursor: int = 0,
        limit: int = 100
    ) -> list:
        """
        TODO
        Args:
            metadataprefix (str):
            filter_from (datetime.datetime):
            filter_until (datetime.datetime):
            filter_set (str):
            cursor (int): position in results to start retrieving from
            limit (int): maximum number of results to return, starting from cursor position
        Returns:
            A tuple of length 3:
             1. A list of valid identifier strings for the repository, filtered appropriately.
             2. A `cursor` (int) to send with a `resumptionToken`,
                or -1 if no `cursor` should be sent,
                or None if no `resuptionToken` is needed.
             3. The `completeListSize` to send with a `resuptionToken`, or Null not send.
        """
        raise NotImplementedError
