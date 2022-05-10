from datetime import datetime
from lxml import etree
import pytest
import oai_repo
from oai_repo.exceptions import OAIErrorBadArgument
from .data_sets import DataWithSets

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
    repo = oai_repo.OAIRepository(DataWithSets())
    req = { 'verb': 'Identify' }
    rawresp = repo.process(req)
    resp = bytes(rawresp)
    assert b"<repositoryName>My OAI Repo</repositoryName>" in resp
    assert b"<earliestDatestamp>2000-01-31</earliestDatestamp>" in resp
    rstamp = rawresp.xpath("//responseDate/text()")[0]
    assert datetime.strptime(rstamp, "%Y-%m-%dT%H:%M:%SZ")

    # Passing an unwanted arg
    request = { 'verb': 'Identify', 'arg': 'unwanted' }
    with pytest.raises(OAIErrorBadArgument):
        repo.create_request(request)

