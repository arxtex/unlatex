'''From TeX log file extract and write its page texbox's.
Useage: $ python log_to_tbox.py path/to/stem.log

Input: path/to/stem.log
Output: path/to/stem.page.1.tbx etc.

'''

import re
from unlatex.tools import LogfileReader

# TODO: It seems TeX puts blank line before and after box contents.
# Completed box being shipped out [1]

# TODO: What about detecting / insisting no trailing white space.
# TODO: What about finding and using \showbox log output.
# TODO: Systematic use of iterators to process box contents.
# TODO: Documents tbox filename extension.

# TODO: Document and deal with:
# >>> x = open(filename)
# >>> y = x.read()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/usr/lib/python3.10/codecs.py", line 322, in decode
#     (result, consumed) = self._buffer_decode(data, self.errors, final)
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0x88 in position 106273: invalid start byte

# Python docs recommend using raw string notation.
# https://docs.python.org/3/library/re.html


# TODO: Provide checking of pagenums.
AAA = r'Completed box being shipped out '
BBB = r'\[(?P<pagenums>[-0-9.]+)\]'
shipout_pattern = re.compile(AAA + BBB)
def getpagenums(line):

    # TODO: Trailing white space? Use pattern.fullmatch?
    mo = shipout_pattern.match(line)
    if mo:
        return mo['pagenums']

def iterboxes(lines):

    for line in lines:

        # if line.startswith('Completed box being shipped out '):
        pagenums = getpagenums(line)
        if pagenums:
            yield Box(pagenums, lines)

class Box:

    # We assumes that lines is Unicode strings with trailing white
    # space trimmed.

    def __init__(self, pagenums, lines):

        self.pagenums = pagenums

    def __iter__(self):

        # TODO: No trailing white space? Replace by filter?
        for line in lines:
            if line:
                yield line
            else:
                break


if __name__ == '__main__':

    import sys
    filename = sys.argv[1]

    if not filename.endswith('.log'):
        raise ValueError(filename)

    filestem = filename[:-len('.log')]    

    lines = LogfileReader(filename)
    # Strips trailing white space.
    lines = map(str.rstrip, lines)

    boxes = iterboxes(lines)
    for box in boxes:
        print(f'Got box {box.pagenums}')
        with open(f'{filestem}.page.{box.pagenums}.tbx', 'w') as f:
            for command in box:
                f.write(command + '\n')
