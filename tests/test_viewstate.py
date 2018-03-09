import pytest

from os import walk
from os.path import join
from viewstate import *


class TestViewState(object):

    def test_blank(self):
        vs = ViewState()
        assert not vs.is_valid()

    def test_is_valid(self):
        for root, dirs, files in walk('tests/samples'):
            for f in files:
                with open(join(root, f), 'r') as t:
                    vs = ViewState(t.read())
                    assert vs.is_valid() is True

    def test_invalid_base64(self):
        with pytest.raises(ViewStateException):
            vs = ViewState('hello')

    def test_invalid_decode(self):
        with pytest.raises(ViewStateException):
            vs = ViewState(raw=b'\x01\x02')
            vs.decode()
