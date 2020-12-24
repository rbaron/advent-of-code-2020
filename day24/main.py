import fileinput
import re

from collections import defaultdict

DIR_PATT = r'e|se|sw|w|nw|ne'


def add_coords(c1, c2):
    return tuple(a + b for a, b in zip(c1, c2))


COORD_DELTA_BY_DIRECTION = {
    'ne': (1, 0, -1),
    'e': (1, -1, 0),
    'se': (0, -1, 1),
    'sw': (-1, 0, 1),
    'w': (-1, 1, 0),
    'nw': (0, 1, -1),
}

def part1(paths):
    counts_by_coord = defaultdict(int)
    for path in paths:
        pos = (0, 0, 0)
        for d in path:
            pos = add_coords(pos, COORD_DELTA_BY_DIRECTION[d])
        counts_by_coord[pos] += 1

    return sum(1 for _, counts in counts_by_coord.items() if counts % 2 == 1)


def part2(paths):
    pass


def main():
    def parse_line(line):
        return re.findall(DIR_PATT, line)

    paths = [parse_line(l) for l in fileinput.input()]
    # paths = [parse_line('')]

    print(part1(paths))
    # print(part2(paths))


if __name__ == '__main__':
    main()
