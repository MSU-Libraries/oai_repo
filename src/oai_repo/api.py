"""
API call handlers
"""
import json
import requests
import jsonpath_ng
from lxml import etree
from . import helpers
from .exceptions import (
    OAIErrorIdDoesNotExist,
    OAIRepoInternalException,
    OAIRepoExternalException,
    OAIErrorNoMetadataFormats,
)

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
        A lxml.etree.Element containing the root of the loaded XML
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

class APIQueries:
    """
    Wrapper class for performing API calls to remote sources
    """
    def __init__(self, repository):
        self.repository = repository

    def assert_identifier(self, identifier: str):
        """
        Given an OAI identifier string, assert that the record exists
        args:
            identifier (str):
        raises:
            OAIErrorIdDoesNotExist when the identifier is invalid or does not exist
        """
        localid = self.repository.localid(identifier)
        idexists = self.repository.config.apiqueries["idExists"]
        idexists["url"] = idexists["url"].replace("$localId$", localid)
        id_match = apicall_querypath(**idexists)
        if not id_match:
            raise OAIErrorIdDoesNotExist("The given identifier does not exist.")

    def metadata_formats(self, identifier: str):
        """
        Given an OAI identifier string, return the list of valid metadata prefixes
        args:
            identifier (str):
        raises:
            OAIErrorIdDoesNotExist when the identifier does not have any valid metadata formats
        """
        localid = self.repository.localid(identifier)
        metadataformats = self.repository.config.apiqueries["metadataFieldValues"]
        metadataformats["url"] = metadataformats["url"].replace("$localId$", localid)
        formats_found = apicall_querypath(**metadataformats)
        if not formats_found:
            raise OAIErrorNoMetadataFormats("No metadata fomats found for given identifier.")
        return formats_found

    def record_metadata(self, identifier, metadataprefix):
        """
        Given both an OAI identifier and metadata prefix, return the loaded root XML element
        of the API response.
        args:
            identifer (str):
            metadataprefix (str):
        raises:
            OAIErrorCannotDisseminateFormat
        """
        localid = self.repository.localid(identifier)
        localmetadataid = self.repository.localmetadataid(metadataprefix)
        recordmetadata = self.repository.config.apiqueries["recordMetadata"]
        recordmetadata["url"] = recordmetadata["url"]\
            .replace("$localId$", localid)\
            .replace("$localMetadataId$", localmetadataid)
        return apicall_getxml(**recordmetadata)

    def list_sets(self, resuptiontoken=None):
        """
        TODO
        args:
            resuptiontoken (str):
        raises:
            OAIErrorBadResumptionToken
            OAIErrorNoSetHierarchy
        """
        if "listSets" not in self.repository.config.apiqueries:
            raise OAIErrorNoSetHierarchy("This repository does not support sets.")

        # TODO
