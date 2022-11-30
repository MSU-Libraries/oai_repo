# Exceptions

Exceptions are failures within `oai_repo`. These are not to be confused with [OAI Errors](https://www.openarchives.org/OAI/openarchivesprotocol.html#ErrorConditions) which are handled automatically by `oai_repo`.

There are two core exceptions within `oai_repo`:

* `OAIRepoInternalException`: This should be raised when there was a fault in how the `DataInterface` was implemented.
* `OAIRepoExternalException`: This should be raised when an external issue prevented a response from being generated (e.g. an API failed).

Additionally, for any method in the `DataInterface` class that is called but not yet implemented, `oai_repo` will
raise a `NotImplementedError`.

It is up to you to catch and handle the above exceptions:
```python
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
