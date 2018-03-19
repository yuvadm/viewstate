from base64 import b64decode, b64encode
from binascii import Error as BinAsciiError

from .exceptions import ViewStateException
from .parse import parse


class ViewState(object):

    def __init__(self, base64=None, raw=None):
        if base64:
            self.base64 = base64
            try:
                self.raw = b64decode(self.base64)
            except BinAsciiError as bae:
                raise ViewStateException('Cannot decode base64 input')
        elif raw:
            self.raw = raw
        self.decoded = None
        self.mac = None
        self.signature = None

    @property
    def preamble(self):
        return self.raw[:2]

    @property
    def body(self):
        return self.raw[2:]

    def is_valid(self):
        FORMAT_MARKER = b'\xff'
        VERSION_MARKER = b'\x01'
        PREAMBLE = FORMAT_MARKER + VERSION_MARKER

        try:
            return self.preamble == PREAMBLE
        except AttributeError:
            return False

    def decode(self):
        if not self.is_valid():
            raise ViewStateException('Cannot decode invalid viewstate, bad preamble')

        self.decoded, self.remainder = parse(self.body)

        if self.remainder:
            if len(self.remainder) == 20:
                self.mac = 'hmac_sha1'
            elif len(self.remainder) == 32:
                self.mac = 'hmac_sha256'
            else:
                self.mac = 'unknown'
            self.signature = self.remainder

        return self.decoded
