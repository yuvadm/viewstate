from .exceptions import ViewStateException

CONSTS = {
    100: {},
    101: '',
    102: 0,
    103: True,
    104: False
}

def parse_const(b):
    return CONSTS.get(b, None)

def parse_string(b):
    n = b[0]
    s = b[1:n+1]
    return s.decode(), b[n+1:]

def parse_pair(b):
    first, remain = parse(b)
    second, remain = parse(remain)
    return (first, second), remain

def parse_array(b):
    n = b[0]
    l = []
    remain = b[1:]
    for _ in range(n):
        val, remain = parse(remain)
        l.append(val)
    return l, remain

def parse_dict(b):
    n = b[0]
    d = {}
    remain = b[1:]
    for _ in range(n):
        k, remain = parse(remain)
        v, remain = parse(remain)
        d[k] = v
    return d, remain

def parse(b):
    if not b:
        return None
    else:
        assert type(b) == bytes().__class__

    if 100 <= b[0] <= 104:
        return parse_const(b[0]), b[1:]
    elif b[0] == 0x5:
        return parse_string(b[1:])
    elif b[0] == 0xf:
        return parse_pair(b[1:])
    elif b[0] == 0x16:
        return parse_array(b[1:])
    elif b[0] == 0x18:
        return parse_dict(b[1:])
    else:
        raise ViewStateException('Unable to parse remainder of bytes {}'.format(b))
        return b, bytes()

