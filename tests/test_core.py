import pytest

from viewstate import ViewState


class TestViewState(object):

    def test_blank(self):
        vs = ViewState()
        assert not vs.is_valid()

    @pytest.mark.skip(reason='Missing test data')
    def test_is_valid(self):
        with open('samples/ngcs.sample', 'r') as f:
            vs = ViewState(f.read())
            self.assertTrue(vs.is_valid())

    def test_invalid_decode(self):
        with pytest.raises(Exception):
            vs = ViewState()
            vs.raw = b'\x01\x02'
            vs.decode()

    def test_parse_const_value(self):
        vs = ViewState()
        vs.raw = b'\xff\x01\x67'
        assert vs.decode() is True

