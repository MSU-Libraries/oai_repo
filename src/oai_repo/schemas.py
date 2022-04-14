"""
Cerberus Schemas
"""

_url_query = [
    {
        "url": {
            "required": True,
            "type": "string",
        },
        "jsonpath": {
            "required": True,
            "type": "string",
        }
    },
    {
        "url": {
            "required": True,
            "type": "string",
        },
        "xpath": {
            "required": True,
            "type": "string",
        }
    }
]

_earliestdatestamp_schemas = [
    {
        "static": {
            "required": True,
            "type": "string",
        }
    }
] + _url_query

_transform_schemas = [
    {
        "type": "dict",
        "schema": {
            "replace": {
                "required": True,
                "type": "list",
                "items": [
                    { "type": "string", "required": True },
                    { "type": "string", "required": True }
                ]
            }
        }
    },
    {
        "type": "dict",
        "schema": {
            "prefix": {
                "type": "list",
                "items": [
                    {
                        "type": "string",
                        "required": True,
                        "allowed": ["add", "del"]
                    },
                    { "type": "string", "required": True }
                ]
            }
        }
    },
    {
        "type": "dict",
        "schema": {
            "suffix": {
                "type": "list",
                "items": [
                    {
                        "type": "string",
                        "required": True,
                        "allowed": ["add", "del"]
                    },
                    { "type": "string", "required": True }
                ]
            }
        }
    },
    {
        "type": "dict",
        "schema": {
            "case": {
                "type": "list",
                "items": [
                    {
                        "type": "string",
                        "required": True,
                        "allowed": ["upper", "lower"]
                    }
                ]
            }
        }
    }
]

config_schema = {
    "repositoryName": {
        "required": True,
        "type": "string",
    },
    "baseURL": {
        "required": True,
        "type": "string",
    },
    "adminEmail": {
        "required": True,
        "type": "list",
        "schema": {
            "type": "string"
        }
    },
    "metadataFormats": {
        "required": True,
        "type": "list",
        "minlength": 1,
        "schema": {
            "type": "dict",
            "schema": {
                "metadataPrefix": {
                    "required": True,
                    "type": "string"
                },
                "schema": {
                    "required": True,
                    "type": "string"
                },
                "metadataNamespace": {
                    "required": True,
                    "type": "string"
                },
            }
        }
    },
    "earliestDatestamp": {
        "required": True,
        "oneof_schema": _earliestdatestamp_schemas,
    },
    "deletedRecord": {
        "required": True,
        "allowed": ["no", "transient", "persistent"],
    },
    "granularity": {
        "required": True,
        "allowed": ["YYYY-MM-DD", "YYYY-MM-DDThh:mm:ssZ"],
    },
    "compression": {
        "type": "list",
        "schema": {
            "type": "string"
        }
    },
    "description": {
        "type": "list",
        "schema": {
            "type": "string"
        }
    },
    "apiQueries": {
        "required": True,
        "type": "dict",
        "schema": {
            "idExists": {
                "required": True,
                "type": "dict",
                "oneof_schema": _url_query
            },
            "metadataFieldValues": {
                "required": True,
                "type": "dict",
                "oneof_schema": _url_query
            },
            "recordMetadata": {
                "required": True,
                "type": "dict",
                "schema": {
                    "url": {
                        "required": True,
                        "type": "string",
                    }
                }
            },
            "listSets": {
                "type": "dict",
                "oneof_schema": _url_query
            },
        }
    },
    "localMetadataId": {
        "required": True,
        "type": "list",
        "anyof_schema": _transform_schemas
    },
    "localId": {
        "required": True,
        "type": "list",
        "anyof_schema": _transform_schemas
    },
    "setName": {
        "required": True,
        "type": "list",
        "anyof_schema": _transform_schemas
    }
}
