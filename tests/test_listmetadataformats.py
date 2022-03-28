import pytest
import oai_repo
from oai_repo.exceptions import OAIErrorIdDoesNotExist

def test_ListMetadataFormats():
    # No identifier given
    repo = oai_repo.OAIRepository("tests/configs/repo1.json")
    request = { 'verb': 'ListMetadataFormats' }
    lmf_req = repo.create_request(request)
    lmf_resp = repo.create_response(lmf_req)
    assert b"<metadataPrefix>mods</metadataPrefix>" in bytes(lmf_resp)
    assert b"<metadataPrefix>oai_dc</metadataPrefix>" in bytes(lmf_resp)

    # Invalid identifier
    repo = oai_repo.OAIRepository("tests/configs/repo3.json")
    request = { 'verb': 'ListMetadataFormats', 'identifier': 'NotAValidIdentifierFormat' }
    lmf_req = repo.create_request(request)
    with pytest.raises(OAIErrorIdDoesNotExist):
        lmf_resp = repo.create_response(lmf_req)

    # Valid identifier but doesn't exist
    request = { 'verb': 'ListMetadataFormats', 'identifier': 'oai:d.lib.msu.edu:notRealId' }
    lmf_req = repo.create_request(request)
    with pytest.raises(OAIErrorIdDoesNotExist):
        lmf_resp = repo.create_response(lmf_req)

    # Valid identifier given
    request = { 'verb': 'ListMetadataFormats', 'identifier': 'oai:d.lib.msu.edu:etd_1000' }
    lmf_req = repo.create_request(request)
    lmf_resp = repo.create_response(lmf_req)
    assert b"<request identifier=\"oai:d.lib.msu.edu:etd_1000\">https://d.lib.msu.edu/oai</request>" in bytes(lmf_resp)
    assert b"<metadataPrefix>mods</metadataPrefix>" in bytes(lmf_resp)
    assert b"<metadataPrefix>oai_dc</metadataPrefix>" in bytes(lmf_resp)
