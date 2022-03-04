"""
OAI Exceptions and Errors
"""

class OAIException(Exception):
    pass

class OAIErrorBadArgument(OAIException):
    pass

class OAIErrorBadResuptionToken(OAIException):
    pass

class OAIErrorBadVerb(OAIException):
    pass

class OAIErrorCannotDisseminateFormat(OAIException):
    pass

class OAIErrorIdDoesNotExist(OAIException):
    pass

class OAIErrorNoRecordsMatch(OAIException):
    pass

class OAIErrorNoMetadataFormats(OAIException):
    pass

class OAIErrorNoSetHierarchy(OAIException):
    pass
