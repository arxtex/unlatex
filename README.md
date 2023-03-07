# unlatex

## In a nutshell
An inverse to the latex compiler. From a texbox construct source and macros. Hence the name.

## Coming soon

For more information see [9 March 2023 TeX Hour](https://texhour.github.io/2023/03/09/unlatex-texbox-access-tree/). I intend before the TeX Hour to populate this repository with some tools and scripts.

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
