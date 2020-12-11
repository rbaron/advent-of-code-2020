import fileinput
import itertools
from collections import Counter


def part1(arg):
    adapters = sorted(arg + [0, max(arg) + 3])
    diffs = [a - b for a, b in zip(adapters[1:], adapters[:-1])]
    counts = Counter(diffs)
    return counts[1] * counts[3]


def part2(arg):
    '''DFS solution. Too slow for non-test inputs.'''
    builtin = max(arg) + 3
    adapters = sorted(arg + [0, builtin])

    def next_adapters(i):
        return itertools.takewhile(
            lambda j: adapters[j] <= adapters[i] + 3,
            range(i + 1, len(adapters)))

    def combinations(i):
        if adapters[i] == builtin:
            return 1
        return sum(combinations(j) for j in next_adapters(i))

    return combinations(0)


def part2_dp(arg):
    '''Dynamic programming solution. *Chef's kiss*.'''
    adapters = sorted(arg + [0, max(arg) + 3])
    solutions = [0 for _ in adapters]
    solutions[0] = 1

    def neighbors(i):
        return itertools.takewhile(
            lambda j: adapters[j] >= adapters[i] - 3,
            range(i - 1, -1, -1))

    for i in range(1, len(adapters)):
        solutions[i] = sum(solutions[n] for n in neighbors(i))

    return solutions[-1]


def main():
    arg = [int(line.strip()) for line in fileinput.input()]

    # 9m21s.
    print(part1(arg))
    # +Inf.
    # print(part2(arg))
    # +Inf.
    print(part2_dp(arg))


if __name__ == '__main__':
    main()
