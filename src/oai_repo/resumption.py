"""
ResumptionToken functionality
"""
import time
import base64
from datetime import datetime, timezone
from hashlib import blake2s
from urllib.parse import urlencode, parse_qs
from lxml import etree
from . import helpers
from .exceptions import OAIErrorBadResumptionToken


class ResumptionToken:
    """
    A basic resumption token implementation
    """
    def __init__(self):
        # Original args to the request which originated this token
        self.args: dict = None
        # An optional unique state indicator which will invalidate the token if changed
        self._state_hash: bin = None
        self.cursor: int = None
        self.complete_list_size: int = None
        self.expiration_date: datetime = None

    def __repr__(self):
        return (
            f"ResumptionToken(cursor={self.cursor}, size={self.complete_list_size}, "
            f"expiration={self.expiration_date}, args={self.args})"
        )

    @property
    def state_hash(self):
        """
        Get a hash of the state

        Returns:
            The hexhash as a string, or None if no state was set
        """
        return self._state_hash

    def set_state(self, state: str):
        """
        Set the state hash from the provided state

        Args:
            state (str): The unqiue state, a string or an object that can be converted to a unique
                         string using __str__
        """
        self._state_hash = None
        if state:
            self._state_hash = blake2s(str(state).encode('utf8'), digest_size=8).hexdigest()

    def __bool__(self):
        """
        Return True if this ResumptionToken instance have data sufficient to generate
        a valid resumptionToken.
        """
        return bool(self.args and self.create())

    def xml(self, limit: int) -> etree._Element:
        """
        Return a formed xml element for the token

        Args:
            limit (int): The limit number of elements tha can be returned.
                         Used to determine if the token string should be included.

        Returns:
            The formed XML for the token, or None if no token can be generated
        """
        token = self.create()
        if not self.args or not token:
            return None

        cursor = self.cursor if self.cursor is not None else 0
        xmlr = etree.Element("resumptionToken")
        # Only add a token string if there are sufficient results to warrant it
        if self.complete_list_size is not None and cursor + limit < self.complete_list_size:
            xmlr.text = token

        xmlr.set('cursor', str(cursor))
        if self.complete_list_size:
            xmlr.set('completeListSize', str(self.complete_list_size))
        if self.expiration_date:
            expdate_str = helpers.granularity_format(
                "YYYY-MM-DDThh:mm:ssZ",
                self.expiration_date
            )
            xmlr.set('expiration_date', expdate_str)
        return xmlr

    def parse(self, token):
        """
        Parse token
        """
        try:
            targstr = base64.b64decode(token)
            tdict = {
                key.decode('utf8'): val[0].decode('utf8')
                for (key, val) in parse_qs(targstr).items()
            }
            if 'c' in tdict:
                self.cursor = int(tdict.pop('c'))
            if 's' in tdict:
                self.complete_list_size = int(tdict.pop('s'))
            if 'e' in tdict:
                self.expiration_date = datetime.fromtimestamp(
                    int(tdict.pop('e'))
                ).replace(tzinfo=timezone.utc)
            if 'h' in tdict:
                self._state_hash = tdict.pop('h')
            self.args = tdict
        except Exception as exc:
            raise OAIErrorBadResumptionToken from exc

        if self.expiration_date and self.expiration_date < datetime.now(timezone.utc):
            raise OAIErrorBadResumptionToken("The provided resumptionToken has expired.")

    def create(self):
        """
        Create a resumption token
        """
        tdict = self.args.copy() if self.args else {}
        if self.cursor is not None:
            tdict['c'] = self.cursor
        if self.complete_list_size is not None:
            tdict['s'] = self.complete_list_size
        if self.expiration_date is not None:
            tdict['e'] = int(time.mktime(self.expiration_date.timetuple()))
        if self.state_hash is not None:
            tdict['h'] = self.state_hash
        targstr = urlencode(tdict).encode('utf8')
        return base64.b64encode(targstr)
