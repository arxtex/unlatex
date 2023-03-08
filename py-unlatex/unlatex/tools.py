import os
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
