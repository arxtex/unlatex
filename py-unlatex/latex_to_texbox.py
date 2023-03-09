'''

Useage: py-unlatex$ python3 \
    latex_to_texbox.py \
    TMP/OUT \
    ../examples/arxiv-2101.04419/tbx \
    2101.04419 \
    ../examples/arxiv-2101.04419/src/sigma21-103.tex
'''


if __name__ == '__main__':

    # Determine the stem part of the script name.
    import sys
    import os.path

    outdir = sys.argv[1]
    texbox_dir = sys.argv[2]
    jobname = sys.argv[3]
    tex_main = sys.argv[4]

    head, tail = os.path.split(tex_main)
    inputdir = head

    # The script fails if outdir or texbox_dir do not exist.
    # TODO: More elegant failure?

    tex_driver = './misc/latex-preamble.sty'
    boot_main = rf'\input {tex_main}'
    boot_driver = rf'\input {tex_driver}'

    boot = rf'{boot_driver} {boot_main} \relax '

    # All set, do typeset the document.
    from unlatex.tools import runtex

    x = runtex(
        progname='latex',
        inputdir=inputdir,
        outputdir=outdir,
        jobname=jobname,
        boot=boot,
    )

    x.wait()
    print(x)


    # Now set up to create the texboxes.
    stem = os.path.splitext(tail)[0]
    logfilename = os.path.join(outdir, jobname + '.log')
    pattern = f'{texbox_dir}/{jobname}.page.{{boxid}}.tbx'
    boxfile_template = pattern.format

    # All set, so read and write the boxes.
    from unlatex.tools import LogfileReader

    reader = LogfileReader(logfilename)
    # TODO: Provide parameter to control progress reporting.
    reader.writeboxes(boxfile_template)
