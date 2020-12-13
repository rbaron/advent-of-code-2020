import fileinput
import math


def part1(ts, ids):
    waits = [
        (i, i - (ts % i))
        for i in ids
    ]
    m = min(waits, key=lambda wait: wait[1])
    return m[0] * m[1]


def part2_slow(i_ids):
    '''Works with the test inputs. Too slow for the real deal.'''
    max_i, max_id = max(i_ids, key=lambda iid: iid[1])
    print(max_i, max_id)
    i = 1
    while True:
        t = max_id * i - max_i
        if all((t + idx) % id_ == 0 for idx, id_ in i_ids):
            return t
        i += 1


def modinv(a, m):
    '''Returns a^-1 mod m.'''
    return pow(a, -1, m)


def part2(i_ids):
    '''Uses the Chinese Remainder Theorem to solve the congruence system.
    https://brilliant.org/wiki/chinese-remainder-theorem/.

    My system is like the following:

    t = -index0 mod(bus_id0)
    t = -index1 mod(bus_id1)
    t = -index2 mod(bus_id2)
    t = -index3 mod(bus_id3)
    ...
    '''
    ais = [-idx for idx, _ in i_ids]
    nis = [bus_id for _, bus_id in i_ids]
    N = math.prod(nis)
    yis = [N // ni for ni in nis]
    zis = [modinv(y, n) for y, n in zip(yis, nis)]
    return sum(a * y * z for a, y, z in zip(ais, yis, zis)) % N


def main():
    arg = [line.strip() for line in fileinput.input()]
    ts = int(arg[0])
    ids = [int(x) for x in arg[1].split(',') if x != 'x']

    # 7m22s.
    print(part1(ts, ids))

    i_ids = [(idx, int(x))
             for idx, x in enumerate(arg[1].split(',')) if x != 'x']
    # +Inf.
    print(part2(i_ids))


if __name__ == '__main__':
    main()
