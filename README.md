# oai_repo
The `oai_repo` Python module provides a configurable implementation of a
[OAI-PMH](http://openarchives.org/OAI/openarchivesprotocol.html) compatible repository.

At its simplest, using `oai_repo` involves:
1. Defining a config file.
2. Adding a few lines of Python code similar to:
```python
import oai_repo

# Create the repository, loading the config
repo = oai_repo.OAIRepository("/my/config.json")

# Pass in URL arguments as a dict to be processed
response = repo.process( { "verb": "Identify" } )
print( type(response.root()) )  # lxml.etree.Element
print( bytes(response) )        # Example output below
```
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
* Works with either a JSON or XML based API backends.
* Compliant to the OAI-PMH 2.0 specification.
* Easy to integrate within any Python application.

## Installation
Requires Python 3.9+

Installation via `pip` is recommended:
```
pip install oai_repo
```

## The Configuration File
The `oai_repo` config file is a JSON file which specifies all the information your OAI-PMH repository needs to operate.

Fields in the config file are:  
`repositoryName` _(Required, String)_: The name of the repository put into the OAI `Identify` verb.

`baseURL` _(Required, String)_: The URL reported in the OAI `Identify` verb and in the `request` element in all responses.

`adminEmail` _(Required, List, Minimum 1)_: A list of email addresses to include in the `Identify` verb.

`earliestDatestamp` _(Required, Dict)_: Define the earliest datestamp as reported in the `Identify` verb. May be set in two ways:

1. `static` _(String)_: A manually set datestamp string.
2. `url`/`*path` pair: Dynamically query for this value.

`deletedRecord` _(Required, String)_: The value to return in the OAI `Identify` verb.

`granularity` _(Required, String)_: The value to return in the OAI `Identify` verb.

`compression` _(Optional, List)_: A list of supported compression types. Per the OAI-PMH specification, do not set the implied `identity` coding.

`description` _(Optional, List)_: A list of XML files to load and serve as descriptions in the OAI `Identify` verb. This file must have a root `<description>` element with appropriate XML namespaces set where needed.

`metadataFormats` _(Required, List)_: List of metadata formats that will be made available via OAI repository.
 * `metadataPrefix` _(String)_: The value to be placed in the `ListMetadataFormats` response.
 * `schema` _(String)_: The value to be placed in the `ListMetadataFormats` response.
 * `metadataNamespace` _(String)_: The to be value placed in the `ListMetadataFormats` response.
 * `fieldValue` _(String)_: The value to be matched in `metadataFormatsQuery.fieldValues`. (An identifier is considered to have a metadata format when `fieldValue` is contained within the results of the `fieldValues` query.)

`metadataFormatsQuery` _(Required, Dict)_: TODO

`localId` _(Required, Dict)_: TODO

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
repo = oai_repo.OAIRepository("/path/config.json")
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
The `oai_repo` module was developed by the Michigan State University Libraries.
It is released under the Apache License version 2.0.

## Copyright
Copyright 2022 Michigan State University Board of Trustees
