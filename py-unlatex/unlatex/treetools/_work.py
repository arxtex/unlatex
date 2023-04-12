'''Temporary working file.

To be revised after experience using the tools in this file.

See py-unlatex/sample.py for example of its use.

'''


# Sorted tuple of distinct strings.


from bisect import bisect_left

class Keys(tuple):

    def __new__(cls, items):

        items = tuple(items)
        if not items:
            raise ValueError

        for curr in items:
            if type(curr) is not str:
                raise TypeError

        prev = items[0]
        for curr in items[1:]:
            if not prev < curr:
                raise ValueError
            prev = curr

        return tuple.__new__(cls, items)


    def index(self, key):
        'Return symbol given by key, else raise KeyError.'
        i = bisect_left(self, key)
        if i != len(self) and self[i] == key:
            return i
        else:
            raise KeyError(key)


    def __repr__(self):

        return f'{type(self).__name__}({tuple.__repr__(self)})'


def symbol_factory(name, keys):
    '''Return symbol_class for new collection of symbols.
    '''

    if type(keys) is not Keys:
        raise TypeError(keys)

    symbol_class = type(name, (int,), dict(__slots__ = ()))
    symbols = tuple(symbol_class(i) for i in range(len(keys)))

    symbol_class.symbols = symbols
    symbol_class.keys = keys

    def index(cls, key):

        i = cls.keys.index(key)
        return cls.symbols[i]


    def __repr__(self):

        i = int(self)
        key = self.keys[i]
        return f'<{type(self).__name__}.{key}: {i}>'


    def __new__(cls, *argv, **kwargs):

        msg = 'Use index to get existing elements - read-only class'
        raise NotImplementedError(msg)


    # TODO: Use a mixin, to simplify code.
    symbol_class.__repr__ = __repr__
    symbol_class.index = classmethod(index)
    symbol_class.__new__ = __new__

    return symbol_class


class MissingEnd(Exception):
    pass


# TODO: Provide a structure that combines lookup and END?
def iter_nodes(lookup, end_symbol, source):
    '''Return generator that yields nodes, built from source.

    Uses lookup to construct the nodes. Uses end_symbol to determine
    control symbols.
    '''

    # Ensure we use an iterator. Iterable is not enough.
    source = iter(source)

    # Manage the recursion, via dispatch.
    symbol_type = type(end_symbol) # Place in closure.
    def local_iter_nodes():
        '''Yield nodes from source until end_symbol.

        '''

        for curr in source:

            if curr is end_symbol:
                return

            elif type(curr) == symbol_type:
                yield dispatch[curr]()

            else:
                yield curr

        raise MissingEnd

    # Can now define local dispatch, which provides recursion.
    dispatch = lookup(end_symbol, local_iter_nodes)

    # Create and return a local iterator over the nodes.
    nodes = local_iter_nodes()
    return nodes


# Build / Assemble larger objects from stream of leaf nodes and
# control symbols.

class Build:

    # TODO: __repr__ for instances.

    def __init__(self, lookup, end_symbol):

        self.lookup = lookup
        self.end_symbol = end_symbol
        self.Symbol = type(end_symbol)

    def __call__(self, source):

        return iter_nodes(self.lookup, self.end_symbol, source)

    # TODO: fn is the lookup factory.
    @classmethod
    def from_function(cls, fn):
        '''Create a Build object from a suitable function.

        Designed to be used as a decorator.
        '''

        _END = '_END'
        end_name = '_END'

        # Compute keys, to pass to symbol_factory.
        fn_keys = fn(None).keys()
        # TODO: Wasted time because wrote 'doit_' for 'do_'.
        prefix = 'do_'
        do_keys = set(filter_strip_prefix('do_', fn_keys))
        if _END in do_keys:
            raise ValueError(f"Found {_END!r}' in f{do_keys}")
        do_keys.add(_END)
        keys = Keys(sorted(do_keys))


        # Create symbols.
        Symbol = symbol_factory(name='AAA', keys=keys)
        end_symbol = Symbol.index(_END)

        # Copied from work4.py.
        # TODO: Create symbol set from the 'closure function'?
        # TODO: What are the good ways to use these tools?
        def lookup_factory(aaa):

            def lookup(END, iter_nodes):

                # Typical way to get the name of a symbol.
                # TODO: Check all todo_ names are known.
                end_name = _END
                mapping = fn(iter_nodes)

                return tuple(
                    None if key == end_name
                    else mapping['do_' + key]
                    for key in end_symbol.keys
                )

            return lookup

        return cls(lookup_factory(fn), end_symbol)


# Helper function.
def filter_strip_prefix(prefix, source):
    '''
    '''
    for item in source:
        if item.startswith(prefix):
            yield item[len(prefix):]
