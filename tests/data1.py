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

    def is_valid_identifier(self, identifier: str) -> bool:
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
