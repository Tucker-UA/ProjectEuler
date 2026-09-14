from functools import cache

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

    possiblePrimes = primes(maxPrime + 1) if maxPrime > 1 else primes(n+1)

    factorization = dict()

    for p in possiblePrimes:
        if n < p:
            break
        elif n % p != 0:
            continue

        factorization[p] = 1
        n = n // p

        while n % p == 0:
            factorization[p] += 1
            n = n // p

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

def isprime(n, maxPrime = 1):
    """
    Function that determines if n is a prime or not.
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
        return isprime(-n, maxPrime)

    if maxPrime == 1:
        return n == primes(n+1)[-1]

    return n in primes(maxPrime + 1)

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
    print("Generating primes")
    p = METHODS[method](N)
    print("Primes Generated")
    return p

