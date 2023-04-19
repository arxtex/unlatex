'''Using logarithms to make data more accessible


Here is a real world example. Suppose we have
>>> data = (1, 4, 132, 2310, 79, 4, 3, 21)

A sighted person can see at a glance that it's roughly bell shaped,
except for the last entry, which is unexpectedly large.

The next example transforms the data, so it works better for a blind
person. It reduces the numbers that makes clearer the same rough bell
shape, with an unexpectedly large final entry.
>>> log10(data)
(1, 1, 3, 4, 2, 1, 1, 2)

If more detail is required, reduce the base of the log. This increase
the resolution.
>>> log4(data)
(1, 2, 4, 6, 4, 2, 1, 3)

We can if we wish do this again.
>>> log2(data)
(1, 3, 8, 12, 7, 3, 2, 5)

The next example shows that log10 gives the number of digits in the
decimal representation, with 0 as a special case.

>>> log10([0, 1, 9, 10, 99, 100, 999, 1000])
(0, 1, 1, 2, 2, 3, 3, 4)

Note that 10**3 = 1000 and that 1000 is the smallest number that
requires 4 decimal digits. The logarithm of 1000 base 10 is by
definition the number 3. All counting numbers strictly less than 1000
have a logarithm that is strictly less than 3.

The example came from unlatex, Lamport example page 1.
# >>> for item in sorted(count.items()): print(item)
...
('', 1)
('.', 4)
('..', 7)
('...', 132)
('....', 2310)
('.....', 79)
('......', 4)
('.......', 3)
('........', 21)
('....|', 2)
('ne ', 1

'''

import math

def log10(count_numbers):

    return tuple( digit_count(10, n) for n in count_numbers )

def log4(count_numbers):

    return tuple( digit_count(4, n) for n in count_numbers )

def log2(count_numbers):

    return tuple( digit_count(2, n) for n in count_numbers )

def digit_count(base, n):
    '''Return number of digits when n is written in the base.

    Negative n is not allowed. If (n == 0), the function returns 0.
    '''

    # TODO? Require base to be a positive counting number.
    if n < 0:
        raise ValueError

    n = math.ceil(n)
    if n == 0:
        return 0

    n = n + 1
    val = math.ceil(math.log(n, base))
    return val
