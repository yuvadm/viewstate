import pytest

from viewstate import *


class TestViewState(object):

    def test_blank(self):
        vs = ViewState()
        assert not vs.is_valid()

    def test_is_valid(self):
        with open('tests/samples/ngcs.sample', 'r') as f:
            vs = ViewState(f.read())
            assert vs.is_valid() is True

    def test_invalid_decode(self):
        with pytest.raises(ViewStateException):
            vs = ViewState()
            vs.raw = b'\x01\x02'
            vs.decode()

    def test_parse_const_value(self):
        vs = ViewState()
        vs.raw = b'\xff\x01\x67'
        assert vs.decode() is True

