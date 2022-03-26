import pytest
import jsonpath_ng
from lxml import etree
from oai_repo import helpers

def test_jsonpath_find_first():
    data = {
        "key": ["one", "two"]
    }
    # Valid match
    assert helpers.jsonpath_find_first(data, "$.key[1]") == "two"

    # Wrong data
    assert helpers.jsonpath_find_first("a string", "$.key") == None

    # Nothing found
    assert helpers.jsonpath_find_first(data, "$.key[2]") == None

    # Invalid query
    with pytest.raises(jsonpath_ng.exceptions.JSONPathError):
        assert helpers.jsonpath_find_first(data, "$....?")


def test_xpath_find_first():
    # Valid match
    xmlr = etree.fromstring("""<root><key>value</key></root>""")
    assert helpers.xpath_find_first(xmlr, "/root/key/text()") == "value"

    # Nothing found
    assert helpers.xpath_find_first(xmlr, "/root/tree/text()") == None

    # Invalid query
    with pytest.raises(etree.XPathError):
        helpers.xpath_find_first(xmlr, "/root\\key\\/fail()")
