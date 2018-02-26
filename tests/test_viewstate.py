import pytest

from viewstate import *


class TestViewState(object):

    def test_blank(self):
        vs = ViewState()
        assert not vs.is_valid()

    def test_is_valid(self):
        for s in ['ngcs', 'mot', 'ecom']:
            with open('tests/samples/{}.sample'.format(s), 'r') as f:
                vs = ViewState(f.read())
                assert vs.is_valid() is True

    def test_invalid_base64(self):
        with pytest.raises(ViewStateException):
            vs = ViewState('hello')

    def test_invalid_decode(self):
        with pytest.raises(ViewStateException):
            vs = ViewState(raw=b'\x01\x02')
            vs.decode()
