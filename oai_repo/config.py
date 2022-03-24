"""
Config file for OAI repository
"""
import json
import cerberus
from .schemas import config_schema
from .exceptions import OAIRepoInternalError

class OAIConfig:
    """
    Wrapper class for the config file
    """
    def __init__(self, filepath: str = None):
        self.filepath: str = filepath
        self.repositoryname: str = 'Example OAI-PMH Repository'
        self.baseurl: str = 'http://oai.example.edu'
        self.adminemail: str = 'admin@oai.example.edu'
        self.metadataformats: dict = {}
        self.earliestdatestamp: str|dict = "1900-01-01T00:00:00Z"
        self.deletedrecord: str = "no"
        self.granularity: str = "YYYY-MM-DDThh:mm:ssZ",
        self.compression: list = []
        self.description: list = []
        if self.filepath:
            self.load_file(self.filepath)

    def load_file(self, filepath: str):
        """
        Validate and load a config file
        Args:
            filepath: The path to the config file to load
        Raises:
            OAIRepoInternalError: If the config file could not be opened, parsed, or is invalid
        """
        self.filepath = filepath
        config = {}
        try:
            with open(self.filepath, 'r', encoding='utf8') as fileh:
                config = json.load(fileh)
        except FileNotFoundError:
            raise OAIRepoInternalError(f"Could not find config file: {self.filepath}") from None
        except json.JSONDecodeError as exc:
            raise OAIRepoInternalError(f"Unable to decode config file ({self.filepath}): {exc}") from None

        # Assert structure
        cerbval = cerberus.Validator(config_schema)
        if not cerbval.validate(config):
            raise OAIRepoInternalError(f"Invalid config file ({self.filepath}): {cerbval.errors}")

        # Set config properties
        self.name = config.get('repositoryName', self.repositoryname)
        self.baseurl = config.get('baseUrl', self.baseurl)
        self.adminemail = config.get('adminEmail', self.adminemail)
        self.metadataformats = config.get('metadataFormats', self.metadataformats)
        self.earliestdatestamp = config.get("earliestDatestamp", self.earliestdatestamp)
        self.deletedrecord = config.get("deletedRecord", self.deletedrecord)
        self.granularity = config.get("granularity", self.granularity)
        self.compression = config.get("compression", self.compression)
        self.description = config.get("description", self.description)
