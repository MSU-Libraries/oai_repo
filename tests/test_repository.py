import oai_repo
from oai_repo.response import nsref

def test_nsref():
    attr1 = "xsi"
    assert nsref(None) == b"{http://www.openarchives.org/OAI/2.0/}"


def test_OAIRepository():
    repo = oai_repo.OAIRepository("tests/inst1/repo1.json")
    # TODO more configuration?

    # Valid verb gets correct response class
    request = {
        'verb': 'Identify'
    }
    response = repo.process(request)
    assert isinstance(response, oai_repo.IdentifyResponse)

    # Invalid verb gets OAIErrorResponse
    request = {
        'verb': 'NotAVerb'
    }
    response = repo.process(request)
    assert isinstance(response, oai_repo.OAIErrorResponse)
    # TODO check for 'badVerb' in response

    # Unexpected args gets OAIErrorResponse
    request = {
        'verb': 'Identify',
        'unexpected': 'arg'
    }
    response = repo.process(request)
    assert isinstance(response, oai_repo.OAIErrorResponse)
    # TODO check for 'badArgument' in response'

    # Missing required args gets OAIErrorResponse
    request = {
        'verb': 'GetRecord'
    }
    response = repo.process(request)
    assert isinstance(response, oai_repo.OAIErrorResponse)
    # TODO check for 'badArgument' in response'

    # Exclusive argument passed with additional arguments
    request = {
        'verb': 'ListIdentifiers',
        'resumptionToken': 'more-please',
        'set': 'my-set'
    }
    response = repo.process(request)
    assert isinstance(response, oai_repo.OAIErrorResponse)
    # TODO check for 'badArgument' in response'

    # ListMetadataFormats accepts identifier arg
    request = {
        'verb': 'ListMetadataFormats',
        'identifier': 'my-ident'
    }
    response = repo.process(request)
    assert isinstance(response, oai_repo.ListMetadataFormatsResponse)
    assert b'identifier="my-ident"' in bytes(response)  # assuming valid identifier
