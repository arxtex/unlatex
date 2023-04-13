'''
Usage: py-unlatex$ python3 -i texhour_2023_04_13.py 

>>> str(box)[:80]
'Vbox((Hbox((Special(),)), Glue(), Vbox((Vbox((Glue(), Hbox((Hbox(()),)))), Glue('

>>> str(box)[240:320]
"e())), Penalty(), ('OT1/cmr/m/n/17.28', ' A'), ('OT1/cmr/m/n/17.28', ' n'), Glue"

'''

from unlatex.lextools import lex_lines
from itertools import repeat


def doit(process, items):

    prev_depth = 0

    for item in items:

        depth, command = item
        delta = prev_depth - depth

        # Supply END symbols implied by delta.
        if delta < 0:
            raise ValueError
        yield from repeat('END', delta)

        # Use BEGIN as signal, that next item has body.
        head, bodied = process(command)
        bodied = bool(bodied)
        if bodied:
            yield 'BEGIN'

        yield head
        prev_depth = depth + bodied

    yield from repeat('END', prev_depth)


# LEAF, HEAD and BODY builder.
def build(items):

    stream = iter(items)

    def iter_nodes():

        for item in stream:
            if item == 'BEGIN':
                head = next(stream)
                yield head(iter_nodes())
            elif item == 'END':
                return
            else:
                yield item

    nodes = iter_nodes()
    return nodes



    

    # Create template for texbox files
#    template = f'{stem}.page.{{boxid}}.tbx'.format

if True:
    
        class Hbox(tuple):

            def partial(ht=0, wd=0, dp=0):

                def fn(body):
                    aaa = Hbox(body)
                    aaa.ht = ht
                    aaa.wd = wd
                    aaa.dp = dp

                    return aaa

                return fn

            def __repr__(self):

                return f'Hbox({tuple.__repr__(self)})'

        class Vbox(tuple):

            def partial(ht=0, wd=0, dp=0):

                def fn(body):
                    aaa = Vbox(body)
                    aaa.ht = ht
                    aaa.wd = wd
                    aaa.dp = dp

                    return aaa

                return fn

            def __repr__(self):

                return f'Vbox({tuple.__repr__(self)})'

        class Disc(tuple):

            def partial(ht=0, wd=0, dp=0):

                def fn(body):
                    aaa = Vbox(body)
                    aaa.ht = ht
                    aaa.wd = wd
                    aaa.dp = dp

                    return aaa

                return fn

            def __repr__(self):

                return f'Disc({tuple.__repr__(self)})'


        class Glue:
            def __repr__(self):
                return 'Glue()'

        class Kern:
            def __repr__(self):
                return 'Kern()'            

        class Penalty:
            def __repr__(self):
                return 'Penalty()'

        class Special:
            def __repr__(self):
                return 'Special()'

        class Write:
            def __repr__(self):
                return 'Write()'

        simple_commands = dict(
            glue = Glue,
            kern = Kern,
            penalty = Penalty,
            special = Special,
            write = Write,
            )

        def llex_lines(lines):

            lines = iter(lines)

            n = 0
            for dots, key, args in lex_lines(lines):
                yield len(dots), (key, args)
                n += 1
                if n >= 50:
                    break

        def lookup(command):
            key, args = command
            if key in set(('hbox', 'vbox', 'discretionary')):

                if key == 'hbox':
                    command = Hbox.partial()
                elif key == 'vbox':
                    command = Vbox.partial()
                elif key == 'discretionary':
                    command = Disc.partial()
                return command, 1
            
            else:

                cls = simple_commands.get(key)
                if cls is None:
                    return command, 0
                else:
                    return cls(), 0

if __name__ == '__main__':


    tbx_filename = '../examples/lamport-example/tbx/lamport-example.page.1.tbx'

    with open(tbx_filename) as f:

        lines =  map(str.rstrip, f)
        items = lex_lines(lines)
        stream = doit(lookup, llex_lines(lines))
        
        box = next(build(stream))
