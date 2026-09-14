import primes

maxPrime = 20000
totients = [primes.totient(n, maxPrime) for n in range(2,maxPrime+1)]
targetTotients = [t for i, t in enumerate(totients) if i % 2 == 1 and (primes.isprimepower(i+1,maxPrime) or primes.isprimepower(i+3,maxPrime))]


def irreducibles(n):
    """
    Finds the number of irreducible dynamical polynomials of degree n
    """
    if n == 1:
        return 2

    d = 2*n

    return targetTotients.count(d)



def prob812(n):
    """
    Finds all dynamical polynomials of degree n
    """
    for a in range(1,n+1):
        print(irreducibles(a))
    pass

if __name__ == "__main__":
    n = 5
    prob812(n)
    print([t for t in targetTotients if t <= 2**n+1])
