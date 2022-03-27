"""
API call handlers
"""
import json
import requests
import jsonpath_ng
from lxml import etree
from . import helpers
from .exceptions import OAIRepoInternalException, OAIRepoExternalException

APICALL_CACHE = {}

def apicall_querypath(
    url: str = None,
    jsonpath: str = None,
    xpath: str = None
):
    """
    Perform an API call and then either an jsonpath or xpath query,
    returning the first matching result.
    Calls are cached. Subsequent calls to the same URL will used previous results.
    """
    if not url:
        raise OAIRepoInternalException("API call query without a URL provided.")
    if not jsonpath and not xpath:
        raise OAIRepoInternalException("API call query without a jsonpath or xpath provided.")

    if url not in APICALL_CACHE:
        try:
            resp = requests.get(url, timeout=10)
        except requests.RequestException as exc:
            raise OAIRepoExternalException(f"Call to API failed: {url}") from exc
        if not resp.status_code == 200:
            raise OAIRepoExternalException(f"Call to API returned {resp.status_code}: {url}")
        APICALL_CACHE[url] = resp
    resp = APICALL_CACHE[url]

    match = None
    if jsonpath:
        try:
            loaded = json.loads(resp.text)
            match = helpers.jsonpath_find_first(loaded, jsonpath)
        except jsonpath_ng.exceptions.JSONPathError as exc:
            raise OAIRepoInternalException(f"JSONPath is not valid: {jsonpath}") from exc
    elif xpath:
        try:
            loaded = etree.fromstring(resp.content)
            match = helpers.xpath_find_first(loaded, xpath)
        except etree.XPathError as exc:
            raise OAIRepoInternalException(f"XPath is not valid: {xpath}") from exc
    return match
