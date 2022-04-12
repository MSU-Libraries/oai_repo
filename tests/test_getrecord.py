import pytest
import oai_repo
from oai_repo.exceptions import (
    OAIErrorIdDoesNotExist,
    OAIErrorBadArgument,
    OAIErrorCannotDisseminateFormat,
    OAIRepoExternalException,
)

def test_GetRecord():
    # No arguments
    repo = oai_repo.OAIRepository("tests/configs/repo2.json")
    request = { 'verb': 'GetRecord' }
    with pytest.raises(OAIErrorBadArgument):
        req = repo.create_request(request)

    # Valid identifier with oai_dc prefix
    request = {
        'verb': 'GetRecord',
        'identifier': 'oai:d.lib.msu.edu:etd_1001',
        'metadataPrefix': 'oai_dc'
    }
    req = repo.create_request(request)
    resp = repo.create_response(req)
    assert b"<dc:creator>Corr, Dustin L.</dc:creator>" in bytes(resp)
    assert b"<dc:identifier>etd:1001</dc:identifier>" in bytes(resp)

    # Valid identifier with mods prefix
    request = {
        'verb': 'GetRecord',
        'identifier': 'oai:d.lib.msu.edu:etd_1002',
        'metadataPrefix': 'mods'
    }
    req = repo.create_request(request)
    resp = repo.create_response(req)
    assert b"<mods:namePart>Wu, Wei-Ying</mods:namePart>" in bytes(resp)
    assert b"<mods:identifier type=\"isbn\">9781124738291</mods:identifier>" in bytes(resp)

    # Invalid metadataPrefix
    request = {
        'verb': 'GetRecord',
        'identifier': 'oai:d.lib.msu.edu:etd_1002',
        'metadataPrefix': 'abc'
    }
    req = repo.create_request(request)
    with pytest.raises(OAIErrorCannotDisseminateFormat):
        resp = repo.create_response(req)

    # Invalid identifier: bad prefix
    request = {
        'verb': 'GetRecord',
        'identifier': 'abc:w.y.y.z:etd_1003',
        'metadataPrefix': 'oai_dc'
    }
    req = repo.create_request(request)
    with pytest.raises(OAIErrorIdDoesNotExist):
        resp = repo.create_response(req)

    # Invalid identifier: does not exist
    request = {
        'verb': 'GetRecord',
        'identifier': 'oai:d.lib.msu.edu:ABCDEFG',
        'metadataPrefix': 'oai_dc'
    }
    req = repo.create_request(request)
    with pytest.raises(OAIErrorIdDoesNotExist):
        resp = repo.create_response(req)

    # Config where API url returns invalid XML
    repo = oai_repo.OAIRepository("tests/configs/repo4.json")
    request = {
        'verb': 'GetRecord',
        'identifier': 'oai:d.lib.msu.edu:etd_1001',
        'metadataPrefix': 'oai_dc'
    }
    req = repo.create_request(request)
    with pytest.raises(OAIRepoExternalException):
        resp = repo.create_response(req)
