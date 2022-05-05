import pytest
import oai_repo
from oai_repo.exceptions import (
    OAIErrorIdDoesNotExist,
    OAIErrorBadArgument,
    OAIErrorCannotDisseminateFormat,
    OAIRepoExternalException,
)
from .data_sets import DataWithSets

def test_GetRecord():
    repo = oai_repo.OAIRepository(DataWithSets())

    # No arguments
    request = { 'verb': 'GetRecord' }
    with pytest.raises(OAIErrorBadArgument):
        req = repo.create_request(request)

    # Valid identifier with oai_dc prefix
    request = {
        'verb': 'GetRecord',
        'identifier': 'oai:d.lib.msu.edu:idetroit_1',
        'metadataPrefix': 'oai_dc'
    }
    req = repo.create_request(request)
    resp = bytes(repo.create_response(req))
    assert b"<identifier>oai:d.lib.msu.edu:idetroit_1</identifier>" in resp
    assert b"<dc:creator>Barnhill, Bryan, 1986-</dc:creator>" in resp
    assert b"<dc:identifier>idetroit:1</dc:identifier>" in resp
    assert b"<ignoreme>Just a test.</ignoreme>" in resp
    assert b"<setSpec>vvl:idetroit</setSpec>" in resp

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

    # Return record header with Python datetime for timestamp
    #TODO

    # Config where API url returns invalid data
    #TODO
