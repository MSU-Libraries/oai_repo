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
        "type": "list",
        "items": [
            {
                "type": "string",
                "allowed": ["replace"]
            },
            { "type": "string" },
            { "type": "string" }
        ]
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
                "fieldValue": {
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
    "metadataFormatsQuery": {
        "required": True,
        "type": "dict",
        "schema": {
            "idExists": {
                "required": True,
                "type": "dict",
                "oneof_schema": _url_query
            },
            "fieldValues": {
                "required": True,
                "type": "dict",
                "oneof_schema": _url_query
            }
        }
    },
    "localId": {
        "required": True,
        "type": "dict",
        "schema": {
            "identifierPrefix": {
                "required": True,
                "type": "string",
            },
            "transforms": {
                "type": "list",
                "oneof_schema": _transform_schemas,
            }
        }
    }
}
