"""
Helper functions
"""
from io import BytesIO
import jsonpath_ng
from lxml import etree

def bytes_to_xml(bdata: bytes|BytesIO) -> etree._Element:
    """
    Given a bytes or BytesIO, parse and return an lxml.etree._Element.
    If passed an lxml.etree._Element, then will return it unchanged.
    Args:
        bdata (bytes|BytesIO): The bytes data to parse
    Returns:
        The loaded XML element.
    Raises:
        etree.XMLSyntaxError: On XML parse error
    """
    if not isinstance(bdata, etree._Element):
        if isinstance(bdata, BytesIO):
            bdata.seek(0)
            bdata = bdata.read()
        bdata = etree.fromstring(bdata)
    return bdata

def jsonpath_find_first(data: dict|list, path: str):
    """
    Get the first matching value for a given JSONPath
    Args:
        data: The already loaded JSON data
        path: The JSONPath to find
    Returns:
        The matched value, or empty string if not found
    Raises:
        jsonpath_ng.exceptions.JSONPathError on jsonpath failure
    """
    pattern = jsonpath_ng.parse(path)
    matches = pattern.find(data)
    return matches[0].value if matches else None

def xpath_find_first(xmlr: etree.Element, path: str):
    """
    Get the first matching value for a given XPath
    Args:
        xmlr: The root xml object to query
        path: The xpath query
    Returns:
        The matched value, or empty string if not found
    Raises:
        lxml.etree.XPathError on xpath failure
    """
    matches = xmlr.xpath(path, namespaces=xmlr.nsmap)
    return matches[0] if matches else None
