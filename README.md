# oai_repo
The `oai_repo` Python module provides a configurable implementation of an
[OAI-PMH](http://openarchives.org/OAI/openarchivesprotocol.html) compatible repository.

At its simplest, using `oai_repo` involves:
1. Implementeing a `DataInterface` class to perform several pre-defined actions.
2. Adding a few lines of Python code similar to:
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

## Features
* Completely customizable to work with any backend you have.
* Compliant to the OAI-PMH 2.0 specification.
* Easy to integrate within any Python application.

## Installation
Requires Python 3.10+

Installation via `pip` is recommended:
```
pip install oai_repo
```

## Implementing the DataInterface Class
TODO docs placeholder

## Available Helper Methods
TODO docs placeholder

### URL/Path Pairs
To have the OAI repository load data dymanically, the config file allows for
querying an API and using wither JSONPath or XPath on the result. In the config
field list, this is specified by `url`/`*path`. This can be either of:  

**URL/JSONPath**  
* `url` _(String)_: A URL to call
* `jsonpath` _(String)_: A JSONPath to call on the results of the URL, retrieving the first match.

**URL/XPath**  
* `url` _(String)_: A URL to call
* `xpath` _(String)_: An XPath to call on the results of the URL, retrieving the first match.

## The Code
Once the config file is defined, adding `oai_repo` to your application is simple.

Create respository instance, passing in config:
```python
import oai_repo
from .myoaidata import MyOAIData

repo = oai_repo.OAIRepository(MyOAIData)
```

Pass in URL arguments as a dict to process the request:
```python
response = repo.process( request.args )
```

The response can be accessed directly as XML:
```python
xml_root_element = response.root()
```

Or response can be cast into a fully formed XML document:
```python
xml_doc_as_bytes = bytes(response)
```

The `OAIRepository` may raise the `OAIRepoInternalException`
and `OAIRepoExternalException` exceptions:
```python
try:
    repo = oai_repo.OAIRepository("/path/config.json")
    response = repo.process( args )
except oai_repo.OAIRepoExternalException as exc:
    # An API call timed out or returned a non-200 HTTP code.
    # Log the failure and abort with server HTTP 503.
except oai_repo.OAIRepoInternalException as exc:
    # There is a missing or bad configuration setting.
    # Log the failure and abort with server HTTP 500.
```

## Author and License
The `oai_repo` module was developed at the Michigan State University Libraries.
It is released under the Apache License version 2.0.

## Copyright
Copyright (c) 2022 Michigan State University Board of Trustees
