import pytest

from os import walk
from os.path import join
from viewstate import ViewState, ViewStateException


class TestViewState(object):
    def test_blank(self):
        vs = ViewState()
        assert not vs.is_valid()

    def test_is_valid(self):
        for root, dirs, files in walk("tests/samples"):
            for f in files:
                with open(join(root, f), "r") as t:
                    vs = ViewState(t.read())
                    assert vs.is_valid() is True

    def test_invalid_base64(self):
        with pytest.raises(ViewStateException):
            ViewState("hello")

    def test_invalid_decode(self):
        with pytest.raises(ViewStateException):
            vs = ViewState(raw=b"\x01\x02")
            vs.decode()

    def test_no_signature(self):
        vs = ViewState(raw=b"\xff\x01e")
        vs.decode()
        assert vs.mac is None
        assert vs.signature is None

    def test_macs(self):
        MAC_LENGTHS = {
            "hmac_sha1": 20,
            "hmac_sha256": 32,
            "unknown": 5,  # could be any other value
        }

        for mac, n in MAC_LENGTHS.items():
            sig = b"\x55" * n  # not a real signature, just testing length
            vs = ViewState(raw=b"\xff\x01d" + sig)
            vs.decode()
            assert vs.mac == mac
            assert vs.signature == sig
