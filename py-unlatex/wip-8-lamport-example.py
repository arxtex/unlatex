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

# TODO: Provide commands to set up and use standard dir layout.

# $ mkdir ../examples/lamport-example
# $ mkdir ../examples/lamport-example/src
# $ mkdir ../examples/lamport-example/run
# $ mkdir ../examples/lamport-example/tbx
# $ cp -iv $(kpsewhich sample2e.tex) ../examples/lamport-example/src
# '/usr/local/texlive/2022/texmf-dist/tex/latex/base/sample2e.tex' -> '../examples/lamport-example/src'

from unlatex.tools import runtex

if __name__ == '__main__':

    # Parameters for the script.
    root = '../examples/lamport-example'
    jobname = 'lamport-example'
    sourcename = 'sample2e.tex'
    
    # TODO: If DNE here, latex gets input file from texmf tree.
    inputdir = '../examples/lamport-example/src/'
    
    # The script fails if this directory does not exist.
    inputdir = f'{root}/src'
    rundir = f'{root}/run'

    boot = rf'\input ./misc/latex-preamble.sty \input {sourcename}'
    x = runtex(
        progname='latex',
        inputdir=inputdir,
        outputdir=rundir,
        jobname=jobname,
        boot=boot,
    )

    x.wait()
    print(x)

    logfilename = f'{rundir}/{jobname}.log'

    pattern = f'{root}/tbx/{jobname}.page.{{boxid}}.tbx'
    boxfile_template = pattern.format

    # All set, so read and write the boxes.
    from unlatex.tools import LogfileReader

    reader = LogfileReader(logfilename)
    reader.writeboxes(boxfile_template)    

    
