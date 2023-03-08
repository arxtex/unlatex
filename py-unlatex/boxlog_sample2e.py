'''From Lamport's small guide create log file with texboxes

The main points in this example are:
* The use of `unlatex.tools.runtex()`.
* The boot parameter can input two (or more) files.
* We can control the outdir and the jobname.
* Use of sys.argv to use name of script as jobname.

This script assumes that the directory 'TMP/OUT' exists, relative to
the current directory. It also assumes that the unlatex package is on
the Python path.

Typical output is:

$ python3 boxlog_sample2e.py 
This is pdfTeX, Version 3.141592653-2.6-1.40.24 (TeX Live 2022) (preloaded format=latex)
 restricted \write18 enabled.
entering extended mode
<Popen: returncode: 0 args: ['latex', '--halt-on-error', '--interaction=batc...>

'''

from unlatex.tools import runtex

if __name__ == '__main__':

    # Determine the stem part of the script name.
    import sys
    import os.path

    scriptname = sys.argv[0]
    base = os.path.basename(scriptname)
    stem = os.path.splitext(base)[0]

    # The script fails if this directory does not exist.
    # TODO: More elegant failure?
    outdir = 'TMP/OUT'

    x = runtex(
        progname='latex',
        inputdir='',
        outputdir=outdir,
        jobname=stem,
        boot=r'\input ./misc/latex-preamble.sty \input sample2e'
    )

    x.wait()
    print(x)
