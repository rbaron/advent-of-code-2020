import fileinput
import functools
import re
from collections import defaultdict

MEM_PATT = re.compile('mem\[(\d+)] = (\d+)')


def apply_mask(mask, n):
    res = int(n)
    for i in range(len(mask)):
        pos = len(mask) - 1 - i
        if mask[pos] == '1':
            res |= (1 << i)
        elif mask[pos ]== '0':
            res &= ~(1 << i)
    return res


def part1(arg):
    mem = defaultdict(int)
    mask = 0
    for cmd, arg1, arg2 in arg:
        if cmd == 'mask':
            mask = arg1
        elif cmd == 'mem':
            mem[arg1] = apply_mask(mask, arg2)
    return sum(mem.values())


@functools.lru_cache(maxsize=None)
def combinations(part):
    if not part:
        return ['']

    if part[0] != 'X':
        return [part[0] + c for c in combinations(part[1:])]
    else:
        return [prefix + comb
                for prefix in '01'
                for comb in combinations(part[1:])
                ]


def addresses(mask, addr_in):
    '''Returns a list of addresses given a mask and a base address.'''
    # Convert address from base 10 to base 2. Strip the leading '0b'.
    addr = format(int(addr_in), '#038b')[2:]
    res = (
        a if m == '0' else m
        for a, m in zip(addr, mask)
    )
    # Convers to tuple so it's hashable and cacheable.
    return combinations(tuple(res))


def part2(arg):
    mem = defaultdict(int)
    mask = 0
    for cmd, arg1, arg2 in arg:
        if cmd == 'mask':
            mask = arg1
        elif cmd == 'mem':
            for addr in addresses(mask, arg1):
                mem[addr] = int(arg2)
    return sum(mem.values())


def parse(line):
    if line.startswith('mask'):
        return ('mask', line.split()[-1], 0)
    else:
        m = re.match(MEM_PATT, line)
        return ('mem', m.group(1), m.group(2))


def main():
    arg = [parse(line.strip()) for line in fileinput.input()]
    # 14m28s.
    print(part1(arg))
    # +Inf. This solution works on the real input but it's too slow
    # for the test input. The test mask has a lot of 'X's, which causes
    # the recursive combinations() to do too much work.
    print(part2(arg))


if __name__ == '__main__':
    main()
