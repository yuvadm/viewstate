from base64 import b64decode, b64encode

from .exceptions import ViewStateException

CONSTS = {
    100: {},
    101: '',
    102: 0,
    103: True,
    104: False
}

def parse_const(b):
    return CONSTS.get(b, None)

def parse(b):
    assert type(b) == bytes().__class__
    if len(b) == 1:
        return parse_const(b[0])
    return None


class ViewState(object):

    def __init__(self, base64=''):
        self.base64 = base64
        self.raw = b64decode(self.base64)
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
        return self.preamble == preamble

    def decode(self):
        if not self.is_valid():
            raise ViewStateException('Cannot decode invalid viewstate, bad preamble')
        self.decoded = parse(self.body)
        return self.decoded
