# Overview

## Implementation

The `oai_repo` module requires you first define an implementation of the
`oai_repo.DataInterface` class, filling out functionality for all the
functions within. You can name your implementation class whatever you'd like.

```python
import oai_repo

class MyOAIData(oai_repo.DataInterface):
    def get_identify(self):
        ident = oai_repo.Identify()
        ... # fill in the Identify data
        return ident

    def get_record_header(self, identifier):
        rechead = oai_repo.RecordHeader()
        ... # fill in the RecordHeader data
        return rechead

    ... # fill in the remaining methods
```

You can feel free to add additional attributes and methods to your implementation,
but at minimum you will need to complete all the methods from `DataInterface`.
```python
# Example of adding extra custom attributes and methods to your implementation
class MyOAIData(oai_repo.DataInterface):
    ...

    identifier_transform = oai_repo.helpers.Transform(...)

    def localid(self, identifier):
        """Custom method to convert OAI identifer to localid"""
        return self.identifier_transform.forward(identifier)

    def identifier(self, localid):
        """Custom method to convert from localid to OAI identifier"""
        return self.identifier_transform.reverse(localid)

```

## Processing Requests

A good first step is to just implement the `get_identify()` method and test that
before working on the completing the entire `DataInterface` implementation.

To run your OAI repository, you'll need to pass your custom class into
`oai_repo.OAIRepository`, which will serve as your OAI request processor.
```python
# args = { 'verb': 'Identify' }
try:
    repo = oai_repo.OAIRepository(MyOAIData())
    response = repo.process(args)
except oai_repo.OAIRepoExternalException as exc:
    # An API call timed out or returned a non-200 HTTP code.
    # Log the failure and abort with server HTTP 503.
except oai_repo.OAIRepoInternalException as exc:
    # There is a fault in how the DataInterface was implemented.
    # Log the failure and abort with server HTTP 500.
```

Once you have the response, you can check if the result is an OAIError
or not using a boolean check. You don't have to treat OAIError responses
any differently than a successful response, it is already a well formed
XML OAI compliant response, but this is an easy way to check nonetheless.
```python
if not response:
    print("We created an OAIError response.")
```

To retrieve the response as XML (an `lxml.etree._Element` specifically),
use the `root()` method.
```python
xml_response = response.root()
```

To get the raw response as bytes, just cast it as `bytes()`.
```python
xml_bytes = bytes(response)
```

At this point, you can take the response data and return it to the client,
or pass it back to whatever web framework you're using. That's it!

Reference for `OAIRepository` and `OAIResponse` are below, but be sure to read
through the [Implementation Classes](/implementation) documentation for
insight on how to create your customized `DataInterface` class.

::: oai_repo.repository.OAIRepository
    rendering:
      show_root_full_path: false
      merge_init_into_class: true
      heading_level: 2
      members:
       - "process"

::: oai_repo.repository.OAIResponse
    rendering:
      show_root_full_path: false
      heading_level: 2
      members:
       - "__bool__"
       - "__bytes__"
       - "root"
       - "xpath"
