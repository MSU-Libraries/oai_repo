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
from .listsets import SetValidator


@dataclass
class Identify(IdentifyValidator):
    """
    The info needed for the Identify verb. In your OAIInterface.get_identify_instance() method
    create an instance of this class, set appropriate data, and return it.
    """
    repository_name: str = None
    base_url: str = None
    admin_email: list = field(default_factory=list)
    earliest_datestamp: str|datetime = None
    deleted_record: str = None
    granularity: str = None
    compression: list = field(default_factory=list)
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
    identifier: str = None
    datestamp: str|datetime = None
    setspecs: list[str] = field(default_factory=list)
    status: str = None

@dataclass
class Set(SetValidator):
    """
    Class to define fields for an OAI set. Your definition of the
    OAIInterface.get_metadata_formats() method should return a list of these.
    """
    spec: str = None
    name: str = None
    description: list = None
    """A list of lxml.etree.Elements to populate `<setDescription>` tags for the set."""


class DataInterface:
    """
    Class in which all required OAI data retrieval actions must be implemented.
    The instantiated instance of this class is then passed to the
    OAI repository.
    """
    # Max number of results to return per request for: ListSets, ListIdentifiers, ListRecords
    limit: int = 50

    def get_identify(self) -> Identify:
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

    def get_metadata_formats(self, identifier: str|None = None) -> list[MetadataFormat]:
        """
        Return a list of metadata prefixes for the identifier. If no identifier
        identifieris passed, then list must contain all possible prefixes for the repository.
        Args:
            identifier (str|None): An identifer string
        Returns:
            A list of instantiated MetadataFormat objects with all properties set appropriately
            to the identifer.
            If identifier is None, then list of all possible MetadataFormat objects for the
            entire repository.
        """
        raise NotImplementedError

    def get_record_header(self, identifier: str) -> RecordHeader:
        """
        Return a RecordHeader instance for the identifier.
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
        Return a list of XML elements which will populate the `<about>` tags in GetRecord responses.
        Args:
            identifier (str): A valid identifier string
        Returns:
            A list of lxml.etree.Elements to populate `<about>` tags for the record.
        Important:
            oai_repo will wrap the response with a `<about>` tag; do not add it yourself.
        """
        raise NotImplementedError

    def list_set_specs(self, identifier: str=None, cursor: int=0) -> tuple:
        """
        Return a list of setSpec string for the given identifier string if provided,
        or the list of all valid setSpec strings for the repository if no identifier is None.
        Args:
            identifier (str): a valid identifier string
            cursor (int): position in results to start from
        Returns:
            A tuple of length 3:
             1. (list|None) List of setSpec strings or None if the repository does not support sets.
                or None if no `resuptionToken` is needed.
             2. (int|None) The `completeListSize` for a `resumptionToken` or Null to not send.
             3. (Any|None) An str()-able value which indicates the constant-ness of the complete
                result set. If any value in the results changes, this value should also
                change. A changed value will invalidate current `resumptionToken`s.
                If None, the `resumptionToken`s will only invalidate based on
                reduction in in `completeListSize`.
        """
        raise NotImplementedError

    def get_set(self, setspec: str) -> Set:
        """
        Return an instatiated OAI Set object for the provided setSpect string.
        Args:
            setspec (str): a setSpec string
        Returns:
            The Set object with all properties set appropriately,
            or None if the setspec is not valid or does not exist.
        """
        raise NotImplementedError

    def list_identifiers(self,
        metadataprefix: str,
        filter_from: datetime = None,
        filter_until: datetime = None,
        filter_set: str = None,
        cursor: int = 0
    ) -> tuple:
        """
        Return valid identifier strings, filtered appropriately to passed parameters.
        Args:
            metadataprefix (str): The metadata prefix to match.
            filter_from (datetime.datetime): Include only identifiers on or after given datetime.
            filter_until (datetime.datetime): Include only identifiers on or before given datetime.
            filter_set (str): Include only identifers within the matching setSpec string.
            cursor (int): position in results to start retrieving from
        Returns:
            A tuple of length 3:
             1. (list) Valid identifier strings for the repository, filtered appropriately.
                or None if no `resuptionToken` is needed.
             2. (int|None) The `completeListSize` for a `resumptionToken` or Null to not send.
             3. (Any|None) An str()-able value which indicates the constant-ness of the complete
                result set. If any value in the results changes, this value should also
                change. A changed value will invalidate current `resumptionToken`s.
                If None, the `resumptionToken`s will only invalidate based on
                reduction in in `completeListSize`.
        """
        raise NotImplementedError
