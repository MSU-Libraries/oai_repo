import pytest
import oai_repo
from oai_repo.exceptions import OAIErrorIdDoesNotExist
from .data_sets import DataWithSets

def test_ListMetadataFormats():
    repo = oai_repo.OAIRepository(DataWithSets())
    # No identifier given
    request = { 'verb': 'ListMetadataFormats' }
    req = repo.create_request(request)
    resp = repo.create_response(req)
    assert b"<metadataPrefix>mods</metadataPrefix>" in bytes(resp)
    assert b"<metadataPrefix>oai_dc</metadataPrefix>" in bytes(resp)

    # Invalid identifier
    request = { 'verb': 'ListMetadataFormats', 'identifier': 'NotAValidIdentifierFormat' }
    req = repo.create_request(request)
    with pytest.raises(OAIErrorIdDoesNotExist):
        repo.create_response(req)

    # Valid identifier but doesn't exist
    request = { 'verb': 'ListMetadataFormats', 'identifier': 'oai:d.lib.msu.edu:notRealId' }
    req = repo.create_request(request)
    with pytest.raises(OAIErrorIdDoesNotExist):
        repo.create_response(req)

    # Valid identifier given
    request = { 'verb': 'ListMetadataFormats', 'identifier': 'oai:d.lib.msu.edu:etd_1000' }
    req = repo.create_request(request)
    resp = repo.create_response(req)
    assert b"<request identifier=\"oai:d.lib.msu.edu:etd_1000\">https://d.lib.msu.edu/oai</request>" in bytes(resp)
    assert b"<metadataPrefix>mods</metadataPrefix>" in bytes(resp)
    assert b"<metadataPrefix>oai_dc</metadataPrefix>" in bytes(resp)
