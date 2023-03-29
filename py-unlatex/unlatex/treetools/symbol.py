'''Support symbol classes, for building and serialization.
'''

def iterpairs(items):
    '''Iterate over items, yielding the (prev, curr) pairs.

    >>> list(iterpairs(''))
    []
    >>> list(iterpairs('a'))
    []
    >>> list(iterpairs('abc'))
    [('a', 'b'), ('b', 'c')]
    '''

    iteritems = iter(items)

    # Avoid: RuntimeError: generator raised StopIteration
    try:
        prev = next(iteritems)
    except StopIteration:
        return

    for curr in iteritems:
        yield (prev, curr)
        prev = curr


def assert_symbolnames(itemtype, items):
    '''If items not ascending tuple of itemtype raise ValueError.

    Otherwise, all is OK and returns None.

    # TODO: Further examples.
    >>> assert_symbolnames(bytes, ('aaa',))
    Traceback (most recent call last):
    ValueError: type('aaa') != <class 'bytes'>
    '''

    if type(items) != tuple:
        raise ValueError

    for item in items:
        if type(item) != itemtype:
            raise ValueError(f'type({item!r}) != {itemtype}')

    for prev, curr in iterpairs(items):
        if not prev < curr:
            raise ValueError(f'{prev!r} < {curr!r} not True')

    return None


# Based on:
# https://docs.python.org/3/library/bisect.html
from bisect import bisect_left
def index(a, key):
    'Return index at which key is found, else raise KeyError.'
    i = bisect_left(a, key)
    if i != len(a) and a[i] == key:
        return i
    raise KeyError(f'Symbol {key!r} not in {a}')


# TODO: Make naming work better.
# TODO: Use decorator so usage similar to class definition?
def symbol_factory(*, name, keytype, keys):

    # Check that we're good to go.
    assert_symbolnames(keytype, keys)

    # TODO: Make Symbol.keys a property of the class? Requires
    # metaclass.
    # TODO: Provide a docstring, maybe via deco class definition.

    class Symbol(int):

        def __new__(Symbol, key):

            if type(key) != keytype:
                raise TypeError(f'key must be {keytype}, not {type(key)}')

            i = index(keys, key)
            return symbols[i]

        def __repr__(self):

            i = int(self)       # Avoids recursion.
            key = keys[i]
            return f'<{name}.{key}: {i}>'

    n = len(keys)
    symbols = tuple(int.__new__(Symbol, i) for i in range(n))

    Symbol.keys = keys          # For convenience only.

    return Symbol
