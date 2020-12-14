import fileinput
import re
from collections import defaultdict


def apply_mask(mask, n):
    res = int(n)
    for i, char in enumerate(reversed(mask)):
        if char == '1':
            res |= (1 << i)
        elif char == '0':
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


def combinations(part):
    if not part:
        return ['']

    if part[0] != 'X':
        return [
            part[0] + c for c in combinations(part[1:])
        ]
    else:
        return [
            prefix + comb
            for prefix in '01'
            for comb in combinations(part[1:])
        ]


def addresses(mask, addr_in):
    addr = list(reversed(format(int(addr_in), '#038b')[2:]))
    res = ''
    for i, char in enumerate(reversed(mask)):
        if char == '1':
            res += '1'
        elif char == '0':
            res += addr[i]
        else:
            res += 'X'

    res = list(reversed(res))
    print('res', res)

    return combinations(res)


def part2(arg):
    mem = defaultdict(int)
    mask = 0
    for cmd, arg1, arg2 in arg:
        if cmd == 'mask':
            mask = arg1
        elif cmd == 'mem':
            for addr in addresses(mask, arg1):
                mem[addr] = int(arg2)

    print(mem.values())
    return sum(mem.values())


mem_patt = re.compile('mem\[(\d+)] = (\d+)')


def parse(line):
    if line.startswith('mask'):
        return ('mask', line.split()[-1], 0)
    else:
        m = re.match(mem_patt, line)
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
