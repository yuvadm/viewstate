import unittest

from viewstate import ViewState

class TestViewState(unittest.TestCase):

    def test_is_valid(self):
        with open('samples/ngcs.sample', 'r') as f:
            vs = ViewState(f.read())
            self.assertTrue(vs.is_valid())

if __name__ == '__main__':
    unittest.main()
