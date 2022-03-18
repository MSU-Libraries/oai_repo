"""
OAIRepository functionality
"""
import json
from typing import NamedTuple
from .getrecord import GetRecordRequest, GetRecordResponse
from .identify import IdentifyRequest, IdentifyResponse
from .listidentifiers import ListIdentifiersRequest, ListIdentifiersResponse
from .listmetadataformats import ListMetadataFormatsRequest, ListMetadataFormatsResponse
from .listrecords import ListRecordsRequest, ListRecordsResponse
from .listsets import ListSetsRequest, ListSetsResponse
from .exceptions import OAIException, OAIErrorBadVerb
from .error import OAIErrorResponse
from .request import OAIRequest
from .response import OAIResponse

class VerbClasses(NamedTuple):
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
    """
    def __init__(self, filepath: str = None):
        self.config = {}
        if filepath:
            self.config_from_file(filepath)

    def config_from_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf8') as fileh:
                self.config = json.load(fileh)
        except FileNotFoundError as exc:
            #TODO
            raise exc
        except json.JSONDecodeError as exc:
            #TODO
            raise exc

    def process(self, request: dict|OAIRequest) -> OAIResponse:
        """
        Given a request, route to appropriate action and return a response
        """
        try:
            if isinstance(request, dict):
                request = _create_request(request)
            response = _create_response(self, request)
        except OAIException as exc:
            response = OAIErrorResponse(exc)
        return response

def _create_request(args: dict) -> OAIRequest:
    try:
        verb = args.pop('verb')
        request = VERBS[verb].request()
        request.parse(args)
        return request
    except KeyError:
        raise OAIErrorBadVerb("The value of the 'verb' argument in the request is not legal.")

def _create_response(repository: OAIRepository, request: OAIRequest) -> OAIResponse:
    return VERBS[request.verb].response(repository, request)
