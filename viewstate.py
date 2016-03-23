from base64 import b64decode, b64encode


class ViewState(object):

    def __init__(self, base64_encoded):
        self.base64_encoded = base64_encoded
        self.raw = b64decode(self.base64_encoded)

    def is_valid(self):
        format_marker = b'\xff'
        version_marker = b'\x01'
        preamble = format_marker + version_marker
        return self.raw[:2] == preamble
