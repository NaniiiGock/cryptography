import random
from hashlib import sha256
from secrets import compare_digest
from primes import primes


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def extended_gcd(e, fi):
    x, x1, y, y1 = 0, 1, 1, 0
    while fi != 0:
        coeff = e // fi
        e, fi = fi, e - coeff * fi
        x1, x = x, x1 - coeff * x
        y1, y = y, y1 - coeff * y
    return x1


def create_e(fi):
    while True:
        e = random.randrange(2, fi)
        if e in primes and (gcd(e, fi) == 1):
            return e


def create_keys():
    p1 = primes[random.randint(30, 120)]
    p2 = primes[random.randint(30, 120)]
    while p2 == p1:
        p2 = primes[random.randint(2, 10)]
    n = p1 * p2
    fi = (p1 - 1) * (p2 - 1)
    e = create_e(fi)
    d = extended_gcd(e, fi)
    if (d < 0):
        d += fi
    return n, e, d


def encrypt(message, en):
    e, n = en
    message, blocks = message, []

    for i in range(len(message)):
        number = ord(message[i])
        number = (number ** e) % n
        blocks.append(str(number))
    return " ".join(blocks)


def decrypt(blocks, dn):
    d, n = dn
    blocks = blocks.split(' ')
    message = ""

    for number in blocks:
        letter_index = ((int(number)) ** d) % n
        letter = chr(letter_index)

        message += letter
    return message


def main():
    """check with hashing"""

    n, e, d = create_keys()
    print(n, e, d)

    m = "hi"
    sha256_digest_1 = sha256(m.encode("utf-8"))
    digest_1 = sha256_digest_1.digest()
    hexdigest_1 = sha256_digest_1.hexdigest()

    encrypted = encrypt(m, (n, e))
    print("ENCRYPTED:", encrypted)
    decrypted = decrypt(encrypted, (d, n))
    print("DECRYPTED:", decrypted)

    sha256_digest_2 = sha256(decrypted.encode("utf-8"))
    digest_2 = sha256_digest_2.digest()
    hexdigest_2 = sha256_digest_2.hexdigest()
    print(compare_digest(digest_1, digest_2))
    print(compare_digest(hexdigest_1, hexdigest_2))


if __name__ == "__main__":
    main()
