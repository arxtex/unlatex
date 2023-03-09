'''From TeX log file extract and write its page texbox's.
Useage: $ python3 log_to_texbox.py TMP/OUT/boxlog_sample2e.log

Input: path/to/stem.log
Output: path/to/stem.page.1.texbox
   ...

Use this as a starting point for writing your own automation
scripts.  I hope to provide an example of such later.
'''


if __name__ == '__main__':

    # Get name of logfile from command line arguments.
    import sys
    logfilename = sys.argv[1]

    # Check that it is a logfile name.
    import os
    root, ext = os.path.splitext(logfilename)
    if ext != '.log':
        raise ValueError(logfilename)

    # Provide a template for boxfile names.
    # WARNING: Script will fail if template give DNE directory.
    pattern = f'{root}.page.{{boxid}}.texbox'
    boxfile_template = pattern.format

    # All set, so read and write the boxes.
    from unlatex.tools import LogfileReader

    reader = LogfileReader(logfilename)
    # TODO: Provide parameter to control progress reporting.
    reader.writeboxes(boxfile_template)
