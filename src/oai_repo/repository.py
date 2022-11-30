"""
OAIRepository functionality
"""
from typing import NamedTuple
from datetime import datetime, timezone
from .getrecord import GetRecordRequest, GetRecordResponse
from .identify import IdentifyRequest, IdentifyResponse
from .listidentifiers import ListIdentifiersRequest, ListIdentifiersResponse
from .listmetadataformats import ListMetadataFormatsRequest, ListMetadataFormatsResponse
from .listrecords import ListRecordsRequest, ListRecordsResponse
from .listsets import ListSetsRequest, ListSetsResponse
from .exceptions import (
    OAIError, OAIErrorBadVerb, OAIErrorIdDoesNotExist,
    OAIErrorCannotDisseminateFormat, OAIErrorBadArgument
)
from .error import OAIErrorResponse
from .request import OAIRequest
from .response import OAIResponse
from .interface import DataInterface

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
    def __init__(self, data: DataInterface):
        self.data = data

    def process(self, request: dict) -> OAIResponse:
        """
        Given a request, route to appropriate action and return a response
        """
        try:
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

    def valid_date(self, datestr: str):
        """
        Parse an argument provided datestr into a datetime object;
        Args:
            datestr (str|None): An unvalidated date string
        Returns:
            A datetime.datetime object, or None if datestr was None.
        Raises:
            OAIErrorBadArgument If an invalid date is passed
                or if date was not valid according to the repository
                granularity.
        """
        allowed_datefmts = ["%Y-%m-%d"]
        if self.data.get_identify().granularity == "YYYY-MM-DDThh:mm:ssZ":
            allowed_datefmts.append("%Y-%m-%dT%H:%M:%SZ")

        date = None
        if datestr is not None:
            try:
                for datefmt in allowed_datefmts:
                    date = datetime.strptime(datestr, datefmt).replace(tzinfo=timezone.utc)
            except (TypeError, ValueError):
                raise OAIErrorBadArgument(
                    "A date passed in not in a valid format. See Identify for granularity."
                ) from None
        return date
