from datetime import datetime

from .colors import COLORS
from .exceptions import ViewStateException


class ParserMeta(type):
    """
    Parser metaclass is used to register each of the parser subclasses `marker` field
    This field is used to dynamically select the right class for parsing a given byte array
    """

    def __init__(cls, name, bases, namespace):
        super(ParserMeta, cls).__init__(name, bases, namespace)
        if not hasattr(cls, "registry"):
            cls.registry = {}
        if hasattr(cls, "marker"):
            marker = getattr(cls, "marker")
            if type(marker) not in (tuple, list):
                marker = [marker]
            for m in marker:
                cls.registry[m] = cls


class Parser(metaclass=ParserMeta):
    """
    Main parser class delegates parsing according to current byte marker
    Performs lookup on metaclass registry
    """

    @staticmethod
    def parse(b):
        marker, remain = b[0], b[1:]
        try:
            return Parser.registry[marker].parse(remain)
        except KeyError:
            raise ViewStateException("Unknown marker {}".format(marker))


class Const(Parser):
    @classmethod
    def parse(cls, remain):
        return cls.const, remain


class Noop(Parser):
    marker = 0x01

    @staticmethod
    def parse(b):
        return None, b


class NoneConst(Const):
    marker = 0x64
    const = None


class EmptyConst(Const):
    marker = 0x65
    const = ""


class ZeroConst(Const):
    marker = 0x66
    const = 0


class TrueConst(Const):
    marker = 0x67
    const = True


class FalseConst(Const):
    marker = 0x68
    const = False


class Integer(Parser):
    marker = (0x02, 0x2B)

    @staticmethod
    def parse(b):
        n = 0
        bits = 0
        i = 0
        while bits < 32:
            tmp = b[i]
            i += 1
            n |= (tmp & 0x7F) << bits
            if not (tmp & 0x80):
                return n, b[i:]
            bits += 7
        return n, b[i:]  # overflow


class String(Parser):
    marker = (0x05, 0x1E, 0x2A, 0x29)

    @staticmethod
    def parse(b):
        n = b[0]
        n, remain = Integer.parse(b)
        s = remain[:n]
        return s.decode(), remain[n:]


class Enum(Parser):
    marker = 0x0B

    @staticmethod
    def parse(b):
        enum, remain = Parser.parse(b)
        val, remain = Integer.parse(remain)  # unsure about this part
        final = "Enum: {}, val: {}".format(enum, val)
        return final, remain


class Color(Parser):
    marker = 0x0A

    @staticmethod
    def parse(b):
        try:
            color = COLORS[b[0]]
        except IndexError:
            color = "Unknown"
        return "Color: {}".format(color), b[1:]


class Pair(Parser):
    marker = 0x0F

    @staticmethod
    def parse(b):
        first, remain = Parser.parse(b)
        second, remain = Parser.parse(remain)
        return (first, second), remain


class Triplet(Parser):
    marker = 0x10

    @staticmethod
    def parse(b):
        first, remain = Parser.parse(b)
        second, remain = Parser.parse(remain)
        third, remain = Parser.parse(remain)
        return (first, second, third), remain


class Datetime(Parser):
    marker = 0x06

    @staticmethod
    def parse(b):
        # print([x for x in b[:8]])
        return datetime(2000, 1, 1), b[8:]


class Unit(Parser):
    marker = 0x1B

    @staticmethod
    def parse(b):
        # print([x for x in b[:12]])
        return "Unit: ", b[12:]


class RGBA(Parser):
    marker = 0x09

    @staticmethod
    def parse(b):
        return "RGBA({},{},{},{})".format(*b[:4]), b[4:]


class StringArray(Parser):
    marker = 0x15

    @staticmethod
    def parse(b):
        n, remain = Integer.parse(b)
        l = []
        for _ in range(n):
            if not remain[0]:
                val, remain = "", remain[1:]
            else:
                val, remain = String.parse(remain)
            l.append(val)
        return l, remain


class Array(Parser):
    marker = 0x16

    @staticmethod
    def parse(b):
        n, remain = Integer.parse(b)
        l = []
        for _ in range(n):
            val, remain = Parser.parse(remain)
            l.append(val)
        return l, remain


class StringRef(Parser):
    marker = 0x1F

    @staticmethod
    def parse(b):
        val, remain = Integer.parse(b)
        return "Stringref #{}".format(val), remain


class FormattedString(Parser):
    marker = 0x28

    @staticmethod
    def parse(b):
        s1, remain = Parser.parse(b)
        s2, remain = String.parse(remain)
        return "Formatted string: {} type ref {}".format(s2, s1), remain


class SparseArray(Parser):
    marker = 0x3C

    @staticmethod
    def parse(b):
        type, remain = Parser.parse(b)
        length, remain = Integer.parse(remain)
        n, remain = Integer.parse(remain)
        l = [None] * length
        for _ in range(n):
            idx, remain = Integer.parse(remain)
            val, remain = Parser.parse(remain)
            l[idx] = val
        return l, remain


class Dict(Parser):
    marker = 0x18

    @staticmethod
    def parse(b):
        n = b[0]
        d = {}
        remain = b[1:]
        for _ in range(n):
            k, remain = Parser.parse(remain)
            v, remain = Parser.parse(remain)
            d[k] = v
        return d, remain


class TypedArray(Parser):
    marker = 0x14

    @staticmethod
    def parse(b):
        typeval, remain = Parser.parse(b)
        n, remain = Integer.parse(remain)
        l = []
        for _ in range(n):
            val, remain = Parser.parse(remain)
            l.append(val)
        return l, remain
