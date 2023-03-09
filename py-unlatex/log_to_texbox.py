'''From TeX log file extract and write its page texbox's.
Useage: $ python log_to_tbox.py path/to/stem.log

Input: path/to/stem.log
Output: path/to/stem.page.1.tbx etc.

'''

from unlatex.tools import LogfileReader
from unlatex.tools import iterboxes


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
