# oai_repo
The `oai_repo` Python module provides a configurable implementation of a
[OAI-PMH](http://openarchives.org/OAI/openarchivesprotocol.html) compatible repository.

At its simplest, you:
1. define a config file
2. use a bit of Python code similar to this
```
import oai_repo

# Create the repository, loading the config
repo = oai_repo.OAIRepository("/my/config.json")
# Pass in URL arguments as a dict to be processed
response = repo.process( { "verb": "Identify" } )
print( type(response.root()) )  # lxml.etree.Element
print( bytes(response) )        # Example output below
```
```
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
        <adminEmail>fedcomall@mail.lib.msu.edu</adminEmail>
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

## The Configuration File
TODO stub

## The Code
TODO stub

## Author and License
The `oai_repo` module was developed by the Michigan State University Libraries.
It is released under the Apache License version 2.0.

## Copyright
Copyright 2022 Michigan State University Board of Trustees
