"""
Interface DataClasses used by the OAI DataInterface
"""
from io import BytesIO
from datetime import datetime
from dataclasses import dataclass, field
import lxml
from .validators import (
    IdentifyValidator, MetadataFormatValidator,
    RecordHeaderValidator, SetValidator
)


@dataclass
class Identify(IdentifyValidator):
    """
    The info needed for the Identify verb. In your `DataInterface.get_identify_instance()`
    method create an instance of this class, set appropriate data, and return it.

    Attributes:
        repository_name (str): The name of the OAI repository
        base_url (str): the base url for this repository
        admin_email (list): a list of email addresses, cannot be empty
        earliest_datestamp (str|datetime): a string in the granularity format or a datetime object
        deleted_record (str): OAI deleted record value, one of `no`, `persistent`, `transient`
        granularity (str): OAI granularity, either `YYYY-MM-DDThh:mm:ssZ` or `YYYY-MM-DD`
        compression (list): compression to be available (typically left empty)
        description (list): can be bytes data or a pre-loaded lxml Element

    **Examples:**
    ```python
    ident = oai_repo.Identify()
    ident.repository_name = "My Repo"
    ident.base_url = f"https://example.edu/oai"
    ident.deleted_record = "no"
    ident.granularity = "YYYY-MM-DDThh:mm:ssZ"
    ident.compression = []
    ... # remaining attributes
    ```
    """
    repository_name: str = None
    base_url: str = None
    admin_email: list = field(default_factory=list)
    earliest_datestamp: str|datetime = None
    deleted_record: str = None
    granularity: str = None
    compression: list = field(default_factory=list)
    description: list[BytesIO|bytes|lxml.etree._Element] = field(default_factory=list)

@dataclass
class MetadataFormat(MetadataFormatValidator):
    """
    Class to define fields necessary for an OAI metadata format. Your definition of the
    `DataInterface.get_metadata_formats()` method should return a list of these.

    Attributes:
        metadata_prefix (str): A metadataPrefix string
        schema (str): The schema for the metadata
        metadata_namespace (str): The namespace for the metadata

    **Examples:**
    ```python
    mdf = oai_repo.MetadataFormat(
        "oai_dc",
        "http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
        "http://www.openarchives.org/OAI/2.0/oai_dc/"
    )
    ```
    """
    metadata_prefix: str = None
    schema: str = None
    metadata_namespace: str = None

@dataclass
class RecordHeader(RecordHeaderValidator):
    """
    Class to define a record header for an identifier. Your definition of the
    `DataInterface.get_record_header()` method should one of these.

    Attributes:
        identifier (str): The OAI identifier
        datestamp (str|datetime): The datestamp for when this record was created or last modified
        setspecs (list[str]): A list of setspec strings this recdord is part of
        status (str): The optional OAI status
    """
    identifier: str = None
    datestamp: str|datetime = None
    setspecs: list[str] = field(default_factory=list)
    status: str = None

@dataclass
class Set(SetValidator):
    """
    Class to define fields for an OAI set. Your definition of the
    `DataInterface.get_metadata_formats()` method should return a list of these.

    Attributes:
        spec (str): The setspec string
        name (str): The name associated with the setspec
        description (list): A list of lxml.etree.Elements to populate 
                            `<setDescription>` tags for the set.
    """
    spec: str = None
    name: str = None
    description: list = None
