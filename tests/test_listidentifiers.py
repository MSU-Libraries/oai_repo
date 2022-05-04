import pytest
import oai_repo
from oai_repo.exceptions import (
    OAIErrorBadResumptionToken, OAIErrorCannotDisseminateFormat,
    OAIErrorNoRecordsMatch, OAIErrorNoSetHierarchy
)
from .data1 import GoodData

def test_ListIdentifiers():
    repo = oai_repo.OAIRepository(GoodData())

    # No resuption token
    request = { 'verb': 'ListIdentifiers', 'metadataPrefix': 'oai_dc' }
    req = repo.create_request(request)
    resp = bytes(repo.create_response(req))
    assert b"<identifier>oai:d.lib.msu.edu:ajpe_1</identifier>" in resp
    assert b"<setSpec>africana:aejp:ajpe</setSpec>" in resp
    assert b"<identifier>oai:d.lib.msu.edu:ajpe_10</identifier>" in resp
    assert b"<setSpec>africana</setSpec>" in resp
    assert b"<resumptionToken cursor=\"50\" completeListSize=" in resp

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
