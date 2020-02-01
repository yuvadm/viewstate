import pprint
import sys

from .viewstate import ViewState


def main(raw=False):
    if raw:
        s = sys.stdin.buffer.read()
        vs = ViewState(raw=s)
    else:
        s = sys.stdin.read()
        vs = ViewState(s)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(vs.decode())


if __name__ == "__main__":
    raw = len(sys.argv) > 1 and sys.argv[1] == "-r"
    main(raw)
