"""
OAIRepository functionality
"""
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

# TODO NamedTuple for Req/Resp pair?
VERBS = {
    'GetRecord': (GetRecordRequest, GetRecordResponse),
    'Identify': (IdentifyRequest, IdentifyResponse),
    'ListIdentifiers': (ListIdentifiersRequest, ListIdentifiersResponse),
    'ListMetadataFormats': (ListMetadataFormatsRequest, ListMetadataFormatsResponse),
    'ListRecords': (ListRecordsRequest, ListRecordsResponse),
    'ListSets': (ListSetsRequest, ListSetsResponse)
}

class OAIRepository:
    """
    """
    def __init__(self, filepath: str = None):
        if filepath:
            self.config_from_file(filepath)

    def config_from_file(self, filepath):
        pass

    def config(self, key: str, val):
        """
        Set or change a repository configuration setting
        """
        pass

    def process(self, request: dict|OAIRequest) -> OAIResponse:
        """
        Given a request, route to appropriate action and return a response
        """
        try:
            if isinstance(request, dict):
                request = _create_request(request)
            response = _create_response(request)
        except OAIException as exc:
            response = OAIErrorResponse(exc)
        return response

def _create_request(args: dict) -> OAIRequest:
    """
    TODO
    """
    try:
        verb = args.pop('verb')
        request = VERBS[verb][0]()
        request.parse(args)
        return request
    except KeyError:
        raise OAIErrorBadVerb("The value of the 'verb' argument in the request is not legal.")

def _create_response(request: OAIRequest) -> OAIResponse:
    """
    TODO
    """
    return VERBS[request.verb][1]()
