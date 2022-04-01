"""
OAI Error
"""
from __future__ import annotations      # To use non-string type hinting; can remove in Python 3.11
from typing import TYPE_CHECKING
from lxml import etree
from .response import OAIResponse
from .exceptions import OAIError
if TYPE_CHECKING:                       # Prevent circular imports for type hinting
    from .repository import OAIRepository

class OAIErrorResponse(OAIResponse):
    """
    Reponse for an request that generated an OAI error.
    """
    def __init__(self, repository: OAIRepository, exc: OAIError):
        self.code = exc.code()
        self.message = str(exc)
        super().__init__(repository)

    def __repr__(self):
        return f"OAIErrorResponse(code={self.code})"

    def body(self):
        """Error response body"""
        xmlb = etree.Element("error")
        xmlb.set(b"code", self.code.encode('utf8'))
        xmlb.text = self.message.encode('utf8')
        return xmlb

    def __bool__(self):
        """Indicates this response is for a failed request"""
        return False
