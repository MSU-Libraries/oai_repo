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
    assert b'<resumptionToken cursor="0" completeListSize=' in resp

    # Filter set
    request = { 'verb': 'ListIdentifiers', 'metadataPrefix': 'oai_dc', "set": "vvl:idetroit" }
    req = repo.create_request(request)
    rawresp = repo.create_response(req)
    resp = bytes(rawresp)
    assert b'<resumptionToken cursor="0" completeListSize="101">' in resp
    assert b"<identifier>oai:d.lib.msu.edu:idetroit_1</identifier>" in resp
    # Using the resumption token
    token = rawresp.xpath("//resumptionToken/text()")[0]
    request = { 'verb': 'ListIdentifiers', 'resumptionToken': token }
    req = repo.create_request(request)
    rawresp = repo.create_response(req)
    resp = bytes(rawresp)
    assert b'<resumptionToken cursor="50" completeListSize="101">' in resp
    token = rawresp.xpath("//resumptionToken/text()")[0]
    request = { 'verb': 'ListIdentifiers', 'resumptionToken': token }
    req = repo.create_request(request)
    rawresp = repo.create_response(req)
    resp = bytes(rawresp)
    assert b'<resumptionToken cursor="100" completeListSize="101"/>' in resp
    assert rawresp.xpath("//resumptionToken/text()") == []

    # Filter from/until
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
