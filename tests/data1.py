from datetime import datetime
import oai_repo

class GoodData(oai_repo.DataInterface):
    """A OAI DataInterface without any failures"""
    def localid(self, identifier):
        """ Custom added method to convert to localid"""
        return oai_repo.Transform([
            { "prefix": ["del", "oai:d.lib.msu.edu:"] },
            { "replace": ["_", ":"] }
        ]).forward(identifier)

    def get_identify(self):
        """
        Create and return an instantiated Identify object.
        Returns:
            The Identify object with all properties set appropriately
        """
        ident = oai_repo.Identify()
        ident.repository_name = "My OAI Repo"
        ident.base_url = "https://d.lib.msu.edu/oai"
        ident.admin_email.append("oai@example.edu")
        ident.deleted_record = "no"
        ident.granularity = "YYYY-MM-DD"
        ident.compression = []
        ident.earliest_datestamp = "2000-01-31"
        ident.description.append(
        """
        <oai-identifier xmlns="http://www.openarchives.org/OAI/2.0/"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai-identifier http://www.openarchives.org/OAI/2.0/oai-identifier.xsd">
            <scheme>oai</scheme>
            <repositoryIdentifier>d.lib.msu.edu</repositoryIdentifier>
            <delimiter>:</delimiter>
            <sampleIdentifier>oai:d.lib.msu.edu:123</sampleIdentifier>
        </oai-identifier>
        """)
        return ident

    def is_valid_identifier(self, identifier: str):
        """
        Determine if an identifier string is valid format and exists.
        Args:
            identifier (str): A string to check for being an identifier
        Returns:
            True if given string is an identifier that exists.
        """
        localid = self.localid(identifier)
        idexists_api = {
            "url": f"https://sandhill.lib.msu.edu/search.json?q=PID:\"{localid}\"&fl=fedora_datastreams_ms",
            "jsonpath": "$.response.docs[0]"
        }
        id_match = oai_repo.apicall_querypath(**idexists_api)
        return bool(id_match)

    def get_metadata_formats(self, identifier: str|None = None):
        """
        Return a list of metadata prefixes for the identifier. If no identifier
        identifieris passed, then list must contain all possible prefixes for the repository.
        Args:
            identifier (str|None): A valid identifer string
        Returns:
            A list of instantiated MetadataFormat objects with all properties set appropriately
            to the identifer.
            If identifier is None, then list of all possible MetadataFormat objects for the
            entire repository.
        """
        allowed_mdfs = {
            'DC': oai_repo.MetadataFormat(
                "oai_dc",
                "http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
                "http://www.openarchives.org/OAI/2.0/oai_dc/"
            ),
            'MODS': oai_repo.MetadataFormat(
                "mods",
                "http://www.loc.gov/standards/mods/v3/mods-3-4.xsd",
                "http://www.loc.gov/mods/v3"
            )
        }
        if not identifier:
            return list(allowed_mdfs.values())
        localid = self.localid(identifier)
        metadataid_api = {
            "url": f"https://sandhill.lib.msu.edu/search.json?q=PID:\"{localid}\"&fl=fedora_datastreams_ms",
            "jsonpath": "$.response.docs[0].fedora_datastreams_ms"
        }
        metadataid_match = oai_repo.apicall_querypath(**metadataid_api)
        mdfs = []
        for localmetaid, mdf in allowed_mdfs.items():
            if localmetaid in metadataid_match:
                mdfs.append(mdf)
        return mdfs

    def get_record_header(self, identifier: str):
        """
        Return a RecordHeader instance for the identifier.
        Args:
            identifier (str): A valid identifier string
        Returns:
            The RecordHeader object with all properties set appropriately.
        """
        raise NotImplementedError

    def get_record_metadata(self, identifier: str, metadataprefix: str):
        """
        Return a lxml.etree.Element representing the root element of the
        metadata found for the given prefix.
        Args:
            identifier (str): A valid identifer string
            metadataprefix (str): A metadata prefix
        Returns:
            The lxml.etree.Element for the requested record metadata,
            or None if record has no metadata for provided prefix.
        Important:
            oai_repo will wrap the response with a `<metadata>` tag; do not add it yourself.
        """
        raise NotImplementedError

    def get_record_abouts(self, identifier: str):
        """
        Return a list of XML elements which will populate the `<about>` tags in GetRecord responses.
        Args:
            identifier (str): A valid identifier string
        Returns:
            A list of lxml.etree.Elements to populate `<about>` tags for the record.
        Important:
            oai_repo will wrap the response with a `<about>` tag; do not add it yourself.
        """
        raise NotImplementedError

    def list_set_specs(self, identifier: str=None, cursor: int=0, limit: int=100):
        """
        Return a list of setSpec string for the given identifier string if provided,
        or the list of all valid setSpec strings for the repository if no identifier is None.
        Args:
            identifier (str): a valid identifier string
            cursor (int): position in results to start from
            limit (int): maximum number of results to return, starting from cursor position
        Returns:
            A tuple of length 3:
             1. A list of setSpec strings or None if the repository does not support sets.
             2. A `cursor` (int) to send with a `resumptionToken`,
                or -1 if no `cursor` should be sent,
                or None if no `resuptionToken` is needed.
             3. The `completeListSize` to send with a `resuptionToken` or Null to not send.
        """
        # TODO if identifier is passed
        # TODO cursor position, limit
        setspec_api = {
            "url": "https://sandhill-1.devel.lib.msu.edu/search.json?q=PID:*\\:root&rows=99999&fl=PID,collection_hierarchy&sort=PID%20asc&facet=false",
            "jsonpath": "$.response"
        }
        setspec_resp = oai_repo.apicall_querypath(**setspec_api)
        size = setspec_resp["numFound"]
        new_cursor = None if cursor > size else cursor + limit
        setspecs = []
        # generate a setspec
        to_setspec = oai_repo.Transform([
            { "prefix": ["del", "info:fedora/"] },
            { "suffix": ["del", ":root"] },
            { "replace": [":", "_"] }   # colons disallowed per OAI spec
        ])
        for doc in setspec_resp["docs"]:
            # prepend with self PID
            newset = [doc["PID"]]
            # add collction hierarchy, but not top level msul
            if "collection_hierarchy" in doc:
                newset.extend(doc["collection_hierarchy"][:-1])
            # transform all
            for idx, val in enumerate(newset):
                newset[idx] = to_setspec.forward(val)
            # reverse order and join by ':'
            setspecs.append(':'.join(reversed(newset)))
        return setspecs, new_cursor, size

    def get_set(self, setspec: str):
        """
        Return an instatiated OAI Set object for the provided setSpect string.
        Args:
            setspec (str): a setSpec string
        Returns:
            The Set object with all properties set appropriately,
            or None if the setspec is not valid or does not exist.
        """
        raise NotImplementedError

    def list_identifiers(self,
        metadataprefix: str,
        filter_from: datetime = None,
        filter_until: datetime = None,
        filter_set: str = None,
        cursor: int = 0,
        limit: int = 100
    ):
        """
        Return valid identifier strings, filtered appropriately to passed parameters.
        Args:
            metadataprefix (str): The metadata prefix to match.
            filter_from (datetime.datetime): Include only identifiers on or after given datetime.
            filter_until (datetime.datetime): Include only identifiers on or before given datetime.
            filter_set (str): Include only identifers within the matching setSpec string.
            cursor (int): position in results to start retrieving from
            limit (int): maximum number of results to return, starting from cursor position
        Returns:
            A tuple of length 3:
             1. A list of valid identifier strings for the repository, filtered appropriately.
             2. A `cursor` (int) to send with a `resumptionToken`,
                or -1 if no `cursor` should be sent,
                or None if no `resuptionToken` is needed.
             3. The `completeListSize` to send with a `resuptionToken`, or Null not send.
        """
        raise NotImplementedError
