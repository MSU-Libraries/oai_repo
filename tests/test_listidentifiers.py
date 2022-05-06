import pytest
import oai_repo
from oai_repo.exceptions import (
    OAIErrorBadResumptionToken, OAIErrorCannotDisseminateFormat,
    OAIErrorNoRecordsMatch, OAIErrorNoSetHierarchy, OAIErrorBadArgument
)
from .data_sets import DataWithSets

def test_ListIdentifiers():
    repo = oai_repo.OAIRepository(DataWithSets())

    # No resuption token
    request = { 'verb': 'ListIdentifiers', 'metadataPrefix': 'oai_dc' }
    req = repo.create_request(request)
    resp = bytes(repo.create_response(req))
    assert b"<identifier>oai:d.lib.msu.edu:ajpe_1</identifier>" in resp
    assert b"<setSpec>africana:aejp:ajpe</setSpec>" in resp
    assert b"<identifier>oai:d.lib.msu.edu:ajpe_10</identifier>" in resp
    assert b"<setSpec>africana</setSpec>" in resp
    assert b'<resumptionToken cursor="0" completeListSize=' in resp

    # No args
    request = { 'verb': 'ListIdentifiers' }
    with pytest.raises(OAIErrorBadArgument):
        req = repo.create_request(request)

    # Filter set
    request = { 'verb': 'ListIdentifiers', 'metadataPrefix': 'oai_dc', "set": "vvl:idetroit" }
    req = repo.create_request(request)
    rawresp = repo.create_response(req)
    resp = bytes(rawresp)
    assert b'<resumptionToken cursor="0" completeListSize="101">' in resp
    assert b"<identifier>oai:d.lib.msu.edu:idetroit_1</identifier>" in resp

    # Valid resumption token
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

    # Repeat resumption token
    rawresp = repo.create_response(req)
    resp = bytes(rawresp)
    assert b'<resumptionToken cursor="100" completeListSize="101"/>' in resp
    assert rawresp.xpath("//resumptionToken/text()") == []

    # Filter from/until with no results
    request = { 'verb': 'ListIdentifiers', 'metadataPrefix': 'oai_dc', "from": "2000-01-01", "until": "2001-12-31" }
    req = repo.create_request(request)
    with pytest.raises(OAIErrorNoRecordsMatch):
        repo.create_response(req)

    # Invalid resuption token
    request = { 'verb': 'ListIdentifiers', 'resumptionToken': 'invalidtoken' }
    with pytest.raises(OAIErrorBadResumptionToken):
        req = repo.create_request(request)

    # Invalid metadata format requested
    request = { 'verb': 'ListIdentifiers', 'metadataPrefix': 'abcxyz' }
    req = repo.create_request(request)
    with pytest.raises(OAIErrorCannotDisseminateFormat):
        repo.create_response(req)

    # Repository not configured for sets support
    #TODO
