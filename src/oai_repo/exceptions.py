"""
OAI Exceptions and Errors
"""

class OAIRepoException(Exception):
    """Base class for oai_repo exceptions"""

class OAIRepoInternalException(OAIRepoException):
    """Base class for internal failures to oai_repo"""

class OAIRepoExternalException(OAIRepoException):
    """Base class for failures external to oai_repo"""

class OAIError(Exception):
    """Shared base class for official OAI errors."""
    @classmethod
    def code(cls):
        """
        Return the OAI error code for the current exception.
        E.g. "OAIErrorBadArgument" => "badArgument"
        """
        name = cls.__name__.removeprefix("OAIError")
        return name[:1].lower() + name[1:]

class OAIErrorBadArgument(OAIError):
    """Class for OAI badArgument"""

class OAIErrorBadResumptionToken(OAIError):
    """Class for OAI badResumptionToken"""

class OAIErrorBadVerb(OAIError):
    """Class for OAI badVerb"""

class OAIErrorCannotDisseminateFormat(OAIError):
    """Class for OAI cannotDisseminateFormat"""

class OAIErrorIdDoesNotExist(OAIError):
    """Class for OAI idDoesNotExist"""

class OAIErrorNoRecordsMatch(OAIError):
    """Class for OAI noRecordsMatch"""

class OAIErrorNoMetadataFormats(OAIError):
    """Class for OAI noMetadataFormats"""

class OAIErrorNoSetHierarchy(OAIError):
    """Class for OAI noSetHierarchy"""
