from lxml import etree
import pytest
import oai_repo
from oai_repo.exceptions import OAIErrorBadArgument

def test_Identify():
    # valid Identify oject
    ident = oai_repo.Identify()
    ident.repository_name = "My OAI Repo"
    ident.base_url = "https://my.example.edu/oai"
    ident.admin_email.append("oai@example.edu")
    ident.deleted_record = "no"
    ident.granularity = "YYYY-MM-DD"
    ident.compression = []
    ident.earliest_datestamp = "2000-01-31"
    ident.description.append(b"<mydescription>Hello</mydescription>")
    assert len(ident.errors()) == 0

    # invalid Identify object
    ident = oai_repo.Identify()
    ident.repository_name = ""
    ident.base_url = "my.example.edu/oai"
    ident.admin_email.append("oai.example.edu")
    ident.deleted_record = "nope"
    ident.granularity = "MM/DD/YYYY"
    ident.compression.append("identity")
    ident.description.append(b"My Description")
    assert len(ident.errors()) == 7

    # another invalid Identity object
    ident = oai_repo.Identify()
    ident.granularity = "YYYY-MM-DD"
    ident.earliest_datestamp = 1900
    ident.description.append("<mydescription>Hello</mydescription>")
    assert len(ident.errors()) == 5

def test_IdentifyResponse():
    # earliestDatestamp: static
    repo = oai_repo.OAIRepository("tests/configs/repo1.json")
    request = { 'verb': 'Identify' }
    identify_req = repo.create_request(request)
    identify_resp = repo.create_response(identify_req)
    xmlr = etree.Element("root")
    identify_resp.add_earliest_datestamp_element(xmlr)
    assert b"<earliestDatestamp>2012-08-21T13:49:50Z</earliestDatestamp>" in etree.tostring(xmlr)

    # earliestDatestamp: jsonpath
    repo = oai_repo.OAIRepository("tests/configs/repo2.json")
    request = { 'verb': 'Identify' }
    identify_req = repo.create_request(request)
    identify_resp = repo.create_response(identify_req)
    xmlr = etree.Element("root")
    identify_resp.add_earliest_datestamp_element(xmlr)
    assert b"<earliestDatestamp>2015-07-15T00:00:00Z</earliestDatestamp>" in etree.tostring(xmlr)

    # earliestDatestamp: xpath
    repo = oai_repo.OAIRepository("tests/configs/repo3.json")
    request = { 'verb': 'Identify' }
    identify_req = repo.create_request(request)
    identify_resp = repo.create_response(identify_req)
    xmlr = etree.Element("root")
    identify_resp.add_earliest_datestamp_element(xmlr)
    assert b"<earliestDatestamp>2015-07-15T00:00:00Z</earliestDatestamp>" in etree.tostring(xmlr)

    # Passing an unwanted arg
    request = { 'verb': 'Identify', 'arg': 'unwanted' }
    with pytest.raises(OAIErrorBadArgument):
        identify_req = repo.create_request(request)

