import fileinput
import re

from collections import defaultdict
from copy import deepcopy


DIR_PATT = r'e|se|sw|w|nw|ne'


COORD_DELTA_BY_DIRECTION = {
    'ne': (1, 0, -1),
    'e': (1, -1, 0),
    'se': (0, -1, 1),
    'sw': (-1, 0, 1),
    'w': (-1, 1, 0),
    'nw': (0, 1, -1),
}


def add_coords(c1, c2):
    return tuple(a + b for a, b in zip(c1, c2))


def get_counts_by_coord(paths):
    '''Returns how many tiles a given coordinated has been identified.'''
    counts_by_coord = defaultdict(int)
    for path in paths:
        pos = (0, 0, 0)
        for d in path:
            pos = add_coords(pos, COORD_DELTA_BY_DIRECTION[d])
        counts_by_coord[pos] += 1
    return counts_by_coord


def count_black_tiles(counts_by_coord):
    return sum(1 for _, counts in counts_by_coord.items() if counts % 2 == 1)


def part1(paths):
    return count_black_tiles(get_counts_by_coord(paths))


def neighbors(coord):
    for direction in COORD_DELTA_BY_DIRECTION.values():
        yield add_coords(coord, direction)


def evolve(counts_by_coord):
    new_counts = deepcopy(counts_by_coord)

    all_coords = set()
    for c in counts_by_coord:
        all_coords.add(c)
        all_coords |= set(neighbors(c))

    for c in all_coords:
        black_adjacent = sum(1 for n in neighbors(
            c) if counts_by_coord.get(n, 0) % 2 == 1)
        if counts_by_coord.get(c, 0) % 2 == 1:
            if black_adjacent == 0 or black_adjacent > 2:
                new_counts[c] = 0
        else:
            if black_adjacent == 2:
                new_counts[c] = 1
    return new_counts


def part2(paths):
    counts_by_coord = dict(get_counts_by_coord(paths))
    for i in range(100):
        counts_by_coord = evolve(counts_by_coord)
    return count_black_tiles(counts_by_coord)


def main():
    def parse_line(line):
        return re.findall(DIR_PATT, line)

    paths = [parse_line(l) for l in fileinput.input()]

    print(part1(paths))
    print(part2(paths))


if __name__ == '__main__':
    main()
