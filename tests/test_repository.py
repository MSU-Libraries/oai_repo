import pytest
import oai_repo
from oai_repo.identify import IdentifyResponse
from oai_repo.listmetadataformats import ListMetadataFormatsResponse
from oai_repo.error import OAIErrorResponse
from oai_repo.exceptions import OAIErrorIdDoesNotExist
from .data_sets import DataWithSets

def test_OAIRepository_process():
    repo = oai_repo.OAIRepository(DataWithSets())

    # Valid verb gets correct response class
    request = {
        'verb': 'Identify'
    }
    response = repo.process(request)
    assert isinstance(response, IdentifyResponse)
    assert response

    # Invalid verb gets OAIErrorResponse
    request = {
        'verb': 'NotAVerb'
    }
    response = repo.process(request)
    assert isinstance(response, OAIErrorResponse)
    assert not response
    assert b"badVerb" in bytes(response)
    assert b"The value of the 'verb' argument in the request is not legal." in bytes(response)

    # Unexpected args gets OAIErrorResponse
    request = {
        'verb': 'Identify',
        'unexpected': 'arg'
    }
    response = repo.process(request)
    assert isinstance(response, OAIErrorResponse)
    assert b"badArgument" in bytes(response)
    assert b"Verb Identify does not allow other arguments." in bytes(response)

    # Missing required args gets OAIErrorResponse
    request = {
        'verb': 'GetRecord'
    }
    response = repo.process(request)
    assert isinstance(response, OAIErrorResponse)
    assert b"badArgument" in bytes(response)

    # Exclusive argument passed with additional arguments
    request = {
        'verb': 'ListIdentifiers',
        'resumptionToken': 'more-please',
        'set': 'my-set'
    }
    response = repo.process(request)
    assert isinstance(response, OAIErrorResponse)
    assert b"badArgument" in bytes(response)

    # ListMetadataFormats accepts identifier arg
    repo = oai_repo.OAIRepository(DataWithSets())
    request = {
        'verb': 'ListMetadataFormats',
        'identifier': 'oai:d.lib.msu.edu:etd_1000'
    }
    response = repo.process(request)
    assert isinstance(response, ListMetadataFormatsResponse)
    assert b'identifier="oai:d.lib.msu.edu:etd_1000"' in bytes(response)
    assert b'<metadataPrefix>mods</metadataPrefix>' in bytes(response)
    assert b'<metadataPrefix>oai_dc</metadataPrefix>' in bytes(response)

    # ListMetadataFormats for identifier that does not exist
    request = {
        'verb': 'ListMetadataFormats',
        'identifier': 'oai:d.lib.msu.edu:fakeID'
    }
    response = repo.process(request)
    assert isinstance(response, OAIErrorResponse)
    assert b"idDoesNotExist" in bytes(response)

def test_OAIRepository_DataWithSets():
    repo = oai_repo.OAIRepository(DataWithSets())

    set1 = repo.data.get_set("vvl")
    assert set1.name == "G. Robert Vincent Voice Library Collection"
    set2 = repo.data.get_set("vvl:wosl")
    assert set2.name == "Women's Overseas Service League Oral History Project"
    set3 = repo.data.get_set("notarealset")
    assert set3 is None
