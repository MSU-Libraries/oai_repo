"""
Interface to be implemented by OAI instance developer
"""
from datetime import datetime
import lxml
from .interfacedata import Identify, MetadataFormat, RecordHeader, Set


class DataInterface:
    """
    Class in which all required OAI data retrieval actions must be implemented.
    The instantiated instance of this class is then passed to the
    OAI repository.

    Attributes:
        limit (int): Max number of results to return per request for
                     ListSets, ListIdentifiers, ListRecords
    """
    limit: int = 100

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
        identifier is passed, then list must contain all possible prefixes for the repository.

        Args:
            identifier (str|None): An identifer string

        Returns:
            A list of instantiated MetadataFormat objects with all properties
                set appropriately to the identifer.
                If identifier is None, then list of all possible MetadataFormat
                objects for the entire repository.
        """
        raise NotImplementedError

    def get_record_header(self, identifier: str) -> RecordHeader:
        """
        Return a RecordHeader instance for the identifier.

        Args:
            identifier (str): A valid identifier string

        Returns:
            The RecordHeader object with all properties set appropriately.

        Note:
            If you implement `get_records_header`, you may not need this
            method implemented. By default, `get_records_header` is the
            only method which calls `get_record_header`.
        """
        raise NotImplementedError

    def get_records_header(self, identifiers: list[str]) -> list[RecordHeader]:
        """
        Return a list of RecordHeader instances for the identifiers.

        Args:
            identifier (list): A list of valid identifier strings

        Returns:
            A list of the RecordHeader objects with all properties set appropriately.

        Note:
            Implementing this function in your DataInterface is _optional_. You may
            want to implement a custom version if pulling record headers is individually
            slow and could be accomplished faster in bulk.
        """
        return [self.get_record_header(identifier) for identifier in identifiers]

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

        Note:
            If you implement `get_records_metadata`, you may not need this
            method implemented. By default, `get_records_metadata` is the
            only method which calls `get_record_metadata`.
        """
        raise NotImplementedError

    def get_records_metadata(self, identifiers: list[str], metadataprefix: str) \
        -> list[lxml.etree._Element|None]:
        """
        Return a list of lxml.etree.Element representing the root elements for the
        metadata found for the requested prefix and identifers.

        Args:
            identifiers (list): A list of valid identifer strings
            metadataprefix (str): A metadata prefix

        Returns:
            list containing the lxml.etree.Element for each requested record metadata,
                or None for records which have no metadata for provided prefix.

        Note:
            Implementing this function in your DataInterface is _optional_. You may
            want to implement a custom version if pulling record metadata is individually
            slow and could be accomplished faster in bulk.
        """
        return [self.get_record_metadata(identifier, metadataprefix) for identifier in identifiers]

    def get_record_abouts(self, identifier: str) -> list[lxml.etree._Element]:
        """
        Return a list of XML elements which will populate the `<about>` tags in GetRecord responses.

        Args:
            identifier (str): A valid identifier string

        Returns:
            A list of lxml.etree.Elements to populate `<about>` tags for the record.

        Important:
            oai_repo will wrap the response with a `<about>` tag; do not add it yourself.

        Note:
            If you implement `get_records_abouts`, you may not need this
            method implemented. By default, `get_records_abouts` is the
            only method which calls `get_record_abouts`.
        """
        raise NotImplementedError

    def get_records_abouts(self, identifiers: list[str]) -> list[list[lxml.etree._Element]]:
        """
        Return a list of XML elements which will populate the `<about>` tags in GetRecord responses.

        Args:
            identifier (list): A list of valid identifier strings

        Returns:
            A list of lists, each being the lxml.etree.Elements to populate `<about>` tags for
            the record in the first list.

        Important:
            oai_repo will wrap each response with a `<about>` tag; do not add them yourself.

        Note:
            Implementing this function in your DataInterface is _optional_. You may
            want to implement a custom version if pulling record metadata is individually
            slow and could be accomplished faster in bulk.
        """
        return [self.get_record_abouts(identifier) for identifier in identifiers]

    def list_set_specs(self, identifier: str=None, cursor: int=0) -> tuple:
        """
        Return a list of setSpec string for the given identifier string if provided,
        or the list of all valid setSpec strings for the repository if no identifier is None.

        Args:
            identifier (str): a valid identifier string
            cursor (int): position in results to start from

        Returns:
            A tuple of length 3:

                1. (list|None) List of setSpec strings or None if the repository does not support
                    sets, or None if no `resuptionToken` is needed.
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
        Return an instatiated OAI Set object for the provided setSpec string.

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

                1. (list) Valid identifier strings for the repository, filtered appropriately,
                    or None if no `resuptionToken` is needed.
                2. (int|None) The `completeListSize` for a `resumptionToken` or Null to not send.
                3. (Any|None) An str()-able value which indicates the constant-ness of the complete
                    result set. If any value in the results changes, this value should also
                    change. A changed value will invalidate current `resumptionToken`s.
                    If None, the `resumptionToken`s will only invalidate based on
                    reduction in in `completeListSize`.
        """
        raise NotImplementedError
