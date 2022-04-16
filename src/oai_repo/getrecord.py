"""
Implementation of GetRecord verb
"""
from lxml import etree
from .request import OAIRequest
from .response import OAIResponse
from .exceptions import OAIErrorCannotDisseminateFormat


class RecordHeaderValidator:
    """
    """


class GetRecordRequest(OAIRequest):
    """
    Parse a request for the GetRecord verb
    raises:
        OAIErrorBadArgument
    """
    def __init__(self):
        super().__init__()
        self.required_args: list = ["identifier", "metadataPrefix"]
        self.identifier: str = None
        self.metadataprefix: str = None

    def post_parse(self):
        """Runs after args are parsed"""
        self.identifier = self.args.get("identifier")
        self.metadataprefix = self.args.get("metadataPrefix")

    def __repr__(self):
        return f"GetRecordRequest(identifier={self.identifier},"\
               f"metadataprefix={self.metadataprefix})"

class GetRecordResponse(OAIResponse):
    """
    Generate a resposne for the GetRecord verb
    raises:
        OAIErrorIdDoesNotExist
        OAIErrorCannotDisseminateFormat
    """
    def __repr__(self):
        return f"GetRecordResponse(identifier={self.request.identifier},"\
               f"metadataprefix={self.request.metadataprefix})"

    def body(self) -> etree.Element:
        """Response body"""
        self.repository.apiqueries.assert_identifier(self.request.identifier)

        metadataformats = self.repository.apiqueries.metadata_formats(self.request.identifier)
        mdprefix = self.repository.localmetadataid(self.request.metadataprefix)
        if mdprefix not in metadataformats:
            raise OAIErrorCannotDisseminateFormat(
                "The requested metadataPrefix does not exist for the given identifier."
            )

        # TODO also needs OAI record <header> section

        # TODO optional <about> section (only when repo supports deletion)

        # TODO record metadata needs to be wrapped in <metadata> tag
        return self.repository.apiqueries.record_metadata(
            self.request.identifier,
            self.request.metadataprefix
        )
