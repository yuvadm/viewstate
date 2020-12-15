import pprint
import sys
import argparse

from .viewstate import ViewState
from .keymodes import Encryption, MAC


def main(options):
    if options.raw:
        s = sys.stdin.buffer.read()
        vs = ViewState(raw=s, encryption_mode=options.encryption_mode, encryption_key=bytearray.fromhex(options.encryption_key), mac_mode=options.mac_mode)
    else:
        s = sys.stdin.read()
        vs = ViewState(s, encryption_mode=options.encryption_mode, encryption_key=bytearray.fromhex(options.encryption_key), mac_mode=options.mac_mode)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(vs.decode())

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-r", dest='raw', action='store_true', default=False, help="Raw mode")
    parser.add_argument("-e", dest='encryption_mode', action='store', type=Encryption, choices=list(Encryption), help="Encryption algorithm")
    parser.add_argument("-k", dest='encryption_key', action='store', help="Encryption key in hexadecimal")
    parser.add_argument("-m", dest='mac_mode', action='store', type=MAC, choices=list(MAC), help="MAC validation algorithm")
    return parser.parse_args(args)

if __name__ == "__main__":
    options = getOptions()
    main(options)
