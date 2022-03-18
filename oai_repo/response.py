"""
Handling OAI-PMH responses
"""

XML_HEADER = '<?xml version="1.0" encoding="UTF-8" ?>'
NS = {
    'dc' : 'http://purl.org/dc/elements/1.1/',
    'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
}
XSD = {
    "OAI": "http://www.openarchives.org/OAI/2.0/",
    "XSI": "http://www.w3.org/2001/XMLSchema-instance",
    "OAI_SCHEMA": "http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd",
    "OAI_DC": "http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
    "OAI_IDENTIFIER": "http://www.openarchives.org/OAI/2.0/oai-identifier http://www.openarchives.org/OAI/2.0/oai-identifier.xsd",
}

class OAIResponse:
    """
    """
