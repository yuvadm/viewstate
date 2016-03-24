from base64 import b64decode, b64encode


CONSTS = {
    '\x64': {},
    '\x65': '',
    '\x66': 0,
    '\x67': True,
    '\x68': False
}

def parse():
    pass


class ViewState(object):

    def __init__(self, base64=''):
        self.base64 = base64
        self.raw = b64decode(self.base64)
        self.decoded = None

    @property
    def body(self):
        return self.raw[:2]

    def is_valid(self):
        format_marker = b'\xff'
        version_marker = b'\x01'
        preamble = format_marker + version_marker
        return self.body == preamble

    def decode(self):
        if not self.is_valid():
            raise Exception('Cannot decode invalid viewstate, bad preamble')
        self.decoded = parse(self.body)
        return self.decoded
