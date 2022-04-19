import pytest
import oai_repo
from oai_repo.exceptions import OAIErrorIdDoesNotExist
from .data1 import GoodData

def test_ListSets():
    repo = oai_repo.OAIRepository(GoodData())

    # No resuption token
    request = { 'verb': 'ListSets' }
    req = repo.create_request(request)
    resp = bytes(repo.create_response(req))
    assert b"<setName>African e-Journals Project</setName>" in resp
    assert b"<dc:title>African e-Journals Project</dc:title>" in resp
    assert b"<dc:identifier>aejp:root</dc:identifier>" in resp
    assert b"<dc:language>Swahili</dc:language>" in resp

    # Valid resumption token
    #TODO

    # Repeat resumption token
    #TODO

    # Invalid resuption token
    #TODO

    # Repository not configured for sets support
    #TODO
