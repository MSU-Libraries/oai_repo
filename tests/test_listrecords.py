import pytest
import oai_repo
from oai_repo.exceptions import (
    OAIErrorBadResumptionToken, OAIErrorCannotDisseminateFormat,
    OAIErrorNoRecordsMatch, OAIErrorNoSetHierarchy
)
from .data1 import GoodData

def test_ListRecords():
    repo = oai_repo.OAIRepository(GoodData())

    # No resuption token
    request = { 'verb': 'ListRecords', 'metadataPrefix': 'oai_dc' }
    req = repo.create_request(request)
    resp = bytes(repo.create_response(req))
    #TODO

    # Valid resumption token
    #TODO

    # Repeat resumption token
    #TODO

    # Invalid resuption token
    #TODO

    # Invalid metadata format requested
    #TODO

    # Repository not configured for sets support
    #TODO
