from datetime import datetime, timezone
import os
import pytest
from lxml import etree
from oai_repo.resumption import ResumptionToken

def test_ResumptionToken():
    os.environ['TZ'] = 'America/Detroit'

    r1 = ResumptionToken()
    r2 = ResumptionToken()
    assert r1.create() == b""
    r1.args = {
        'metadataPrefix': 'oai_dc'
    }
    assert r1.create() == b"bWV0YWRhdGFQcmVmaXg9b2FpX2Rj"
    assert etree.tostring(r1.xml(50)) == b'<resumptionToken cursor="0"/>'
    r1.complete_list_size = 100
    assert etree.tostring(r1.xml(50)) == (
        b'<resumptionToken cursor="0" completeListSize="100">bWV0YWRhdGFQcmVmaXg9b2FpX'
        b'2RjJnM9MTAw</resumptionToken>'
    )
    r1.cursor = 50
    assert etree.tostring(r1.xml(50)) == b'<resumptionToken cursor="50" completeListSize="100"/>'
    r2.parse(r1.create())
    assert r2.args == r1.args
    assert r2.cursor == r1.cursor
    assert r2.complete_list_size == r1.complete_list_size
    assert r2.expiration_date == r1.expiration_date
    assert r2.state_hash == r1.state_hash

    r1.cursor = 0
    r1.complete_list_size = 999
    r1.expiration_date = datetime(2222,2,22,2,2,2,tzinfo=timezone.utc)
    r1.set_state(123456.789)
    assert r1.state_hash == "ef8bbfd41d4cc599"
    assert r1.create() == (
        b'bWV0YWRhdGFQcmVmaXg9b2FpX2RjJmM9MCZzPTk5OSZlPTc5NTY4NjA1MjImaD1lZjhiYmZkNDFk'
        b'NGNjNTk5'
    )
    r2.parse(r1.create())
    assert r2.args == r1.args
    assert r2.cursor == 0
    assert r2.complete_list_size == 999
    assert r2.expiration_date == datetime(2222,2,22,2,2,2,tzinfo=timezone.utc)
    assert r2.state_hash == "ef8bbfd41d4cc599"
    assert r2.cursor == r1.cursor
    assert r2.complete_list_size == r1.complete_list_size
    assert r2.expiration_date == r1.expiration_date
    assert r2.state_hash == r1.state_hash
    assert etree.tostring(r2.xml(50)) == (
        b'<resumptionToken cursor="0" completeListSize="999" expiration_date="2222-02-'
        b'22T02:02:02Z">bWV0YWRhdGFQcmVmaXg9b2FpX2RjJmM9MCZzPTk5OSZlPTc5NTY4NjA1MjImaD'
        b'1lZjhiYmZkNDFkNGNjNTk5</resumptionToken>'
    )
