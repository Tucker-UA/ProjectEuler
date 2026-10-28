from functools import cache
from math import isqrt

# Functions not related to the math


# Functions related to the math

def gcd(a,b, *args):
    # Returns the GCD of two integers
    # Uses a variation of Euclid
    length = len(args)
    if length == 1:
        return gcd(a, gcd(b, *args))
    elif length > 1:
        newArgs = [a,b] + [c for c in args]
        mid = length // 2 + 1
        first = newArgs[:mid]
        last = newArgs[mid:]
        return gcd(gcd(*first), gcd(*last))

    a = abs(a)
    b = abs(b)
    if a < b:
        return gcd(b,a)
    elif a == b:
        return a

    while b > 0:
        c = a % b
        a = b
        b = c

    return a

def factor(n, maxPrime = 1):
    """
    Implements a factorization of n.
    Inputs:
        - n:            integer
        - maxPrime:     positive integer > 2
    Output:
        - factorization = {p : e}   dict of primes : exponents

    n = product(pow(p,e) for p, e in factorization.items()) 
    """
    if not isinstance(n, int):
        raise Exception(f"Not defined for non-integers {n}")
    if n < 0:
        return factor(-n, maxPrime)

    squareRootLimit = isqrt(n)+1

    possiblePrimes = primes(maxPrime + 1) if maxPrime > 1 else primes(squareRootLimit)

    factorization = dict()

    for p in possiblePrimes:
        if p > squareRootLimit:
            break
        elif n % p != 0:
            continue

        factorization[p] = 1
        n = n // p

        while n % p == 0:
            factorization[p] += 1
            n = n // p

    if n > 1:
        factorization[n] = 1

    return factorization

def totient(n, maxPrime = 1):
    """
    Implements the Euler Totient function.
    Inputs:
        - n:            integer
        - maxPrime:     positive integer > 2
    Output:
        - totient(abs(n))

    If maxPrime == 1, then totient will call primes(n+1).
    Otherwise, totient will call primes(maxPrime+1).
    This is done as primes will be a cached function.
    There is probably a better implementation to be done with generators.
    """
    if not isinstance(n, int):
        raise Exception(f"Not defined for non-integers {n}")
    elif n == 0 or n == 1:
        raise Exception(f"Totient function not defined for {n}")
    elif n < 0:
        return totient(-n, maxPrime)

    possiblePrimes = primes(maxPrime+1) if maxPrime > 1 else primes(n+1)

    factorization = factor(n, maxPrime)
    
    t = 1
    
    for p, e in factorization.items():
        if e > 1:
            t *= pow(p,e-1)*(p-1)
        else:
            t *= p-1

    return t

# Functions for checking if a number is prime

# The really naive approach
def isprimeNaive(n, maxPrime = 1):
    """
    Function that determines if n is a prime or not.
    Does so by checking if it is in the list of primes.

    Inputs:
        - n:            integer
        - maxPrime:     positive integer > 2
    Output:
        - True or False

    If maxPrime == 1, then we will call primes(n+1).
    Otherwise, we will call primes(maxPrime + 1).
    """
    if n >= maxPrime:
        return n == primes(n+1)[-1]

    return n in primes(maxPrime + 1)

def isprimeDivision(n, maxPrime = 1):
    """
    Function that determines if n is a prime or not.
    Does so by checking if it is divisible by primes less than maxPrime.

    Inputs:
        - n:            integer
        - maxPrime:     positive integer > 2
    Output:
        - True or False

    If maxPrime == 1, then we will set maxPrime = isqrt(n).
    """
    if maxPrime == 1:
        maxPrime = isqrt(n)

        if maxPrime**2 == n:
            return False

    for p in primes(maxPrime+1):
        if n % p == 0:
            return n == p
        elif n < p:
            break

    return True

def probablePrime(base, n):
    """
    Checks to see if n is a probable prime in the given base
    Assumes that the base is prime.
    Returns true if n satisfies pow(base, n-1, n) = 1
    Returns false otherwise.
    """
    return pow(base, n-1, mod=n) == 1

def strongProbablePrime(base, n):
    """
    Checks to see if n is a strong probable prime in the given base
    Assumes that the base is prime.
    Returns true if n satisfies pow(base, d, n) == 1 or pow(base ** d, 2 ** r, n) == -1 for n-1 = (2**s)*d and 0 < r < s
    Returns false otherwise.
    """
    m = n - 1
    d = m
    s = 0

    while d % 2 == 0:
        d = d // 2
        s += 1

    if pow(base, d, n) == 1:
        return True

    e = base ** d

    for r in range(s):
        if pow(e, 2**r, n) == -1:
            return True

    return False

def multipleStrongProbablePrime(bases, n):
    """
    Does the strong probable prime test for the given bases.
    Returns False if any is not a strong probable prime
    """
    return all(strongProbablePrime(base, n) for base in bases)

def isprimeStrong(n, maxPrime = 1):
    """
    Using strong probable primes and numbers from t5k.org, we check for primality.
    Tries to do as few strong probable primes as possible.
    Returns True if it succeeds and False otherwise.
    Will only be probabilistic for n > 341*pow(10,12)
    """
    if n < 1373653:
        return multipleStrongProbablePrime([2,3], n)
    elif n < 25326001:
        return multipleStrongProbablePrime([2,3,5], n)
    elif n < 2152302898747:
        return multipleStrongProbablePrime([2,3,5,7,11], n)
    elif n < 3474749660383:
        return multipleStrongProbablePrime([2,3,5,7,11,13], n)
    
    return multipleStrongProbablePrime([2,3,5,7,11,13,17], n)

primalityMethods = {"Naive" : isprimeNaive, "Trial Division" : isprimeDivision}
primalityMethods["Best Deterministic"] = isprimeDivision
primalityMethods["Best Probabilistic"] = isprimeStrong

@cache
def isprime(n, method = "Best Probabilistic", **kwargs):
    """
    Function that allows you to pick the method for finding if a number is prime
    """
    if not isinstance(n, int):
        raise Exception(f"Not defined for non-integers {n}")
    elif n < 0:
        return isprime(-n, method = method, **kwargs)
    elif n == 1:
        return False
    elif n % 2 == 0:
        return n == 2
    elif n % 3 == 0:
        return n == 3

    return primalityMethods[method](n,**kwargs)


def isprimepower(n, maxPrime = 1):
    """
    Function that determines if n is a prime power or not
    Inputs:
        - n:            integer
        - maxPrime:     positive integer > 2
    Output:
        - True or False

    If maxPrime == 1, then we will call primes(n+1).
    Otherwise, we will call primes(maxPrime + 1).
    """
    if not isinstance(n, int):
        raise Exception(f"Not defined for non-integers {n}")
    elif n < 0:
        return isprimepower(-n, maxPrime)

    factorization = factor(n, maxPrime)

    if len(factorization) > 1:
        return False

    return True

# Ways to find all primes less than N below here

def primesErato(N):
    # Return all primes less than N as a list
    if N <= 2:
        return []

    start = 2
    sieve = list(range(start,N))
    stop = N-start

    for s in sieve:
        if s == 0:
            continue
        elif s == 2:
            sieve[s::s] = [0] * -((s-stop) // s)

        bottom = s*s - start  # Reason why this is our bottom is because 
                         # All the smaller numbers were multiples of other primes
        if bottom >= stop: # If we got out of the list index range
            break

        sieve[bottom::s] = [0] * -((bottom - stop) // s)
        # The above uses a nice slice to set those entries to 0

    return [p for p in sieve if p > 0]

METHODS = {"Eratosthenes" : primesErato}

@cache
def primes(N, method = "Eratosthenes"):
    # Return all primes less than N as a tuple
    # Uses method requested
    #print("Generating primes")
    p = METHODS[method](N)
    #print("Primes Generated")
    return p

