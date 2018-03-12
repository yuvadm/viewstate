import pytest

from os import walk
from os.path import join
from viewstate import *


class TestParse(object):

    def test_int_value(self):
        vs = ViewState(raw=b'\xff\x01\x02\x88\x01')
        assert vs.decode() == 136

    def test_const_value(self):
        vs = ViewState(raw=b'\xff\x01\x67')
        assert vs.decode() is True

    def test_string_value(self):
        s = 'abcdefghij'
        vs = ViewState(raw=b'\xff\x01\x05\x0a' + s.encode())
        assert vs.decode() == s

    def test_simple_dict(self):
        vs = ViewState(raw=b'\xff\x01\x18\x02\x05\x01a\x05\x01b\x05\x01c\x05\x01d')
        assert vs.decode() == {'a': 'b', 'c': 'd'}

    def test_simple_list(self):
        vs = ViewState(raw=b'\xff\x01\x16\x05\x05\x01a\x05\x01b\x05\x01c\x05\x01d\x05\x01e')
        assert vs.decode() == ['a', 'b', 'c', 'd', 'e']

    def test_simple_pair(self):
        vs = ViewState(raw=b'\xff\x01\x0f\x67\x68')
        assert vs.decode() == (True, False)

    def test_simple_triplet(self):
        vs = ViewState(raw=b'\xff\x01\x10\x67\x68\x67')
        assert vs.decode() == (True, False, True)

    def test_unknown_color(self):
        vs = ViewState(raw=b'\xff\x01\n\x01\x02')
        assert vs.decode() == 'Color: unknown'  # all colors are unknown for now

    def test_complex_pair(self):
        vs = ViewState()
        vs.raw = b'\xff\x01\x0f\x67\x0f\x68\x66'
        assert vs.decode() == (True, (False, 0))
        vs.raw = b'\xff\x01\x0f\x0f\x67\x68\x66'
        assert vs.decode() == ((True, False), 0)
        vs.raw = b'\xff\x01\x0f\x0f\x67\x05\x061q2w3e\x66'
        assert vs.decode() == ((True, '1q2w3e'), 0)

    def test_parse_unknown(self):
        with pytest.raises(ViewStateException):
            vs = ViewState(raw=b'\xff\x01\x99\x99\x99')
            assert vs.decode()

    def test_parse_samples(self):
        for root, dirs, files in walk('tests/samples'):
            for f in files:
                with open(join(root, f), 'r') as t:
                    vs = ViewState(t.read())
                    _ = vs.decode()

