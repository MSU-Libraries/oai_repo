import pytest
import oai_repo
from oai_repo.exceptions import (
    OAIErrorBadResumptionToken, OAIErrorCannotDisseminateFormat,
    OAIErrorNoRecordsMatch, OAIErrorNoSetHierarchy
)
from .data_sets import DataWithSets

def test_ListRecords():
    repo = oai_repo.OAIRepository(DataWithSets())

    # No resuption token
    request = { 'verb': 'ListRecords', 'metadataPrefix': 'oai_dc' }
    req = repo.create_request(request)
    rawresp = repo.create_response(req)
    resp = bytes(rawresp)
    assert b"<dc:title>Front cover, editorial board, and contents</dc:title>" in resp
    assert b"<dc:publisher>African Association of Political Science</dc:publisher>" in resp
    assert b"<identifier>oai:d.lib.msu.edu:ajpe_1</identifier>" in resp
    assert b"<setSpec>africana:aejp:ajpe</setSpec>" in resp
    assert b"<identifier>oai:d.lib.msu.edu:ajpe_10</identifier>" in resp
    assert b"<setSpec>africana</setSpec>" in resp
    assert b'<resumptionToken cursor="0" completeListSize=' in resp

    # Valid resumption token
    token = rawresp.xpath("//resumptionToken/text()")[0]
    request = { 'verb': 'ListRecords', 'resumptionToken': token }
    req = repo.create_request(request)
    rawresp = repo.create_response(req)
    resp = bytes(rawresp)
    assert b'<resumptionToken cursor="50" completeListSize="' in resp
