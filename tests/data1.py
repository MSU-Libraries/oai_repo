import oai_repo


class GoodData(oai_repo.DataInterface):
    """A OAI DataInterface without any failures"""
    def get_identify(self):
        """
        Create and return an instantiated Identify object.
        Returns:
            The Identify object with all properties set appropriately
        """
        ident = oai_repo.Identify()
        ident.repository_name = "My OAI Repo"
        ident.base_url = "https://my.example.edu/oai"
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

