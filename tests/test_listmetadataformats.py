import oai_repo

def test_ListMetadataFormats():
    # No identifier given
    repo = oai_repo.OAIRepository("tests/configs/repo1.json")
    request = { 'verb': 'ListMetadataFormats' }
    lmf_req = repo.create_request(request)
    lmf_resp = repo.create_response(lmf_req)
    assert b"<metadataPrefix>mods</metadataPrefix>" in bytes(lmf_resp)
    assert b"<metadataPrefix>oai_dc</metadataPrefix>" in bytes(lmf_resp)
