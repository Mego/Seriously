1. Numeric Commands
===================

Commands for numbers.

1.1. Pushing Numbers
--------------------

Pushing numbers is as easy as typing the number itself! ::

    1234    Pushes 1, 2, 3, and 4 individually
    :144:   Pushes 144 as a single number

1.2. Basic Arithmetic
---------------------

Seriously is a postfix language, meaning that operators come after arguments. ::

    23+     This adds 3 to 2.
    79-     Subtracts 7 from 9.
    35*     Multiplies 5 by 3.
    83/     Float division. This divides 3 by 8 returning 0.375.
    37\     Integer division. This divides 7 by 3 returning 2.

1.3. Other Arithmetical Operators
---------------------------------

Other important operators in arithmetic include: ::

    7:29:%  Modulo operator. This calculates 29 mod 7, returning 1.
    4!      Factorial. This calculates 4!, returning 24

1.4. Boolean Operators
----------------------

The boolean operators operate on the last two stack elements as follows ::

    33=     Boolean equal. Since 3 = 3, 1 is pushed onto the stack (otherwise 0).
    44<     Boolean less than. Since 4 is not less than 4, 0 is pushed onto the stack (otherwise 1).
    25>     Boolean greater than. Since 2 is not greater than 5, 0 is pushed onto the stack (otherwise 1).

The following boolean operators relate to logic gates ::

    01^     XOR. 0 XOR 1 is equal to 1, so 1 is returned. 

1.5. Extended Math Functions
----------------------------

More advanced than 1.3. ::

    :8:f    Fibbonaci index. Since 8 is the 6th fibbonaci number, 6 is returned. If a non-fibbonaci number is input, returns -1

1.5. Trig Functions
-------------------

These perform trig operations on the stack ::

    â       Performs asin on the stack.
    ä       Performs acos on the stack.
    à       Performs atan on the stack.
    å       Performs atan2 on the last two stack elements.
    
