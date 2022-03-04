"""
Implementation of ListMetadataFormats verb
"""
from .oaiverb import OAIVerb
from ..exceptions import OAIErrorBadArgument, OAIErrorIdDoesNotExist, OAIErrorNoMetadataFormats

class ListMetadataFormats(OAIVerb):
    """
    raises:
        OAIErrorBadArgument
        OAIErrorIdDoesNotExist
        OAIErrorNoMetadataFormats
    """
    def __init__(self):
        super().__init__(__class__.__name__)
