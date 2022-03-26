import oai_repo
from oai_repo.response import nsref

def test_nsref():
    attr1 = "xsi"
    assert nsref(None) == b"{http://www.openarchives.org/OAI/2.0/}"


def test_OAIRepository_process():
    repo = oai_repo.OAIRepository("tests/configs/repo1.json")

    # Valid verb gets correct response class
    request = {
        'verb': 'Identify'
    }
    response = repo.process(request)
    assert isinstance(response, oai_repo.IdentifyResponse)
    assert response

    # Invalid verb gets OAIErrorResponse
    request = {
        'verb': 'NotAVerb'
    }
    response = repo.process(request)
    assert isinstance(response, oai_repo.OAIErrorResponse)
    assert not response
    assert b"badVerb" in bytes(response)
    assert b"The value of the 'verb' argument in the request is not legal." in bytes(response)

    # Unexpected args gets OAIErrorResponse
    request = {
        'verb': 'Identify',
        'unexpected': 'arg'
    }
    response = repo.process(request)
    assert isinstance(response, oai_repo.OAIErrorResponse)
    assert b"badArgument" in bytes(response)
    assert b"Verb Identify does not allow other arguments." in bytes(response)

    # Missing required args gets OAIErrorResponse
    request = {
        'verb': 'GetRecord'
    }
    response = repo.process(request)
    assert isinstance(response, oai_repo.OAIErrorResponse)
    assert b"badArgument" in bytes(response)

    # Exclusive argument passed with additional arguments
    request = {
        'verb': 'ListIdentifiers',
        'resumptionToken': 'more-please',
        'set': 'my-set'
    }
    response = repo.process(request)
    assert isinstance(response, oai_repo.OAIErrorResponse)
    assert b"badArgument" in bytes(response)

    # ListMetadataFormats accepts identifier arg
    repo = oai_repo.OAIRepository("tests/configs/repo3.json")
    request = {
        'verb': 'ListMetadataFormats',
        'identifier': 'oai:d.lib.msu.edu:etd_1000'
    }
    response = repo.process(request)
    assert isinstance(response, oai_repo.ListMetadataFormatsResponse)
    assert b'identifier="oai:d.lib.msu.edu:etd_1000"' in bytes(response)

def test_OAIRepository_identifier():
    repo = oai_repo.OAIRepository("tests/configs/repo1.json")
    assert repo.identifier("abc:123") == "oai:my.example.edu:abc_123"

def test_OAIRepository_local_id():
    repo = oai_repo.OAIRepository("tests/configs/repo1.json")
    assert repo.local_id("oai:my.example.edu:abc_123") == "abc:123"
