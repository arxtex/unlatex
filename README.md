# unlatex

## In a nutshell
An inverse to the latex compiler. From a texbox construct source and macros. Hence the name.

## News

[9 March 2023] There is now a script that typesets a LaTeX file and from that generates the texbox files. See below for how it's done.


## Summary

`latex` is a document compiler. From a source file it
produces PDF. However, `unlatex` goes the other way. Hence the name.

To produce a page of PDF, `latex` ships out an internal TeX box. The
starting point of `unlatex` is a text representation of that box. This
TeX Hour will demonstrate software to produce such files. It can
process any source file file that `latex` can process.

The resulting `texbox` files provide a very good starting point for
reconstructing the original source file, and also the style files that
created the PDF.  The `texbox` files are also a good starting point
for creating an Accessibility Tree. The access tree is the object the
screen reader interacts with, when reading an accessible document.

## Creating texbox files

To create texbox files you must first typeset the latex source file in
a slightly special environment, and then extract the texbox files from
the log files.

Although not complicated it is a bit fiddly, and it's something that
should be automated. There are thousands of latex documents out there. Here's how to do it, by example.

```
$ mkdir anydir
$ cd anydir
anydir$ git clone git@github.com:arxtex/unlatex.git
Cloning into 'unlatex'...
remote: Enumerating objects: 123, done.
remote: Counting objects: 100% (123/123), done.
remote: Compressing objects: 100% (52/52), done.
remote: Total 123 (delta 71), reused 104 (delta 60), pack-reused 0
Receiving objects: 100% (123/123), 429.90 KiB | 898.00 KiB/s, done.
Resolving deltas: 100% (71/71), done.

/anydir$ cd unlatex/py-unlatex/
/anydir/unlatex/py-unlatex$ mkdir TMP
/anydir/unlatex/py-unlatex$ mkdir TBX

/anydir/unlatex/py-unlatex$ # From https://arxiv.org/format/2101.04419 download source IN YOUR BROWSER

anydir/unlatex/py-unlatex$ mkdir SRC

anydir/unlatex/py-unlatex$ mv ~/Downloads/2101.04419 SRC

anydir/unlatex/py-unlatex$ cd SRC
anydir/unlatex/py-unlatex/SRC$ file 2101.04419
2101.04419: POSIX tar archive (GNU)
/anydir/unlatex/py-unlatex/SRC$ tar xvf 2101.04419
5loops.png
Blowupsimplex.pdf
SunriseSimplex.pdf
Wheel3.png
WheelN.pdf
sigma.cls
sigma21-103.tex

anydir/unlatex/py-unlatex/SRC$ cd ..

anydir/unlatex/py-unlatex$ python3 latex_to_texbox.py TMP TBX your-jobname SRC/sigma21-103.tex
This is pdfTeX, Version 3.141592653-2.6-1.40.24 (TeX Live 2022) (preloaded format=latex)
 restricted \write18 enabled.
entering extended mode
<Popen: returncode: 0 args: ['latex', '--halt-on-error', '--interaction=batc...>
TBX/your-jobname.page.1.tbx
[...]
TBX/your-jobname.page.54.tbx
```
