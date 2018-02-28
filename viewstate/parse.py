from .exceptions import ViewStateException

CONSTS = {
    100: None,
    101: '',
    102: 0,
    103: True,
    104: False
}

def parse_const(b):
    return CONSTS.get(b, None)

def parse_int(b):
    n = 0
    bits = 0
    i = 0
    while (bits < 32):
        tmp = b[i]
        i += 1
        n |= (tmp & 0x7f) << bits
        if not (tmp & 0x80):
            return n, b[i:]
        bits += 7
    return n, b[i:]  # overflow

def parse_string(b):
    n = b[0]
    n, remain = parse_int(b)
    s = remain[:n]
    return s.decode(), remain[n:]

def parse_enum(b):
    if b[0] == 0x29:
        n, remain = parse_int(b[1:])
        for _ in range(n):
            return remain[:n], remain[n+1:]
    else:
        pass

def parse_pair(b):
    first, remain = parse(b)
    second, remain = parse(remain)
    return (first, second), remain

def parse_str_array(b):
    n, remain = parse_int(b)
    l = []
    for _ in range(n):
        if not remain[0]:
            val, remain = '', remain[1:]
        else:
            val, remain = parse_string(remain)
        l.append(val)
    return l, remain

def parse_array(b):
    n, remain = parse_int(b)
    l = []
    for _ in range(n):
        val, remain = parse(remain)
        l.append(val)
    return l, remain

def parse_stringref(b):
    val, remain = parse_int(b)
    return 'Stringref #{}'.format(val), remain

def parse_sparse_array(b):
    type, remain = parse_type(b)
    length, remain = parse_int(remain)
    n, remain = parse_int(remain)
    l = [None] * length
    for _ in range(n):
        idx, remain = parse_int(remain)
        val, remain = parse(remain)
        l[idx] = val
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

def parse_type(b):
    if b[0] in (0x29, 0x2a):
        return parse_string(b[1:])
    elif b[0] == 0x2b:
        return parse_int(b[1:])
    else:
        raise ViewStateException('Unknown type flag at {} bytes {}'.format(len(b), b[:20]))

def parse_typed_array(b):
    typeval, remain = parse_type(b)
    n, remain = parse_int(remain)
    l = []
    for _ in range(n):
        val, remain = parse(remain)
        l.append(val)
    return l, remain

def parse(b):
    if not b:
        return None
    else:
        assert type(b) == bytes().__class__

    if 100 <= b[0] <= 104:
        return parse_const(b[0]), b[1:]
    elif b[0] == 0x2:
        return parse_int(b[1:])
    elif b[0] in (0x5, 0x1e):
        return parse_string(b[1:])
    elif b[0] == 0xb:
        return parse_enum(b[1:])
    elif b[0] == 0xf:
        return parse_pair(b[1:])
    elif b[0] == 0x14:
        return parse_typed_array(b[1:])
    elif b[0] == 0x15:
        return parse_str_array(b[1:])
    elif b[0] == 0x16:
        return parse_array(b[1:])
    elif b[0] == 0x18:
        return parse_dict(b[1:])
    elif b[0] == 0x1f:
        return parse_stringref(b[1:])
    elif b[0] == 0x3c:
        return parse_sparse_array(b[1:])
    else:
        raise ViewStateException('Unable to parse remainder of {} bytes {}'.format(len(b), b[:20]))
        return b, bytes()

