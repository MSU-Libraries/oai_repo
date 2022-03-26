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
from .exceptions import OAIException, OAIErrorBadVerb, OAIErrorIdDoesNotExist
from .error import OAIErrorResponse
from .request import OAIRequest
from .response import OAIResponse
from .config import OAIConfig

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

    def process(self, request: dict|OAIRequest) -> OAIResponse:
        """
        Given a request, route to appropriate action and return a response
        """
        try:
            if isinstance(request, dict):
                request = self.create_request(request)
            response = self.create_response(request)
        except OAIException as exc:
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

    def identifier(self, local_id: str) -> str:
        """Convert from local id value to OAI identifier"""
        if "transforms" in self.config.identifier:
            for transform in self.config.identifier["transforms"]:
                local_id = local_id.replace(transform[0], transform[1])
        return self.config.identifier["prefix"] + local_id

    def local_id(self, identifier: str) -> str:
        """Convert from OAI identifier to local id value"""
        prefix = self.config.identifier["prefix"]
        if not identifier.startswith(prefix):
            raise OAIErrorIdDoesNotExist("Identifier argument is invalid.")
        local_id = identifier.removeprefix(prefix)
        if "transforms" in self.config.identifier:
            for transform in self.config.identifier["transforms"]:
                local_id = local_id.replace(transform[1], transform[0])
        return local_id
