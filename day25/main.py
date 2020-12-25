'''

This is similar to the Diffie-Hellman key exchange.

Public information:
N = 20201227 (modulus)
g = 7 (generator)

Private information:
c = #card loops (secret)
d = #door loops (secret)

Each party derives its pub key:
card_pubkey = g ^ c (mod N)
door_pubkey = g ^ d (mod N)

Parties exchange their pub keys. Now:

1. At the door side, it can calculate:
enc_key = card_pubkey ^ d (mod N) = g ^ (c * d) (mod N)

2. At the card side, it can calculate
enc_key = door_pubkey ^ c (mod N) = g ^ (d * c) (mod N)

Now both parties have agreed on a secret enc_key without ever transmiting it!
'''

import fileinput

N = 20201227
g = 7


def fast_exp(base, exp):
    '''This is an amazing recursive optimization for fast exponentiation.
    Pulled from the bible itself: https://mitpress.mit.edu/sites/default/files/sicp/full-text/sicp/book/node18.html
    '''
    if exp == 0:
        return 1
    # exp is odd.
    elif exp % 2 == 1:
        return (base * fast_exp(base, exp - 1)) % N
    # exp is even.
    else:
        return (fast_exp(base, exp // 2) ** 2) % N


def transform(subject, loop):
    # This is faster (by a constant factor, I believe) than
    # the `fast_exp` above, but what's the fun?
    # return pow(subject, loop, N)

    # ** Chef's kiss **
    return fast_exp(subject, loop)


def part1(card_pubkey, door_pubkey):
    # Let's find the card's loop number.
    card_loop = 0
    while True:
        if transform(g, card_loop) == card_pubkey:
            break
        card_loop += 1
    print('Found:', card_loop)

    # Now we can derive the encryption key by exponentiating
    # the door's pub key with card loop.
    return transform(door_pubkey, card_loop)


def main():
    card_pubkey, door_pubkey = [int(line.strip())
                                for line in fileinput.input()]
    print(part1(card_pubkey, door_pubkey))


if __name__ == '__main__':
    main()
