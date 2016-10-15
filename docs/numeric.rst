1. Numeric Commands
===================

Commands for numbers.

1.1. Pushing Numbers
--------------------

Pushing numbers is as easy as typing the number itself! ::

    1234     Pushes 1, 2, 3, and 4 individually.
    :144     Pushes 144 as a single number. The second : is implicit at the end of the file
    54n      Pushes 4 to the stack 5 times.
    "40"≈    Converts a string or float to an integer, int(x).
    "4.23"i  Converts a string to a float.
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
    37d      divmod(a,b). This returns 2, 1.
    :3.2K    Pushes ceil(a). This returns 4.
    :3.2L    Pushes floor(a). This returns 3.
    :-5A     The absolute value of a number.
    :-4s     sgn(x). If positive, return 1. If negative, return -1. Else, return 0.
    2:-3¢    abs(a)*sgn(b). This returns 3.
    :4.2m    This returns int(4.2), frac(4.2).
    35┤      Checks if a and b are coprime. This returns 1.
    7u       Increment once, or push a+1. This returns 8.
    9D       Decrement once, or push a-1. This returns 8.
    3⌐       Increment twice, or push a+2. This returns 5.
    5¬       Decrement twice, or push a-2. This returns 3.
    3ì       Pushes 1/a. This returns 1/3.
    8½       Pushes a/2 (float division). This returns 4.0.
    8¼       Pushes a/4 (float division). This returns 2.0.
    4τ       Pushes 2*a. This returns 8.
    4²       Pushes a*a. This returns 16.
    4√       Pushes sqrt(a). This returns 2.0.

1.4. Range Commands
-------------------

These are the commands that create ranges in Seriously. ::

    :12r     This creates the range [0, a). Returns the range [0,1,2,...,10,11].
    :25R     This creates the range [1, a]. Returns the range [1,2,3,...,24,25].
    92x      This creates the range [a, b). Returns the range [2,3,4,5,6,7,8].

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

    37&   Bitwise AND. This returns 3 (0b111 & 0b011 = 0b011).
    45|   Bitwise OR. This returns 5 (0b100 & 0b101 = 0b101).
    1~    Bitwise negate. This returns -2 (~ 0b01 = 0b10).
    32^   Bitwise XOR. This returns 1 (0b11 ^ 0b10 = 0b01).
    TBC

1.6. Commands for Complex Numbers
---------------------------------

Here are some of the commands for complex mathematics ::

    12Ç    Pushes a+bi. This returns (2+1i).
    :2+1i  : also pushes complex numbers. This returns (2+1i).
    ï      Pushes 0+1i.
    4î     Pushes 0+ai. This returns (0+4i).
    72Çá   Pushes the complex conjugate of z. This returns (2-7i).
    ï₧     phase(z) or the argument of z. This returns 1.57079632679.
    12Ç╫   Pushes Re(z), Im(z). This returns 2, 1.
    TBC

1.7. Trigonometric Functions
----------------------------

Here are the trigonometric functions. ::

    :30°   Converts to radians.
                This returns pi/6.
    2º     Converts to degrees.
                This returns 114.59155902616465.
    3S     Sine in radians.
                This returns sin(3) = 0.1411200080598672.
    2C     Cosine in radians.
                This returns cos(2) = -0.4161468365471424.
    4T     Tangent in radians.
                This returns tan(4) = 1.1578212823495775.
    1â     asin(a) (arcsine or inverse sine).
                This returns 1.5707963267948966.
    0ä     acos(a) (arccosine or inverse cosine).
                This returns 1.5707963267948966.
    3à     atan(a) (arctangent or inverse tangent).
                This returns 1.2490457723982544.
    13å    atan2(a,b) (2-argument arctangent, returns angle between positive x-axis and (a,b)).
                This returns 1.2490457723982544.
    4Ä     sinh(a) (hyperbolic sine).
                This returns 27.28991719712775.
    1Å     cosh(a) (hyperbolic cosine).
                This returns 1.5430806348152437.
    5É     tanh(a) (hyperbolic tangent).
                This returns 0.9999092042625951.
    6ç     asinh(a) (hyperbolic arcsine).
                This returns 2.491779852644912.
    9ê     acosh(a) (hyperbolic arccosine).
                This returns 2.8872709503576206.
    1ë     atanh(a) (hyperbolic arctangent).
                This returns 1.

1.8. Randomization Functions
----------------------------

Here are some commands that return random numbers. ::

    :100:20B     Pushes a random integer in the range [a, b). This returns a random integer in [20, 100) (like 42).
    G            Pushes a random float in the range [0, 1).
    :52J         Pushes a random integer in the range [0, a). This returns a random integer in [0, 52) (like 15).
    41V          Pushes a random float in range [a,b). This returns a random float in [1, 4) (like 3.5).
    :65537v      Seeds the RNG with a.
    TBC

1.9. Commands for the Primes
----------------------------

These functions deal with primes and factorization. ::

    0P        Returns the a-th prime. The 0th (first) prime is 2.
    :11p      Checks if a is prime. 11 is prime, so this returns 1.
    :10▓      Returns pi(a), the number of primes <= a. There are 4 primes <= 10.
    :60w      Returns the full positive prime factorization of abs(x). This returns [[2, 2], [3, 1], [5, 1]] (2**2 + 3**1 + 5**1).
    :72y      Returns The positive prime factors of abs(x). This returns [2, 3].

1.10. Base Conversion Commands
------------------------------

These commands deal with conversion to and from other bases. ::

    59¡      For a and b, pushes a string representing a in base b. This returns "14".
    5"14"¿   For a and b, Interprets [a] or "a" as a base-b int. This returns 9.
    :64├     bin(a) for ints, binary float data for floats, ascii_to_bin(a) for strings. This returns "1000000".
    :64─     Same as the bin built-in but to hexadecimal. This returns "40".
    :64▀     For a, pushes all of the digits in base a. 
               This returns "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/".

1.11. Miscellaneous Numeric Operators
------------------------------------

Here are the rest of Seriously's numeric operators. ::

    3"20"¿   Interprets a as a base-b int. This returns 6 (20 in base 3).
    3:20¡    Pushes a string representing a in base-b. This returns "202" (because 202 in base 3 is 20 in decimal).
    :16▀     Pushes digits in base a. This returns "0123456789ABCDEF" (hexadecimal digits).

    7!       The factorial function. This returns 5040.
    8Γ       The gamma function. This returns 5040.0.

    54g      gcd(a,b). This returns the gcd of 4 and 5 (1).
    68▲      lcm(a,b). This returns the lcm of 8 and 6 (24).
    :12:9▼   Pushes b//gcd(a,b), a//gcd(a,b). This returns 3, 4 (9//3, 12//3).
    5▒       totient(a), the number of integers < a that are coprime with a. This returns 4 (1, 2, 3, and 4).
    68h      The Euclidean norm of a and b, sqrt(a*a+b*b). This returns sqrt(8*8+6*6) = 10.0.

    :13F     Returns the a-th Fibonacci number. This returns 233.
    7f       Returns the Fibonacci index of a if a is a Fibonacci number, else, returns -1. This returns -1.

    :10╣     Pushes the a-th row of Pascal's triangle. This returns [1.0, 10.0, 45.0, 120.0, 210.0, 252.0, 210.0, 120.0, 45.0, 10.0, 1].
    38█      C(a,b). This returns 56.
    38▄      P(a,b). This returns 336.
    
    :20:_    ln(x). This returns ln(20).
    7e       exp(x). This returns exp(7).
    2E       erf(x). This returns erf(2).
    5╥       10**a. This returns 100000.
    4╙       log10(a). This returns log10(4).
    :20:Ó    2**a. This returns 1048576.
    :256:╘   log2(a). This returns 8.
    TBC

1.12. Important Constants
------------------------

Here are some important constants. ::

    ╦   pi
    ╠   e
    ╒   ln(2)
    φ   phi (golden ratio)
    TBC
