import oai_repo

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
    #TODO

    # Valid identifier but doesn't exist
    #TODO

    # Valid identifier given
    request = { 'verb': 'ListMetadataFormats', 'identifier': 'oai:d.lib.msu.edu:etd_1000' }
    lmf_req = repo.create_request(request)
    lmf_resp = repo.create_response(lmf_req)
    assert b"<request identifier=\"oai:d.lib.msu.edu:etd_1000\">http://d.lib.msu.edu/oai</request>" in bytes(lmf_resp)
    assert b"<metadataPrefix>mods</metadataPrefix>" in bytes(lmf_resp)
    assert b"<metadataPrefix>oai_dc</metadataPrefix>" in bytes(lmf_resp)
