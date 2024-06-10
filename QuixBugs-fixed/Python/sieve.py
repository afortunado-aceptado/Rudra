def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if all(n % p != 0 for p in primes):
            primes.append(n)
    return primes
'''
The original code has a logical error in the condition used to check if a number \(n\) is prime. Specifically, the condition \texttt{any(n \% p > 0 for p in primes)} is incorrect because it appends \(n\) to the list of primes if \(n\) is not divisible by any prime number already in the list. However, the use of \texttt{any} and the comparison \texttt{> 0} are not the right approach to determine primality. The correct approach is to check if \(n\) is divisible by any of the primes already found, and if it is not, then \(n\) is a prime number. This is achieved by using \texttt{all(n \% p != 0 for p in primes)}, which ensures that \(n\) is only appended to the list of primes if it is not divisible by any of the primes already in the list. This change corrects the logic, ensuring that the function correctly identifies and returns all prime numbers up to and including the given maximum value.

'''