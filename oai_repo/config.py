"""
Config file for OAI repository
"""
from copy import deepcopy
import json
import cerberus
from . import schemas
from .exceptions import OAIRepoInternalException

class OAIConfig:
    """
    Wrapper class for the config file
    """
    def __init__(self, filepath: str = None):
        self.filepath: str = filepath
        self._config: dict = {}
        self._defaults: dict = {
            "repositoryName": "Example OAI-PMH Repository",
            "baseURL": "http://example.edu/oai",
            "adminEmail": "admin@oai.example.edu",
            "metadataFormats": {},
            "earliestDatestamp": "1900-01-01T00:00:00Z",
            "deletedRecord": "no",
            "granularity": "YYYY-MM-DDThh:mm:ssZ",
            "compression": [],
            "description": [],
            "localId": {},
            "metadataFormatsQuery": {}
        }
        if self.filepath:
            self.load_file(self.filepath)

    def load_file(self, filepath: str):
        """
        Validate and load a config file
        Args:
            filepath: The path to the config file to load
        Raises:
            OAIRepoInternalException: If the config file could not be opened, parsed, or is invalid
        """
        self.filepath = filepath
        config = {}
        try:
            with open(self.filepath, 'r', encoding='utf8') as fileh:
                config = json.load(fileh)
        except FileNotFoundError:
            raise OAIRepoInternalException(f"Could not find config file: {self.filepath}") from None
        except json.JSONDecodeError as exc:
            raise OAIRepoInternalException(
                f"Unable to decode config file ({self.filepath}): {exc}"
            ) from None

        # Assert structure
        cerbval = cerberus.Validator(schemas.config_schema)
        if not cerbval.validate(config):
            raise OAIRepoInternalException(
                f"Invalid config file ({self.filepath}): {cerbval.errors}"
            )

        self._config = config

    def __getattr__(self, name):
        for key, default in self._defaults.items():
            if key.lower() == name:
                return deepcopy(self._config.get(key, default))
        raise AttributeError
