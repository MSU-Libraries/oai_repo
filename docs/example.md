# Simple Example

At its simplest, using `oai_repo` involves:

1. Implementeing a `DataInterface` class to perform several pre-defined actions.
2. Adding a few lines of Python code to your app similar to:
```python
import oai_repo
from .myoaidata import MyOAIData

# Create the repository, passing your implemented DataInterface
repo = oai_repo.OAIRepository(MyOAIData())

# Pass in URL arguments as a dict to be processed
response = repo.process( { "verb": "Identify" } )
print( type(response.root()) )  # lxml.etree.Element
print( bytes(response) )        # XML byte response
```
Resulting in a complete OAI response:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <responseDate>2022-03-24T05:50:06Z</responseDate>
    <request>https://d.lib.msu.edu/oai</request>
    <Identify>
        <repositoryName>MSU Libraries Digital Repository</repositoryName>
        <baseURL>https://d.lib.msu.edu/oai</baseURL>
        <protocolVersion>2.0</protocolVersion>
        <adminEmail>admin@example.edu</adminEmail>
        <earliestDatestamp>2012-08-21T13:49:50Z</earliestDatestamp>
        <deletedRecord>no</deletedRecord>
        <granularity>YYYY-MM-DDThh:mm:ssZ</granularity>
        <description>
            <oai-identifier xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai-identifier
              http://www.openarchives.org/OAI/2.0/oai-identifier.xsd">
                <scheme>oai</scheme>
                <repositoryIdentifier>d.lib.msu.edu</repositoryIdentifier>
                <delimiter>:</delimiter>
                <sampleIdentifier>oai:d.lib.msu.edu:123</sampleIdentifier>
            </oai-identifier>
        </description>
    </Identify>
</OAI-PMH>
```

The missing piece above is the `MyOAIData` class, although you can name this
class whatever you'd like. When you create the `oai_repo.OAIRepository` class,
you need to pass it an implemented `oai_repo.DataInterface` class. This
`DataInterface` provides you a template of the functionality which you must
code yourself.

For example, in order for the OAI `Identify` verb to function, you must
implement the `DataInterface` `get_identity()` method.
```python
from oai_repo import DataInterface, Identity

class MyOAIData(DataInterface):
    def get_identify(self) -> Identify:
        ident = Identity()
        ident.repository_name = "My OAI Repository"
        ident.base_url = f"https://example.edu/oai"
        ident.granularity = "YYYY-MM-DDThh:mm:ssZ"
        ... # fill in the rest of the Identify info
        return ident
```

To have full OAI functionality, you will need to implement all the methods
defined in the `DataInterface` class. Refer to the [Implementation Classes](implementation/)
documentation for more information.
