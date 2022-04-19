"""
Helper functions which may prove useful when creating your DataInterface instance
"""
import json
from datetime import datetime
from io import BytesIO
import requests
import jsonpath_ng
from lxml import etree
from .exceptions import OAIRepoInternalException, OAIRepoExternalException

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

def granularity_format(granularity: str, timestamp: datetime) -> str:
    """
    Format the timestamp according to the OAI granularity and return it.
    """
    return timestamp.strftime("%Y-%m-%d") \
        if granularity == "YYYY-MM-DD" \
        else timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

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

# Exact repeat API calls will be pulled from here
__APICALL_CACHE = {}

def apicall_querypath(
    url: str = None,
    jsonpath: str = None,
    xpath: str = None
):
    """
    Perform an API call and then either an jsonpath or xpath query,
    returning the first matching result.
    Calls are cached. Subsequent calls to the same URL will used previous results.
    args:
        TODO
    returns:
        TODO
    raises:
        TODO
    """
    if not url:
        raise OAIRepoInternalException("API call querypath without a URL provided.")
    if not jsonpath and not xpath:
        raise OAIRepoInternalException("API call querypath without a jsonpath or xpath provided.")

    if url not in __APICALL_CACHE:
        try:
            resp = requests.get(url, timeout=10)
        except requests.RequestException as exc:
            raise OAIRepoExternalException(f"Call to API failed: {url}") from exc
        if not resp.status_code == 200:
            raise OAIRepoExternalException(f"Call to API returned {resp.status_code}: {url}")
        __APICALL_CACHE[url] = resp
    resp = __APICALL_CACHE[url]

    match = None
    if jsonpath:
        try:
            loaded = json.loads(resp.text)
            match = jsonpath_find_first(loaded, jsonpath)
        except jsonpath_ng.exceptions.JSONPathError as exc:
            raise OAIRepoInternalException(f"JSONPath is not valid: {jsonpath}") from exc
    elif xpath:
        try:
            loaded = etree.fromstring(resp.content)
            match = xpath_find_first(loaded, xpath)
        except etree.XPathError as exc:
            raise OAIRepoInternalException(f"XPath is not valid: {xpath}") from exc
        except etree.XMLSyntaxError as exc:
            raise OAIRepoInternalException(
                f"Response to API call was not valid XML: {url}"
            ) from exc
    return match

def apicall_getxml(url: str = None):
    """
    Perform API call to URL and load the response as XML.
    args:
        url (str): A URL path to call
    returns:
        A lxml.etree._Element containing the root of the loaded XML
    raises:
        OAIRepoExternalException when the URL call fails or returns non-success response
        OAIRepoInternalException when call to URL does not return valid XML or no URL was provided
    """
    if not url:
        raise OAIRepoInternalException("API call getxml without a URL provided.")
    try:
        resp = requests.get(url, timeout=10)
    except requests.RequestException as exc:
        raise OAIRepoExternalException(f"Call to API failed: {url}") from exc
    if not resp.status_code == 200:
        raise OAIRepoExternalException(f"Call to API returned {resp.status_code}: {url}")

    try:
        loaded = etree.fromstring(resp.content)
    except etree.XMLSyntaxError as exc:
        raise OAIRepoInternalException(f"Response to API call was not valid XML: {url}") from exc
    return loaded
