"""
OAI Exceptions and Errors
"""

class OAIRepoInternalError(Exception):
    """Base class for internal errors to oai_repo"""

class OAIException(Exception):
    """Shared base class for official OAI errors."""
    @classmethod
    def code(cls):
        """
        Return the OAI error code for the current exception.
        E.g. "OAIErrorBadArgument" => "badArgument"
        """
        name = cls.__name__.removeprefix("OAIError")
        return name[:1].lower() + name[1:]

class OAIErrorBadArgument(OAIException):
    """Class for OAI badArgument"""

class OAIErrorBadResumptionToken(OAIException):
    """Class for OAI badResumptionToken"""

class OAIErrorBadVerb(OAIException):
    """Class for OAI badVerb"""

class OAIErrorCannotDisseminateFormat(OAIException):
    """Class for OAI cannotDisseminateFormat"""

class OAIErrorIdDoesNotExist(OAIException):
    """Class for OAI idDoesNotExist"""

class OAIErrorNoRecordsMatch(OAIException):
    """Class for OAI noRecordsMatch"""

class OAIErrorNoMetadataFormats(OAIException):
    """Class for OAI noMetadataFormats"""

class OAIErrorNoSetHierarchy(OAIException):
    """Class for OAI noSetHierarchy"""
