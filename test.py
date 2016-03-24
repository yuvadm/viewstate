import unittest

from viewstate import ViewState

class TestViewState(unittest.TestCase):

    def test_blank(self):
        vs = ViewState()
        self.assertFalse(vs.is_valid())

    def test_is_valid(self):
        with open('samples/ngcs.sample', 'r') as f:
            vs = ViewState(f.read())
            self.assertTrue(vs.is_valid())

    # def test_invalid_decode(self):
    #     with self.assertRaises(Exception):
    #         vs = ViewState(b'\x01\x02', decoded=True)
    #         vs.decode()

    # def test_parse(self):
    #     vs = ViewState(b'\xff\x01\x67', decoded=True)
    #     assertTrue(vs.decode())

if __name__ == '__main__':
    unittest.main()
