1. Numeric Commands
===================

Commands for numbers.

1.1. Pushing Numbers
--------------------

Pushing numbers is as easy as typing the number itself! ::

    1234     Pushes 1, 2, 3, and 4 individually.
    :144:    Pushes 144 as a single number. The second : is implicit at the end of the file
    54n      Pushes 4 to the stack 5 times.
    "40"≈    Converts a string or float to an integer, int(x).
    "4.23"   Converts a string to a float.
    5±       Pushes a number x, then pops x and pushes -x.
    TBC

1.2. Basic Arithmetic
---------------------

Seriously is a postfix language, meaning that operators come after arguments. ::

    23+     This adds 3 to 2.
    79-     Subtracts 7 from 9.
    35*     Multiplies 5 by 3.
    83/     Float division. This divides 3 by 8 returning 0.375.
    37\     Integer division. This divides 7 by 3 returning 2.
    TBC

1.3. Other Arithmetical Operators
---------------------------------

Other important operators in arithmetic include: ::

    45ⁿ      Exponentiation. This raises 5 to the power of 4, returning 15625.
    7:29:%   Modulo operator. This calculates 29 mod 7, returning 1.
    3ì       Push 1/a.

    :-5:A    The absolute value of a number.
    :-4:s    sgn(x). If positive, return 1. If negative, return -1. Else, return 0.
    2:-3:¢   abs(a)*sgn(b)
    :4.2:m   Returns int(4.2), frac(4.2).
    35┤      Checks if a and b are coprime.
    TBC

1.4. Range Commands
-------------------

These are the commands that create ranges in Seriously. ::

    :12:r    Returns the range [0,1,2,...,10,11].
    :25:R    Returns the range [1,2,3,...,24,25].
    92x      Returns the range [2,3,4,5,6,7,8,9].

1.5. Boolean Operators
----------------------

Here are the comparison operators. ::

    33=   Equality comparator. 3 = 3, so this returns True.
    43<   Less-than. 3 < 4, so this returns True.
    75>   Greater-than. 5 not > 7, so this returns False.
    92≤   Less-than-or-equal. 2 ≤ 9, so this returns True.
    58≥   Greater-than-or-equal. 8 ≥ 5, so this returns True.
    1b    Logical buffer. If False, return 0. Else, return 1. Works for numbers, strings, lists and functions.
    0Y    Logical NOT. If False, return 1. Else, return 0. Works for numbers, strings, lists and functions.
    TBC

Here are the bitwise operators. ::

    37&   Bitwise AND
    45|   Bitwise OR
    1~    Bitwise negate
    32^   Bitwise XOR
    TBC

1.6. Commands for Complex Numbers
---------------------------------

Here are some of the ::

    12Ç    Pushes a+bi. This returns (2+1i).
    ï      Pushes 0+1i.
    4î     Pushes 0+ai. This returns (0+4i).
    72Çá   Pushes the complex conjugate of z. This returns (2-7i)
    ï₧     phase(z) or the argument of z. This returns 1.57079632679.
    TBC

1.7. Trigonometric Functions
----------------------------

Here are the trigonometric functions. ::

    :30°   Converts to radians.
    2º     Converts to degrees.
    3S     Sine in radians.
    2C     Cosine in radians.
    4T     Tangent in radians.
    9â     asin(a)
    7à     acos(a)
    3å     atan(a)
    13†    atan2(a,b)
    4Ä     sinh(a)
    1Å     cosh(a)
    5É     tanh(a)
    6ç     asinh(a)
    9ê     acosh(a)
    2ë     atanh(a)

1.8. Randomization Functions
----------------------------

Here are some commands that return random numbers. ::

    :100::20:B   Pushes a random integer in the range [a, b).
    G            Pushes a random float in the range [0, 1).
    :52:J        Pushes a random integer in the range [0, a).
    41V          Pushes a random float in range [a,b].
    :65537:v     Seeds the RNG with a.
    TBC

1.9. Commands for the Primes
----------------------------

These functions deal with primes and factorization. ::

    0P        Returns the a-th prime.
    :11:p     Checks if a is prime.
    :1000:▓   Returns pi(a), the number of primes <= a.
    :60:w     Returns the full positive prime factorization of abs(x).
    :72:y     Returns The positive prime factors of abs(x).

1.10. Miscellaneous Numeric Operators
------------------------------------

Here are the rest of Seriously's numeric operators. ::


    7u       Increment once, or push a+1.
    9D       Decrement once, or push a-1.
    3⌐       Increment twice, or push a+2.
    5¬       Decrement twice, or push a-2.
    8½       Pushes a/2 (float division).
    8¼       Pushes a/4 (float division).
    4τ       Pushes 2*a.
    4ª       Pushes a*a.
    4√       Pushes sqrt(a).

    3:20:¿   Interprets a as a base-b int.
    3:20:¡   Pushes a string representing a in base-b.
    :16:▀    Pushes digits in base a.

    7!       The factorial function.
    8Γ       The gamma function.

    54g      gcd(a,b). This returns the gcd of 4 and 5.
    5▒       totient(a), the number of integers <= a that are coprime with a.
    98h      The Euclidean norm of a and b, a*a+b*b. This returns 8*8+9*9 = 145.

    :13:F    Returns the a-th Fibonacci number.
    7f       Returns the Fibonacci index of a if a is a Fibonacci number, else, returns -1.

    :10:╣    Pushes the a-th row of Pascal's triangle.
    38█      C(a,b). This returns 56.
    38▄      P(a,b). This returns 336.
    
    :20:_    ln(x). This returns ln(20).
    2E       erf(x). This returns erf(2).
    7e       exp(x). This returns exp(7).
    5╥       10**a. This returns 100000.
    4╙       log10(a). This returns log10(4).
    :20:Ó    2**a. This returns 1048576.
    :256:╘   log2(a). This returns 8.
    TBC

1.11. Important Constants
------------------------

Here are some important constants. ::

    ╦   pi
    ╠   e
    ╒   ln(2)
    φ   phi (golden ratio)
    TBC
