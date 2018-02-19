import sys

from .core import ViewState

def main():
    s = sys.stdin.read()
    vs = ViewState(s)
    print('Got: ' + s)
    print(vs.raw)
    print(vs.decode())

if __name__ == '__main__':
    main()
