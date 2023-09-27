"""
Implementation of ListIdentifiers verb
"""
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse
from .getrecord import header
from .resumption import ResumptionToken
from .exceptions import (
    OAIErrorNoRecordsMatch, OAIErrorBadResumptionToken,
    OAIErrorCannotDisseminateFormat
)


class ListIdentifiersRequest(OAIRequest):
    """
    Parse a request for the ListIdentifiersResponse verb

    Raises:
        OAIErrorBadArgument
        OAIErrorBadResumptionToken
        OAIErrorCannotDisseminateFormat
        OAIErrorNoRecordsMatch
        OAIErrorNoSetHierarchy
    """
    def __init__(self):
        super().__init__()
        self.optional_args = ["from", "until", "set"]
        self.required_args = ["metadataPrefix"]
        self.exclusive_arg = "resumptionToken"
        self.token = ResumptionToken()

    def post_parse(self):
        """Runs after args are parsed"""
        def first_match(key, *args):
            """Return first value from args with key, else None"""
            for arg in args:
                if arg and key in arg:
                    return arg[key]
            return None

        if "resumptionToken" in self.args:
            self.token.parse(self.args["resumptionToken"])

        self.filter_from = first_match("from", self.token.args, self.args)
        self.filter_until = first_match("until", self.token.args, self.args)
        self.filter_set = first_match("set", self.token.args, self.args)
        self.metadata_prefix = first_match("metadataPrefix", self.token.args, self.args)
        if "resumptionToken" in self.args and not self.metadata_prefix:
            raise OAIErrorBadResumptionToken("The resumption token is not valid for given verb.")


class ListIdentifiersResponse(OAIResponse):
    """Generate a resposne for the ListIdentifiers verb"""
    def body(self) -> etree.Element:
        """Response body"""
        mdformats = self.repository.data.get_metadata_formats()
        if self.request.metadata_prefix not in [mdf.metadata_prefix for mdf in mdformats]:
            raise OAIErrorCannotDisseminateFormat(
                "The given metadataPrefix not suported by this repository"
            )

        cursor = (
            self.request.token.cursor + self.repository.data.limit
            if self.request.token.cursor is not None else 0
        )

        identifiers, new_size, state = self.repository.data.list_identifiers(
            self.request.metadata_prefix,
            self.repository.valid_date(self.request.filter_from),
            self.repository.valid_date(self.request.filter_until),
            self.request.filter_set,
            cursor
        )

        if (
            new_size is not None and
            self.request.token.complete_list_size is not None and
            new_size < self.request.token.complete_list_size
        ):
            raise OAIErrorBadResumptionToken("Token is no longer valid as data has changed.")

        if not identifiers:
            raise OAIErrorNoRecordsMatch("No identifiers were found matching given parameters.")

        xmlb = etree.Element("ListIdentifiers")
        # populate response body with record headers
        for identifier in identifiers:
            header(self.repository, identifier, xmlb)

        # append a resumptionToken if needed
        if new_size > self.repository.data.limit:
            token = ResumptionToken()
            token.cursor = cursor
            token.complete_list_size = new_size
            token.set_state(state)
            token.args = { "metadataPrefix": self.request.metadata_prefix }
            if self.request.filter_from:
                token.args['from'] = self.request.filter_from
            if self.request.filter_until:
                token.args['until'] = self.request.filter_until
            if self.request.filter_set:
                token.args['set'] = self.request.filter_set
            if (token_xml := token.xml(self.repository.data.limit)) is not None:
                xmlb.append(token_xml)
        # State change
        if self.request.token.state_hash and self.request.token.state_hash != token.state_hash:
            raise OAIErrorBadResumptionToken("Token is no longer valid as data has changed.")
        return xmlb
