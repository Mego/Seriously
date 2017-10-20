import random


def find_spelling(n):
    """
    Finds d, r s.t. n-1 = 2^r * d
    """
    r = 0
    d = n - 1
    # divmod used for large numbers
    quotient, remainder = divmod(d, 2)
    # while we can still divide 2's into n-1...
    while remainder != 1:
        r += 1
        d = quotient  # previous quotient before we overwrite it
        quotient, remainder = divmod(d, 2)
    return r, d


def probably_prime(n, k=10):
    """
    Miller-Rabin primality test
    Input: n > 3
    k: accuracy of test
    Output: True if n is "probably prime", False if it is composite

    From psuedocode at https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    """
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    r, d = find_spelling(n)
    for check in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, d, n)  # a^d % n
        if x == 1 or x == n - 1:
            continue
        for i in range(r):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True