from datetime import datetime
from urllib.parse import quote
from lxml import etree
import oai_repo

class DataWithSets(oai_repo.DataInterface):
    """A OAI DataInterface without any failures"""
    identifier_transform = oai_repo.Transform([
        { "prefix": ["del", "oai:d.lib.msu.edu:"] },
        { "replace": ["_", ":"] }
    ])
    setspec_transform = oai_repo.Transform([
        { "prefix": ["del", "info:fedora/"] },
        { "suffix": ["del", ":root"] },
        { "replace": [":", "_"] }   # colons disallowed per OAI spec
    ])

    def __init__(self, timestamp=False) -> None:
        super().__init__()
        self.timestamp = timestamp

    def localid(self, identifier):
        """Custom method to convert to localid"""
        return self.identifier_transform.forward(identifier)

    def identifier(self, localid):
        """Custom method to convert from localid"""
        return self.identifier_transform.reverse(localid)

    def localmetadataid(self, metadataprefix):
        """Custom method to convert metadataPrefix to localmetadataid"""
        return oai_repo.Transform([
            { "prefix": ["del", "oai_"] },
            { "case": ["upper"] }
        ]).forward(metadataprefix)

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
        if self.timestamp:
            ident.granularity = "YYYY-MM-DDThh:mm:ssZ"
        else:
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
            "url": f"https://d.lib.msu.edu/search.json?q=PID:\"{localid}\"&fl=fedora_datastreams_ms",
            "jsonpath": "$.response.docs[0]"
        }
        id_match = oai_repo.helpers.apicall_querypath(**idexists_api)
        return bool(id_match)

    def get_metadata_formats(self, identifier: str|None = None):
        """
        Return a list of metadata prefixes for the identifier. If no identifier
        identifier is passed, then list must contain all possible prefixes for the repository.
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
            "url": f"https://d.lib.msu.edu/search.json?q=PID:\"{localid}\"&fl=fedora_datastreams_ms",
            "jsonpath": "$.response.docs[0].fedora_datastreams_ms"
        }
        metadataid_match = oai_repo.helpers.apicall_querypath(**metadataid_api)
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
        localid = self.localid(identifier)
        lastmod_api = {
            "url": f"https://d.lib.msu.edu/search.json?q=PID:\"{localid}\"&fl=fgs_lastModifiedDate_dt",
            "jsonpath": "$.response.docs[0].fgs_lastModifiedDate_dt"
        }
        lastmod_match = oai_repo.helpers.apicall_querypath(**lastmod_api)
        setspecs, _, _ = self.list_set_specs(identifier)
        return oai_repo.RecordHeader(
            identifier,
            lastmod_match,
            setspecs
        )

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
        localid = self.localid(identifier)
        localmetadataid = self.localmetadataid(metadataprefix)
        getmetadata_api = {
            "url": f"https://d.lib.msu.edu/{localid}/{localmetadataid}/view"
        }
        return oai_repo.helpers.apicall_getxml(**getmetadata_api)

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
        testabout = etree.fromstring(b"<ignoreme>Just a test.</ignoreme>")
        return [testabout]

    def list_set_specs(self, identifier: str=None, cursor: int=0):
        """
        Return a list of setSpec string for the given identifier string if provided,
        or the list of all valid setSpec strings for the repository if no identifier is None.
        Args:
            identifier (str): a valid identifier string
            cursor (int): position in results to start from
        Returns:
            A tuple of length 3:
             1. (list|None) List of setSpec strings or None if the repository does not support sets.
             2. (int|None) The `completeListSize` to send with a `resumptionToken` or Null to not send.
             3. (Any|None) An str()-able value which indicates the constant-ness of the complete
                result set. If any value in the results changes, this value should also
                change. A changed value will invalidate current `resumptionToken`s.
                If None, the `resumptionToken`s will only invalidate based on
                reduction in in `completeListSize`.
        """
        # TODO cursor position, limit
        pid_match = identifier[identifier.rfind(":")+1:].replace("_", "\\:") if identifier else "*\\:root"
        setspec_api = {
            "url": (
                f"https://d.lib.msu.edu/search.json?q=PID:{pid_match}&rows=99999"
                "&fl=PID,collection_hierarchy&sort=PID%20asc&facet=false"
            ),
            "jsonpath": "$.response"
        }
        setspec_resp = oai_repo.helpers.apicall_querypath(**setspec_api)
        size = setspec_resp["numFound"]
        setspecs = []
        for doc in setspec_resp["docs"]:
            # prepend with self PID
            newset = [doc["PID"]]
            # add collction hierarchy, but not top level msul
            if "collection_hierarchy" in doc:
                newset.extend(doc["collection_hierarchy"][:-1])
            # transform all
            for idx, val in enumerate(newset):
                newset[idx] = self.setspec_transform.forward(val)
            # reverse order and join by ':'
            newset = list(reversed(newset))
            if not identifier:
                setspecs.append(':'.join(newset))
            else:
                # if for an individual identifier, build hierarchy
                while len(newset) > 1:
                    newset.pop()
                    setspecs.append(':'.join(newset))
        return setspecs, size, None

    def get_set(self, setspec: str):
        """
        Return an instatiated OAI Set object for the provided setSpect string.
        Args:
            setspec (str): a setSpec string
        Returns:
            The Set object with all properties set appropriately,
            or None if the setspec is not valid or does not exist.
        """
        pid_match = setspec[setspec.rfind(":")+1:] + ":root"
        dcfields = [
            "dc.title", "dc.creator", "dc.subject", "dc.description", "dc.publisher",
            "dc.contributor", "dc.date", "dc.type", "dc.format", "dc.identifier", "dc.source",
            "dc.language", "dc.relation", "dc.coverage", "dc.rights"
        ]
        set_api = {
            "url": f"https://d.lib.msu.edu/search.json?q=PID:{pid_match}&rows=1&fl=fgs_label_s,{','.join(dcfields)}&facet=false",
            "jsonpath": "$.response.docs[0]"
        }
        set_resp = oai_repo.helpers.apicall_querypath(**set_api)
        if set_resp is None:
            return None

        xdesc = etree.Element(
            b"{" + oai_repo.NSMAP_OAIDC["oai_dc"] + b"}dc",
            nsmap=oai_repo.NSMAP_OAIDC
        )

        # Create description
        xdesc.set(*oai_repo.OAIDC_SCHEMA)
        for dcf in dcfields:
            if dcf not in set_resp:
                continue
            for dcv in set_resp[dcf]:
                xdc = etree.SubElement(
                    xdesc,
                    dcf.encode().replace(b"dc.", b"{" + oai_repo.NSMAP_OAIDC["dc"] + b"}")
                )
                xdc.text = dcv

        return oai_repo.Set(
            setspec,
            set_resp["fgs_label_s"],
            [xdesc]
        )

    def list_identifiers(self,
        metadataprefix: str,
        filter_from: datetime = None,
        filter_until: datetime = None,
        filter_set: str = None,
        cursor: int = 0
    ):
        """
        Return valid identifier strings, filtered appropriately to passed parameters.
        Args:
            metadataprefix (str): The metadata prefix to match.
            filter_from (datetime.datetime): Include only identifiers on or after given datetime.
            filter_until (datetime.datetime): Include only identifiers on or before given datetime.
            filter_set (str): Include only identifers within the matching setSpec string.
            cursor (int): position in results to start retrieving from
        Returns:
            A tuple of length 3:
             1. (list) Valid identifier strings for the repository, filtered appropriately.
             2. (int|None) The `completeListSize` to send with a `resumptionToken` or Null to not send.
             3. (Any|None) An str()-able value which indicates the constant-ness of the complete
                result set. If any value in the results changes, this value should also
                change. A changed value will invalidate current `resumptionToken`s.
                If None, the `resumptionToken`s will only invalidate based on
                reduction in in `completeListSize`.
        """
        identifier_url = (
            f"https://d.lib.msu.edu/search.json?q=-PID:*\\:root&rows={int(self.limit)}"
            f"&fl=PID&sort=PID asc&facet=false&start={int(cursor)}"
        )
        if filter_from or filter_until:
            date_start = oai_repo.helpers.datestamp_long(filter_from) if filter_from else "*"
            date_end = oai_repo.helpers.datestamp_long(filter_until) if filter_until else "*"
            identifier_url += f"&fq=fgs_lastModifiedDate_dt:[{date_start} TO {date_end}]"
        if filter_set:
            singleset = filter_set.split(":")[-1]
            localset = self.setspec_transform.reverse(singleset)
            identifier_url += "&fq=collection_hierarchy:"+quote(localset.replace(":", "\\:"))

        identifier_resp = oai_repo.helpers.apicall_querypath(
            url=identifier_url,
            jsonpath="$.response"
        )
        size = identifier_resp["numFound"]
        pids = oai_repo.helpers.jsonpath_find(identifier_resp, '$.docs[*].PID')
        identifiers = [self.identifier(pid) for pid in pids]
        return identifiers, size, None
