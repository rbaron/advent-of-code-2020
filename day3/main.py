import argparse
from math import prod


def positions(chart, current, slope):
    while current[0] < len(chart):
        yield current
        current = (current[0] + slope[0],
                   (current[1] + slope[1]) % len(chart[0]))


def part1(arg):
    return sum(
        arg[pos[0]][pos[1]] == '#'
        for pos in positions(arg, (0, 0), (1, 3))
    )


def part2(arg):
    return prod(
        sum(arg[pos[0]][pos[1]] == '#'
            for pos in positions(arg, (0, 0), slope))
        for slope in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test', action='store_true')
    args = ap.parse_args()

    with open('test-input.txt' if args.test else 'input.txt', 'r') as f:
        arg = f.read().split('\n')

    print(part1(arg))
    print(part2(arg))


if __name__ == '__main__':
    main()
