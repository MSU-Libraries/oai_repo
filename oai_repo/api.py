"""
API call handlers
"""
import json
import requests
import jsonpath_ng
from lxml import etree
from . import helpers
from .exceptions import OAIRepoInternalError

def apicall_querypath(
    url: str = None,
    jsonpath: str = None,
    xpath: str = None,
    **kwargs
):
    """
    Perform an API call and then either an jsonpath or xpath query,
    returning the first matching result.
    """
    url = kwargs["url"] if "url" in kwargs else url
    jsonpath = kwargs["jsonpath"] if "jsonpath" in kwargs else jsonpath
    xpath = kwargs["xpath"] if "xpath" in kwargs else xpath
    if not url:
        raise OAIRepoInternalError("API call query without a URL provided.")
    if not jsonpath and not xpath:
        raise OAIRepoInternalError("API call query without a jsonpath or xpath provided.")

    try:
        resp = requests.get(url, timeout=10)
    except requests.RequestException as exc:
        raise OAIRepoInternalError(f"Call to API failed: {url}") from exc
    if not resp.status_code == 200:
        raise OAIRepoInternalError(f"Call to API returned {resp.status_code}: {url}")

    match = None
    if jsonpath:
        try:
            loaded = json.loads(resp.text)
            match = helpers.jsonpath_find_first(loaded, jsonpath)
        except jsonpath_ng.exceptions.JSONPathError as exc:
            raise OAIRepoInternalError(f"JSONPath is not valid: {jsonpath}") from exc
    elif xpath:
        try:
            loaded = etree.fromstring(resp.content)
            match = helpers.xpath_find_first(loaded, xpath)
        except etree.XPathError as exc:
            raise OAIRepoInternalError(f"XPath is not valid: {xpath}") from exc
    return match
