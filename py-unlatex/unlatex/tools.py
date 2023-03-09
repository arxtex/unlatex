import codecs
import os
import re
import subprocess

# TODO: Define class Texjobspec.
# TODO: Provide a method run().
# TODO: Add new dir parameter SPEC and RUN.
# TODO: (IN, OUT, SPEC, RUN) constitute a completed Job.
# TODO: The quad of dirs can be arranged in various ways.
# TODO: (IN, OUT) is so to speak a test.
# TODO: (IN, SPEC) is something that can be run.
# TODO: (IN, SPEC, RUN, OUT) is a completed Job.

def runtex(*, progname, inputdir, outputdir, jobname, boot):
    """Return subprocess.Popen() that runs program with parameters.

    program -- the name of the tex or tex-like program to run
    inputdir -- path to directory containing tex source file
    outputdir -- path to directory into which outputs are to be written
    jobname -- the stem part of output filenames, sets \jobname
    boot -- tex macros to boot typesetting, eg r'\input story.tex \bye'

    The boot parameter gives great flexibility. Use the jobname to
    distinguish diffent runs of the same input file.

    # TODO: Clean up this example of use.
    >>> from unlatex.tools import runtex
    >>> x = runtex(progname='tex', inputdir='.', outputdir='OUT', jobname='mystory', boot=r'\input story \bye')
    >>> This is TeX, Version 3.141592653 (TeX Live 2022) (preloaded format=tex)

    >>> x.wait()
    0

    """

    texenv = dict(
        PATH = os.environ['PATH'],
        TEXINPUT = f'{inputdir}',
    )

    texargs = [
        f'{progname}',
        # These parameters in alphabetic order.
        # TODO: Allow other parameters to be set?
        '--halt-on-error',
        '--interaction=batchmode',
        f'--jobname={jobname}',
        f'--output-directory={outputdir}',
        '--recorder',
        # Final unnamed parameter.
        f'{boot}',
    ]

    return subprocess.Popen(args=texargs, env=texenv)





class LogfileReader:
    '''Lines in logfile, errors replaced, as an iterable.

    Replaces non-Unicode bytes by official REPLACEMENT CHARACTER, and
    trims trailing white space (as TeX does on input).

    >>> filename = 'TMP/OUT/boxlog_sample2e.log'
    >>> reader = LogfileReader(filename)
    >>> lines = list(reader)
    >>> lines[0]
    'This is pdfTeX, Version 3.141592653- ...'
    >>> lines[-1]
    'Output written on TMP/OUT/boxlog_sample2e.dvi (3 pages, 7576 bytes).'
    '''

    # https://docs.python.org/3/library/stdtypes.html#bytes.decode
    # https://docs.python.org/3/library/codecs.html#error-handlers
    # https://docs.python.org/3/library/codecs.html#codecs.replace_errors
    # TODO: Perhaps an iterator, not iterable, should be returned.

    def __init__(self, filename):

        self.filename = filename
        self.file = open(filename, 'rb')

    def __iter__(self):

        for input_line in self.file:

            output_line = input_line.decode(errors='replace').rstrip()
            yield output_line


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
        self.lines = lines

    def __iter__(self):

        # TODO: No trailing white space? Replace by filter?
        for line in self.lines:
            if line:
                yield line
            else:
                break
