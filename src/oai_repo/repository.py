"""
OAIRepository functionality
"""
from typing import NamedTuple
from .getrecord import GetRecordRequest, GetRecordResponse
from .identify import IdentifyRequest, IdentifyResponse
from .listidentifiers import ListIdentifiersRequest, ListIdentifiersResponse
from .listmetadataformats import ListMetadataFormatsRequest, ListMetadataFormatsResponse
from .listrecords import ListRecordsRequest, ListRecordsResponse
from .listsets import ListSetsRequest, ListSetsResponse
from .exceptions import (
    OAIError, OAIErrorBadVerb, OAIErrorIdDoesNotExist, OAIErrorCannotDisseminateFormat
)
from .error import OAIErrorResponse
from .request import OAIRequest
from .response import OAIResponse
from .config import OAIConfig
from .api import APIQueries
from .transform import Transform

class VerbClasses(NamedTuple):
    """Named access to verb classes"""
    request: OAIRequest
    response: OAIResponse

VERBS = {
    'GetRecord': VerbClasses(GetRecordRequest, GetRecordResponse),
    'Identify': VerbClasses(IdentifyRequest, IdentifyResponse),
    'ListIdentifiers': VerbClasses(ListIdentifiersRequest, ListIdentifiersResponse),
    'ListMetadataFormats': VerbClasses(ListMetadataFormatsRequest, ListMetadataFormatsResponse),
    'ListRecords': VerbClasses(ListRecordsRequest, ListRecordsResponse),
    'ListSets': VerbClasses(ListSetsRequest, ListSetsResponse)
}

class OAIRepository:
    """
    The primary OAI repository class which loads the config and handles OAI requests
    """
    def __init__(self, filepath: str = None):
        self.config = OAIConfig(filepath)
        self.apiqueries = APIQueries(self)

    def process(self, request: dict|OAIRequest) -> OAIResponse:
        """
        Given a request, route to appropriate action and return a response
        """
        try:
            if isinstance(request, dict):
                request = self.create_request(request)
            response = self.create_response(request)
        except OAIError as exc:
            response = OAIErrorResponse(self, exc)
        return response

    @staticmethod
    def create_request(args: dict) -> OAIRequest:
        """Given arguments, create an appropriate new OAI request object"""
        try:
            verb = args.pop('verb')
            request = VERBS[verb].request()
            request.parse(args)
            return request
        except KeyError:
            raise OAIErrorBadVerb(
                "The value of the 'verb' argument in the request is not legal."
            ) from None

    def create_response(self, request: OAIRequest) -> OAIResponse:
        """Given a request, create an appropriate OAI response object"""
        return VERBS[request.verb].response(self, request)

    def identifier(self, localid: str) -> str:
        """Convert from local id value to OAI identifier"""
        return Transform(self.config.localid).reverse(localid)

    def localid(self, identifier: str) -> str:
        """Convert from OAI identifier to local id value"""
        return Transform(self.config.localid).forward(identifier)

    def localmetadataid(self, metadataprefix: str) -> str:
        """Convert a metadataprefix into a local metadata id value"""
        if metadataprefix not in [mdf["metadataPrefix"] for mdf in self.config.metadataformats]:
            raise OAIErrorCannotDisseminateFormat(
                "The requested metadataPrefix is not valid for "\
                "either the given record or the repository."
            )
        return Transform(self.config.localmetadataid).forward(metadataprefix)