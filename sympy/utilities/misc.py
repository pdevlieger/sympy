"""Miscellaneous stuff that doesn't really fit anywhere else."""

from textwrap import fill, dedent

# if you use
# filldedent('''
#             the text''')
# a space will be put before the first line because dedent will
# put a \n as the first line and fill replaces \n with spaces
# so we strip off any leading and trailing \n since printed wrapped
# text should not have leading or trailing spaces.
filldedent = lambda s, w=70: '\n' + fill(dedent(str(s)).strip('\n'), width=w)


def rawlines(s):
    """Return a cut-and-pastable string that, when printed, is equivalent
    to the input. The string returned is formatted so it can be indented
    nicely within tests; in some cases it is wrapped in the dedent
    function which has to be imported from textwrap.

    Examples
    ========

    Note: because there are characters in the examples below that need
    to be escaped because they are themselves within a triple quoted
    docstring, expressions below look more complicated than they would
    be if they were printed in an interpreter window.

    >>> from sympy.utilities.misc import rawlines
    >>> from sympy import TableForm
    >>> s = str(TableForm([[1, 10]], headings=(None, ['a', 'bee'])))
    >>> print rawlines(s) # the \\ appears as \ when printed
    (
        'a bee\\n'
        '-----\\n'
        '1 10 '
    )
    >>> print rawlines('''this
    ... that''')
    dedent('''\\
        this
        that''')

    >>> print rawlines('''this
    ... that
    ... ''')
    dedent('''\\
        this
        that
        ''')

    >>> s = \"\"\"this
    ... is a triple '''
    ... \"\"\"
    >>> print rawlines(s)
    dedent(\"\"\"\\
        this
        is a triple '''
        \"\"\")

    >>> print rawlines('''this
    ... that
    ...     ''')
    (
        'this\\n'
        'that\\n'
        '    '
    )
    """
    lines = s.split('\n')
    if len(lines) == 1:
        return repr(lines[0])
    triple = ["'''" in s, '"""' in s]
    if any(li.endswith(' ') for li in lines) or '\\' in s or all(triple):
        rv = ["("]
        # add on the newlines
        trailing = s.endswith('\n')
        last = len(lines) - 1
        for i, li in enumerate(lines):
            if i != last or trailing:
                rv.append(repr(li)[:-1] + '\\n\'')
            else:
                rv.append(repr(li))
        return '\n    '.join(rv) + '\n)'
    else:
        rv = '\n    '.join(lines)
        if triple[0]:
            return 'dedent("""\\\n    %s""")' % rv
        else:
            return "dedent('''\\\n    %s''')" % rv

import sys
size = getattr(sys, "maxint", None)
if size is None:  # Python 3 doesn't have maxint
    size = sys.maxsize
if size > 2**32:
    ARCH = "64-bit"
else:
    ARCH = "32-bit"

# Python 2.5 does not have sys.flags (it doesn't have hash randomization either)
HASH_RANDOMIZATION = hasattr(sys, 'flags') and getattr(sys.flags,
                                                       'hash_randomization',
                                                       False)


def debug(*args):
    """
    Print ``*args`` if SYMPY_DEBUG is True, else do nothing.
    """
    from sympy import SYMPY_DEBUG
    if SYMPY_DEBUG:
        for a in args:
            print a,
        print
