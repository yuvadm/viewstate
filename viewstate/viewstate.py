from base64 import b64decode
from binascii import Error as BinAsciiError
try:
    from Crypto.Cipher import AES, DES3, DES
except ImportError:
    from Cryptodome.Cipher import AES, DES3, DES

from .keymodes import Encryption, MAC
from .exceptions import ViewStateException
from .parse import Parser


class ViewState(object):
    def __init__(self, base64=None, raw=None, encryption_mode=None, encryption_key=None, mac_mode=None):
        if base64:
            self.base64 = base64
            try:
                self.raw = b64decode(self.base64)
            except BinAsciiError:
                raise ViewStateException("Cannot decode base64 input")
        elif raw:
            self.raw = raw
        self.decrypt = False
        if isinstance(encryption_mode, Encryption):
            if encryption_key is not None and isinstance(mac_mode, MAC):
                self.encryption_mode = encryption_mode
                self.encryption_key = encryption_key
                self.mac_mode = mac_mode
                self.decrypt = True
            else:
                raise ViewStateException("Cannot decrypt without key or mac_mode")
        else:
            self.encryption_mode = None
            self.encryption_key = None
            self.mac_mode = None
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
        FORMAT_MARKER = b"\xff"
        VERSION_MARKER = b"\x01"
        PREAMBLE = FORMAT_MARKER + VERSION_MARKER

        try:
            return self.preamble == PREAMBLE
        except AttributeError:
            return False

    def decode(self):
        if self.decrypt:
            if self.mac_mode == MAC.HMACMD5:
                hashlen = 16
            elif self.mac_mode == MAC.HMACSHA1:
                hashlen = 20
            elif self.mac_mode == MAC.HMACSHA256:
                hashlen = 32
            elif self.mac_mode == MAC.HMACSHA384:
                hashlen = 48
            elif self.mac_mode == MAC.HMACSHA512:
                hashlen = 64

            if self.encryption_mode == Encryption.DES:
                decryptor = DES.new(self.encryption_key, DES.MODE_CBC, bytearray(8))
                blockpadlen = 8
            elif self.encryption_mode == Encryption.DES3:
                decryptor = DES3.new(self.encryption_key, DES3.MODE_CBC, bytearray(8))
                blockpadlen = 24
            elif self.encryption_mode == Encryption.AES:
                decryptor = AES.new(self.encryption_key, AES.MODE_CBC, bytearray(16))
                blockpadlen = 32

            self.signature = self.raw[-hashlen:]
            self.mac = self.mac_mode.value
            decrypted = decryptor.decrypt(self.raw[:-hashlen])
            self.raw = decrypted[blockpadlen:]

            if not self.is_valid():
                raise ViewStateException('Cannot decode invalid viewstate, bad preamble')

            self.decoded, self.remainder = Parser.parse(self.body)
        else:
            if not self.is_valid():
                raise ViewStateException('Cannot decode invalid viewstate, bad preamble')

            self.decoded, self.remainder = Parser.parse(self.body)

            if self.remainder:
                if len(self.remainder) == 20:
                    self.mac = 'hmac_sha1'
                elif len(self.remainder) == 32:
                    self.mac = 'hmac_sha256'
                else:
                    self.mac = 'unknown'
                self.signature = self.remainder

        return self.decoded
