"""
Helper functions
"""
import jsonpath_ng
from lxml import etree

def jsonpath_find_first(data: dict|list, path: str) -> str:
    """
    Get the first matching value for a given JSONPath
    args:
        data: The already loaded JSON data
        path: The JSONPath to find
    returns:
        The matched value, or empty string if not found
    """
    pattern = jsonpath_ng.parse(path)
    matches = pattern.find(data)
    return matches[0].value if matches else ""

def xpath_find_first(xmlr: etree.Element, path: str) -> str:
    """
    Get the first matching value for a given XPath
    args:
        xmlr: The root xml object to query
        path: The xpath query
    returns:
        The matched value, or empty string if not found
    """
    matches = xmlr.xpath(path, namespaces=xmlr.nsmap)
    return matches[0] if matches else ""

