'''
Usage: $ python3 command_stats.py \
    '../examples/arxiv-2101.04419/tbx/2101.04419' \
    | head
47176 OT1/cmr/m/n/10
20883 glue
8277 hbox
6301 kern
5131 OT1/cmr/m/n/9
2724 penalty
2651 OT1/cmr/m/it/10
2266 OML/cmm/m/it/10
1698 mathon
1698 mathoff
'''

from unlatex.lextools import lex_lines

if __name__ == '__main__':

    import sys
    stem = sys.argv[1]

    # Create template for texbox filesl
    template = f'{stem}.page.{{boxid}}.tbx'.format

    # Set up a counter to record results.
    from collections import Counter
    grand_total = Counter()
    # Create stats for up to 1000 pages.
    for pageno in range(1, 1001):

        filename = template(boxid=pageno)
        try:
            f = open(filename)
        except FileNotFoundError:
            break

        lines =  map(str.rstrip, open(filename))
        items = lex_lines(lines)
        grand_total.update(item[1] for item in items)


    # Sort grand_total keys, most frequent first.
    keys = list(
         item[0]
         for item in sorted(grand_total.items(), key=lambda x: -x[1])
     )

    for key in keys:
        val = grand_total[key]
        print(f'{val} {key}')

# Other things you might try.
if False:

    # Process a single file.
    filename = template(boxid=1)

    # Print the lines that failed to lex properly.
    lines =  map(str.rstrip, open(filename))
    for item in lex_lines(lines):

        command = item[1]
        if command == 'LEXERROR':
            print(item)
