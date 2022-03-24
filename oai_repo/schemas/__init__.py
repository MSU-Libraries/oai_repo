"""
Cerberus Schemas
"""

_earliestdatestamp_schemas = [
    {
        "static": {
            "required": True,
            "type": "string",
        }
    },
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

config_schema = {
    "repositoryName": {
        "required": True,
        "type": "string",
    },
    "baseUrl": {
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
                }
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
            "type": "dict"
        }
    }
}
