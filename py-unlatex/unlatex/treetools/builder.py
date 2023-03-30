'''


Self-test: /py-unlatex$ python3 -m unlatex.treetools.builder
[0, [1, 2, [3], 4], 5, 6, 7, {'a': 1, 'b': 2}, 8]
[0, [1, 2, [3], 4], 5, 6, 7, {'a': 1, 'b': 2}, 8]

'''

# Resources consulted.
# https://en.wikipedia.org/wiki/Tree_(data_structure)
# https://github.com/urwid/urwid/blob/master/urwid/treetools.py
# https://www.google.com/search?q=python+treetools
# https://www.google.com/search?q=Grasshopper+data+trees
# https://www.google.com/search?q=serialize+data+tree

# 2011/python-jfine/jfine/treetools.py
# https://peps.python.org/pep-0479/
# https://stackoverflow.com/questions/37707187/python-pep479-change-stopiteration-handling-inside-generators


# I've probably moved on since 2011, so I will reinvent and then
# perhaps compare.

# Mostly, our trees will consist of leaf nodes (passed on AS_IS), so I
# will use sentinels for other behaviour. For Python sentinels see
# https://peps.python.org/pep-0661/

# Non-sentinel values in the stream are passed straight though. Other
# sentinel values affect the subsequent parsing of the stream. The
# most common sentinel value is likely to represent StopIteration.

# As we wish to detect and switch quickly on the sentinel, let's use
# an Enum. This will work fine so long as the 'sentinel' Enums do not
# appear as data. (If they do, perhaps an escaping mechanism can be
# used.)

# Perhaps enum.py has more code than we need, and also missing code
# that we need. Let's not worry too much about that for
# now. Certainly, we wish to be aligned with the good thinking that
# underlies enum.py.

# Let's stick to low-level and use ints, but with names.

from .symbol import symbol_factory

# Create some symbols.
keys = ('END', 'dict', 'list')

AAA = symbol_factory(name='AAA', keytype=str, keys=keys)

RAISE = AAA('END')
LIST = AAA('list')
DICT = AAA('dict')

# This explains how DICT works.
'''
>>> data = 'abcdef'
>>> idata = iter(data)
>>> dict(zip(idata, idata))
{'a': 'b', 'c': 'd', 'e': 'f'}
'''

def call_raise(exception, *_):
    raise exception

def dict_like(action, items):
    # TODO: Error if RAISE after odd number of items?
    return action(zip(items, items))

def list_like(action, items):
    return action(items)


lookup = (
    (call_raise, StopIteration),
    (dict_like, dict),
    (list_like, list),
)


class Builder:

    def __init__(self, items):

        self.items = iter(items)

    def __iter__(self):
        return self

    def __next__(self):

        # Look at the next item.
        curr = next(self.items)

        if type(curr) is AAA:
            # Process the symbols.
            fn, param = lookup[curr]
            return fn(param, self)
        else:
            # Pass through rest unchanged.
            return curr


if __name__ == '__main__':

    # This is the pretty way to see the semantics.
    items = [
        0,
        LIST,
          1, 2,
          LIST,
            3,
          RAISE,
          4,
        RAISE,
        5, 6, 7,
        DICT,
          'a', 1, 'b', 2,
        RAISE,
        8
    ]
    expected = [0, [1, 2, [3], 4], 5, 6, 7, {'a': 1, 'b': 2}, 8]

    builder = Builder(items)
    done = list(builder)
    print(expected)
    print(done)
