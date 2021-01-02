def hexify(b: bytes, sep: str = ':'):
    return sep.join('{:02x}'.format(i) for i in b)
