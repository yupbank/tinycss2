from __future__ import unicode_literals


def serialize(nodes):
    """Serialize an iterable of nodes to CSS syntax
    and return an Unicode string.

    """
    chuncks = []
    _serialize_to(nodes, chuncks.append)
    return ''.join(chuncks)


def serialize_identifier(value):
    if value == '-':
        return r'\-'

    if value[0] == '-':
        result = '-'
        value = value[1:]
    else:
        result = ''
    c = value[0]
    result += (
        c  if c in ('abcdefghijklmnopqrstuvwxyz_'
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ') or ord(c) > 0x7F else
        r'\A ' if c == '\n' else
        r'\D ' if c == '\r' else
        r'\C ' if c == '\f' else
        '\\%X ' % ord(c) if c in '0123456789' else
        '\\' + c
    )
    result += serialize_name(value[1:])
    return result


def serialize_name(value):
    return ''.join(
        c  if c in ('abcdefghijklmnopqrstuvwxyz-_0123456789'
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ') or ord(c) > 0x7F else
        r'\A ' if c == '\n' else
        r'\D ' if c == '\r' else
        r'\C ' if c == '\f' else
        '\\' + c
        for c in value
    )


def serialize_string_value(value):
    return ''.join(
        r'\"' if c == '"' else
        r'\\' if c == '\\' else
        r'\A ' if c == '\n' else
        r'\D ' if c == '\r' else
        r'\C ' if c == '\f' else
        c
        for c in value
    )


# http://dev.w3.org/csswg/css-syntax/#serialization-tables
def _serialize_to(nodes, write):
    """Serialize an iterable of nodes to CSS syntax,
    writing chuncks as Unicode string
    by calling the provided :obj:`write` callback.

    """
    bad_pairs = BAD_PAIRS
    previous_type = None
    for node in nodes:
        serialization_type = node.type if node.type != 'literal' else node.value
        if (previous_type, serialization_type) in bad_pairs:
            write('/**/')
        if previous_type == '\\':
            write('\n')
            if serialization_type != 'whitespace':
                node._serialize_to(write)
        else:
            node._serialize_to(write)
        previous_type = serialization_type


BAD_PAIRS = set(
    [(a, b) for a in ('ident', 'at-keyword', 'hash', 'dimension', '#', '-',
                      'number')
            for b in ('ident', 'function', 'url', 'number', 'percentage',
                      'dimension', 'unicode-range')] +
    [(a, b) for a in ('ident', 'at-keyword', 'hash', 'dimension')
            for b in ('-', '-->')] +
    [(a, b) for a in ('#', '-', 'number', '@')
            for b in ('ident', 'function', 'url')] +
    [(a, b) for a in ('unicode-range', '.', '+')
            for b in ('number', 'percentage', 'dimension')] +
    [('@', b) for b in ('ident', 'function', 'url', 'unicode-range', '-')] +
    [('unicode-range', b) for b in ('ident', 'function', '?')] +
    [(a, '=') for a in '$*^~|'] +
    [('ident', '() block'), ('|', '|'), ('/', '*')]
)