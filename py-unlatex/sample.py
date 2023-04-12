from unlatex.treetools import Build

# TODO: Move to separate file.
# A decorator that creates an instance of a class.
@Build.from_function
def basic_build(iter_nodes):

    # Basically, one entry for each type / constructor.
    def do_list():
        return list(iter_nodes())

    def do_tuple():
        return tuple(iter_nodes())

    def do_dict():
        tmp = iter_nodes()
        return dict(zip(tmp, tmp))

    return locals()


if True:

    END = basic_build.end_symbol
    DICT = basic_build.Symbol.index('dict')
    LIST = basic_build.Symbol.index('list')
    TUPLE = basic_build.Symbol.index('tuple')


    nodes = basic_build([
        'a',
        LIST,
          1, 2, 3,
          DICT, 'a', 1, 'b', 2, END,
        END,
        1,
        2,
    END
    ])



    aaa = list(nodes)
    print(aaa)
