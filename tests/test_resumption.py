import pytest
from datetime import datetime
from oai_repo.resumption import ResumptionToken

def test_ResumptionToken():
    r1 = ResumptionToken()
    r2 = ResumptionToken()
    assert r1.create() == b""
    r1.args = {
        'verb': 'ListSets',
        'metadataPrefix': 'oai_dc'
    }
    assert r1.create() == b"dmVyYj1MaXN0U2V0cyZtZXRhZGF0YVByZWZpeD1vYWlfZGM="
    r2.parse(r1.create())
    assert r2.args == r1.args
    assert r2.cursor == r1.cursor
    assert r2.complete_list_size == r1.complete_list_size
    assert r2.expiration_date == r1.expiration_date
    assert r2.state_hash == r1.state_hash
    assert bytes(r1) == b"<resumptionToken>dmVyYj1MaXN0U2V0cyZtZXRhZGF0YVByZWZpeD1vYWlfZGM=</resumptionToken>"

    r1.cursor = 50
    r1.complete_list_size = 999
    r1.expiration_date = datetime(2222,2,22,2,2,2)
    r1.set_state(123456.789)
    assert r1.state_hash == "ef8bbfd41d4cc599"
    assert r1.create() == (
        b'dmVyYj1MaXN0U2V0cyZtZXRhZGF0YVByZWZpeD1vYWlfZGMmYz01MCZzPTk5OSZlPTc5NTY4NjA1'
        b'MjImaD1lZjhiYmZkNDFkNGNjNTk5'
    )
    r2.parse(r1.create())
    assert r2.args == r1.args
    assert r2.cursor == 50
    assert r2.complete_list_size == 999
    assert r2.expiration_date == datetime(2222,2,22,2,2,2)
    assert r2.state_hash == "ef8bbfd41d4cc599"
    assert r2.cursor == r1.cursor
    assert r2.complete_list_size == r1.complete_list_size
    assert r2.expiration_date == r1.expiration_date
    assert r2.state_hash == r1.state_hash
    assert bytes(r2) == (
        b'<resumptionToken cursor="50" completeListSize="999" expiration_date="2222-02'
        b'-22T02:02:02Z">dmVyYj1MaXN0U2V0cyZtZXRhZGF0YVByZWZpeD1vYWlfZGMmYz01MCZzPTk5O'
        b'SZlPTc5NTY4NjA1MjImaD1lZjhiYmZkNDFkNGNjNTk5</resumptionToken>'
    )
