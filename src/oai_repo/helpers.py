"""
These are functions which may prove useful when implementing your
your custom DataInterface instance.
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
    # pylint: disable=protected-access
    if not isinstance(bdata, etree._Element):
        if isinstance(bdata, BytesIO):
            bdata.seek(0)
            bdata = bdata.read()
        bdata = etree.fromstring(bdata)
    return bdata

def datestamp_short(timestamp: datetime) -> str:
    """
    Convert a datetime to short form datestamp: YYYY-MM-DD

    Args:
        timestamp (datetime): A Python datetime

    Returns:
        A short granularity formatted date string

    **Examples:**
    ```python
    from datetime import datetime
    from oai_repo import helpers
    # Making a YYYY-MM-DD granularity time string from a datetime
    timestr = helpers.datestamp_short(datetime.now())
    ```
    """
    return timestamp.strftime("%Y-%m-%d")

def datestamp_long(timestamp: datetime) -> str:
    """
    Convert a datetime to long form datestamp: YYYY-MM-DDThh:mm:ssZ

    Args:
        timestamp (datetime): A Python datetime

    Returns:
        A long granularity formatted date string

    **Examples:**
    ```python
    from datetime import datetime
    from oai_repo import helpers
    # Making a YYYY-MM-DDThh:mm:ssZ granularity time string from a datetime
    timestr = helpers.datestamp_long(datetime.now())
    ```
    """
    return timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

def granularity_format(granularity: str, timestamp: datetime) -> str:
    """
    Format a timestamp according to the OAI granularity and return it.

    Args:
        granularity (str): The granularity from OAI (either `YYYY-MM-DDThh:mm:ssZ` or `YYYY-MM-DD`)
        timestamp (datetime): A Python datetime

    Returns:
        A granularity formatted date string appropriate to the granularity passed in

    **Examples:**
    ```python
    from datetime import datetime
    from oai_repo import helpers
    timestr = helpers.granularity_format("YYYY-MM-DD", datetime.now())
    ```
    """
    return datestamp_short(timestamp) \
        if granularity == "YYYY-MM-DD" \
        else datestamp_long(timestamp)

def jsonpath_find(data: dict|list, path: str) -> list:
    """
    Get all matching values for a given JSONPath.

    Args:
        data (dict|list): The already loaded JSON data
        path (str): The JSONPath to find

    Returns:
        A list of matching values

    Raises:
        jsonpath_ng.exceptions.JSONPathError: On jsonpath failure

    **Examples:**
    ```python
    ids = helpers.jsonpath_find(loaded_json, '$.docs[*].id')
    ```
    """
    pattern = jsonpath_ng.parse(path)
    matches = pattern.find(data)
    return [match.value for match in matches]

def jsonpath_find_first(data: dict|list, path: str) -> any:
    """
    Get the first matching value for a given JSONPath

    Args:
        data (dict|list): The already loaded JSON data
        path (str): The JSONPath to find

    Returns:
        The matched value, or None if not found

    Raises:
        jsonpath_ng.exceptions.JSONPathError: On jsonpath failure

    **Examples:**
    ```python
    first_id = helpers.jsonpath_find_first(loaded_json, '$.docs[*].id')
    ```
    """
    matches = jsonpath_find(data, path)
    return next(iter(matches)) if matches else None

def xpath_find(xmlr: etree.Element, path: str) -> list:
    """
    Get matching values for a given XPath

    Args:
        xmlr (lxml.etree.Element): The root xml object to query
        path (str): The xpath query

    Returns:
        A list of matching values

    Raises:
        lxml.etree.XPathError: On xpath failure

    **Examples:**
    ```python
    ids = helpers.xpath_find(loaded_xml, "/response/result/doc/str[name=id]/text()")
    ```
    """
    return xmlr.xpath(path, namespaces=xmlr.nsmap)

def xpath_find_first(xmlr: etree.Element, path: str) -> any:
    """
    Get the first matching value for a given XPath

    Args:
        xmlr (lxml.etree.Element): The root xml object to query
        path (str): The xpath query

    Returns:
        The matched value, or None if not found

    Raises:
        lxml.etree.XPathError: On xpath failure

    **Examples:**
    ```python
    first_id = helpers.xpath_find_first(loaded_xml, "/response/result/doc/str[name=id]/text()")
    ```
    """
    matches = xpath_find(xmlr, path)
    return next(iter(matches)) if matches else None

# Exact repeat API calls will be pulled from here
__APICALL_CACHE = {}

def apicall_querypath(
    url: str = None,
    jsonpath: str = None,
    xpath: str = None
) -> str|None:
    """
    Perform an API call on the given URL and then run either a jsonpath or
    xpath query, returning the first matching result.

    _API call results are cached while processing a single OAI request._  
    Subsequent calls to the same URL will used previous results,
    without resulting in an additional API call.

    Args:
        url (str): The URL to perform an API call to.
        jsonpath (str): A JSONPath query to run on the results from the URL  
                        (must be `None` if `xpath` is passed)
        xpath (str): An XPath query to run on the results from the URL  
                     (must be `None` if `jsonpath` is passed)

    Returns:
        The matching string value, or None if not found

    Raises:
        OAIRepoInternalException: on invalid URL, invalid query, or wrong API response type.
        OAIRepoExternalException: on API call failure, or a non-200 response.

    **Examples:**
    ```python
    # JSONPath
    earliest_api = {
        "url": f"{my_solr_url}?fl=dateyear_dt&q=*%3A*&rows=1&sort=dateyear_dt%20asc",
        "jsonpath": "$.response.docs[0].dateyear_dt[0]"
    }
    earliest = helpers.apicall_querypath(**earliest_api)
    ```
    ```python
    # XPath
    earliest_url = f"{my_solr_url}?fl=dateyear_dt&q=*%3A*&rows=1&sort=dateyear_dt%20asc&wt=xml"
    earliest_query = "/response/result/doc[0]/arr[name=dateyear_dt]/str[0]/text()"
    earliest = helpers.apicall_querypath(url=earliest_url, xpath=earliest_query)
    ```
    """
    if not url:
        raise OAIRepoInternalException("apicall_querypath without a url provided.")
    if not jsonpath and not xpath:
        raise OAIRepoInternalException("apicall_querypath without a jsonpath or xpath provided.")
    if jsonpath and xpath:
        raise OAIRepoInternalException("apicall_querypath with both jsonpath and xpath provided.")

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

def apicall_getxml(url: str = None) ->  etree._Element:
    """
    Perform API call to a URL and load the response as XML.

    Args:
        url (str): A URL path to call.

    Returns:
        A lxml.etree._Element containing the root of the loaded XML.

    Raises:
        OAIRepoExternalException: when the URL call fails or returns non-200 response.
        OAIRepoInternalException: when call to URL does not return valid XML or no URL was provided.

    **Examples:**
    ```python
    loadedXml = helpers.apicall_getxml("https://api.example.edu/record/42")
    ```
    """
    if not url:
        raise OAIRepoInternalException("apicall_getxml called without a URL provided.")
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
