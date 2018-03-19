import pprint
import sys

from .viewstate import ViewState

def main():
    s = sys.stdin.read()
    vs = ViewState(s)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(vs.decode())

if __name__ == '__main__':
    main()
