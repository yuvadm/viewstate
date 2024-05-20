import pytest

from datetime import datetime
from os import walk
from os.path import join
from viewstate import ViewState, ViewStateException


class TestParse(object):
    def test_const_value(self):
        vs = ViewState(raw=b"\xff\x01\x67")
        assert vs.decode() is True

    def test_int_value(self):
        vs = ViewState(raw=b"\xff\x01\x02\x88\x01")
        assert vs.decode() == 136

    def test_string_value(self):
        s = "abcdefghij"
        vs = ViewState(raw=b"\xff\x01\x05" + bytes([len(s)]) + s.encode())
        assert vs.decode() == s

    def test_simple_dict(self):
        vs = ViewState(raw=b"\xff\x01\x18\x02\x05\x01a\x05\x01b\x05\x01c\x05\x01d")
        assert vs.decode() == {"a": "b", "c": "d"}

    def test_simple_list(self):
        vs = ViewState(
            raw=b"\xff\x01\x16\x05\x05\x01a\x05\x01b\x05\x01c\x05\x01d\x05\x01e"
        )
        assert vs.decode() == ["a", "b", "c", "d", "e"]

    def test_simple_pair(self):
        vs = ViewState(raw=b"\xff\x01\x0f\x67\x68")
        assert vs.decode() == (True, False)

    def test_simple_triplet(self):
        vs = ViewState(raw=b"\xff\x01\x10\x67\x68\x67")
        assert vs.decode() == (True, False, True)

    def test_color(self):
        vs = ViewState(raw=b"\xff\x01\n\x91")
        assert vs.decode() == "Color: Salmon"

        vs = ViewState(raw=b"\xff\x01\n\x8d\x01")
        assert vs.decode() == "Color: Red"

        vs = ViewState(raw=b"\xff\x01\n\xff")
        assert vs.decode() == "Color: Unknown"

    def test_rgba(self):
        vs = ViewState(raw=b"\xff\x01\x09\x10\x20\x30\x40")
        assert vs.decode() == "RGBA(16,32,48,64)"

    def test_formatted_string(self):
        vs = ViewState()
        s1 = "System.Int64, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089"
        s2 = "6111733106"
        vs.raw = (
            b"\xff\x01()"
            + bytes([len(s1)])
            + s1.encode()
            + bytes([len(s2)])
            + s2.encode()
        )
        assert vs.decode() == "Formatted string: {} type ref {}".format(s2, s1)

    @pytest.mark.skip(reason="Datetime parsing not yet supported")
    def test_datetime(self):
        vs = ViewState()
        vs.raw = b"\xff\x01\x06\x000Po\x9b\x87\xd5\x88"
        assert vs.decode() == datetime(2018, 3, 11, 22)
        vs.raw = b"\xff\x01\x06\x00\xf0\xb9\x99d\x88\xd5\x88"
        assert vs.decode() == datetime(2018, 3, 12, 22)

    def test_complex_pair(self):
        vs = ViewState()
        vs.raw = b"\xff\x01\x0f\x67\x0f\x68\x66"
        assert vs.decode() == (True, (False, 0))
        vs.raw = b"\xff\x01\x0f\x0f\x67\x68\x66"
        assert vs.decode() == ((True, False), 0)
        vs.raw = b"\xff\x01\x0f\x0f\x67\x05\x061q2w3e\x66"
        assert vs.decode() == ((True, "1q2w3e"), 0)

    def test_parse_unknown(self):
        with pytest.raises(ViewStateException):
            vs = ViewState(raw=b"\xff\x01\x99\x99\x99")
            assert vs.decode()

    def test_parse_samples(self):
        for root, dirs, files in walk("tests/samples"):
            for f in files:
                with open(join(root, f), "r") as t:
                    vs = ViewState(t.read())
                    _ = vs.decode()
