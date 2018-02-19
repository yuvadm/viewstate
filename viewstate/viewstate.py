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

    @property
    def preamble(self):
        return self.raw[:2]

    @property
    def body(self):
        return self.raw[2:]

    def is_valid(self):
        format_marker = b'\xff'
        version_marker = b'\x01'
        preamble = format_marker + version_marker

        try:
            return self.preamble == preamble
        except AttributeError:
            return False

    def decode(self):
        if not self.is_valid():
            raise ViewStateException('Cannot decode invalid viewstate, bad preamble')
        self.decoded, self.remainder = parse(self.body)
        return self.decoded
