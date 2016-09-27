2. String Commands
==================

Commands for strings. Many of these commands also work for lists.

2.1. Pushing Strings
--------------------

Pushing strings is as simple as `'1'2'3`! ::

    'a     Pushes one character.
    "b     Pushes a string until the next " or the end of the file is reached.
    'c5*   This repeats "c" 5 times.
    :25$   str(a). This returns "25".
    ,      This reads a value from STDIN and pushes it to the stack.
             Actually automatically reads STDIN and pushes it to the stack at the beginning of the program if you omit ","
    §      Pushes all data from STDIN as a string.
    ○      Pushes a single byte of unformatted input from STDIN. (This character is NOT lowercase o)
    .      Writes the top value of the stack to STDOUT.

2.2. Strings, Elements and Indices
----------------------------------

Here are the commands to get some elements of a string, either by indices or randomly. ::

    "world"l    len("a"). This returns 5.
    "abcd"N     a[-1]. This returns 'd'.
    2"abcd"H    a[:b]. This returns "ab".
    2"abcd"t    a[b:]. This returns "cd".
    5"world"V   Pushes all slices of "world" length 1 <= n <= b.
                    This returns ['w', 'wo', 'wor', 'worl', 'world', 'orld', 'rld', 'ld', 'd'].
    "abcdef"J   Pushes a random element of "abcdef".
    'c"abcd"í   "a".index(b) (0-based, -1 if not found). This returns 2.

2.3. String Manipulation
------------------------

These commands manipulate a single string. ::

    "abcd"R               Reverses a string. This returns "dcba".
    "world"S              Sorts a string. This returns "dlorw".
    [5,6,7]", "j          "a".join([b]) for string "a" and list [b]. This returns "5, 6, 7".
    [5,6]"%d,%d"%         %-formatting. This returns "5,6".
    [5,6]"{},{}"f         Python-style formatting. Pushes "a".format(*[b]) for string "a" and list [b]. This returns "5,6".
    ['t]"stats"           Splits "stats" by any occurrences of elements of ["t"]. Returns ["s", "a", "s"]
    "tv""bc""abacus"t     Pushes a.translate(str.maketrans(b,c)). This returns "atavus".
    ["hello", "world"]O   Pushes ord() for each character in "hello".
                            This returns [104, 101, 108, 108, 111, 119, 111, 114, 108, 100].
    "  abc  "ô            "a".strip(). This returns "abc".
    "  abc  "ö            "a".lstrip(). This returns "abc  ".
    "  abc  "ò            "a".rstrip(). This returns "  abc".
    "aBcD"û               "a".upper(). This returns "ABCD".
    "aBcD"ù               "a".lower(). This returns "abcd".
    "aBcD"ÿ               "a".title(). This returns "Abcd".
    "aBcD"Ö               "a".swapcase(). This returns "AbCd".

2.4. Multiple Strings
---------------------

These are the commands that manipulate multiple strings. ::

    'b'a+         Concatenates strings. This returns "ab".
    "ab""acda"-   [a]-[b] (all elements of [a] not in [b]). Works for string and lists. This returns ['c', 'd'].
    'a"abacus"c   Pushes "abacus".count("a"). This returns 2.

2.5. Constant Strings
---------------------

Here are some constant strings. ::

    H   If stack is empty, push "Hello, World!"
    N   If stack is empty, push the lyrics to "99 Bottles of Beer".

