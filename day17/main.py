import copy
import fileinput
import itertools
import operator

from collections import defaultdict


def add(coord, delta):
    return tuple(map(operator.add, coord, delta))


def neighbors(coord):
    dim = len(coord)
    deltas = itertools.product((1, 0, -1), repeat=dim)
    return (
        add(coord, delta)
        for delta in deltas if delta != tuple(0 for _ in range(dim))
    )


def count_alive(cube):
    return sum(cube.values())


def evolve_one(cube, coord):
    n_alive = sum(cube[n] for n in neighbors(coord))
    if cube[coord]:
        return 2 <= n_alive <= 3
    else:
        return n_alive == 3


def evolve(cube):
    new_cube = defaultdict(bool)
    all_coords = {
        n for coord in cube for n in neighbors(coord)
    }
    for coord in all_coords:
        new_cube[coord] = evolve_one(cube, coord)
    return new_cube


def run(cube):
    for i in range(6):
        cube = evolve(cube)
    return count_alive(cube)


def part1(arg):
    cube = defaultdict(bool)
    for y, line in enumerate(arg):
        for x, c in enumerate(line):
            cube[(x, y, 0)] = c == '#'
    return run(cube)


def part2(arg):
    cube = defaultdict(bool)
    for y, line in enumerate(arg):
        for x, c in enumerate(line):
            cube[(x, y, 0, 0)] = c == '#'
    return run(cube)


def main():
    arg = [line.strip() for line in fileinput.input()]

    print(part1(arg))
    print(part2(arg))


if __name__ == '__main__':
    main()
