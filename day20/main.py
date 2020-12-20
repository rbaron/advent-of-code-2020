import copy
import fileinput
import itertools

from collections import defaultdict
from math import prod, sqrt


# def cannonical_border(border):
#     yield sorted([seq, ''.join(reversed(seq))])[0]


def borders(rows):
    cols = [''.join(c) for c in zip(*rows)]
    for seq in (rows[0], cols[-1], rows[-1], cols[0]):
        # Yield the "cannonical" representation of a border: the
        # lexicographic first one among its possible orientations.
        yield sorted([seq, ''.join(reversed(seq))])[0]


def get_corners(tiles_by_id):
    tiles_by_border = defaultdict(list)
    for tile_id, rows in tiles_by_id.items():
        for border in borders(rows):
            tiles_by_border[border].append(tile_id)

    n_borders_by_tile_id = defaultdict(int)
    for border, tile_ids in tiles_by_border.items():
        if len(tile_ids) > 1:
            continue
        for tile_id in tile_ids:
            n_borders_by_tile_id[tile_id] += 1

    return (
        tile_id
        for tile_id, n_borders in n_borders_by_tile_id.items()
        if n_borders == 2)


def part1(tiles_by_id):
    return prod(get_corners(tiles_by_id))


def flips(rows):
    yield rows
    yield list(reversed(rows))
    yield [''.join(reversed(r)) for r in rows]


def rotate(rows):
    return [''.join(r) for r in zip(*reversed(rows))]


def orientations(rows):
    rotated = copy.deepcopy(rows)
    for i in range(4):
        rotated = rotate(rotated)
        yield from flips(rotated)


# def find_orientation(row, edges_in_positions, n_borders_by_tile_id)


def solve(tiles_by_id):
    w = h = int(sqrt(len(tiles_by_id)))

    # def is_corner(r, c):
    #     return (r, c) in [(0, 0), (0, w-1), (h-1, 0), (h-1, w-1)]

    unordered_corners = get_corners(tiles_by_id)
    for c1, c2, c3, c4 in itertools.permutations(unordered_corners):
        grid = [[None] * w for _ in range(h)]
        grid[0][0] = c1
        grid[0][h - 1] = c2
        grid[w - 1][0] = c3
        grid[w - 1][h - 1] = c4
        # for r in range(h):
        #     for c in range(w):
        #         # If this is a corner, continue.
        #         if grid[r][c] is not None:
        #             continue

        #         # Find edge.
        #         edge =
        # return grid


def part2(tiles_by_id):
    tiles_by_border = defaultdict(list)
    for tile_id, rows in tiles_by_id.items():
        for border in borders(rows):
            tiles_by_border[border].append(tile_id)

    c1, c2, c3, c4 = get_corners(tiles_by_id)
    w = h = int(sqrt(len(tiles_by_id)))
    grid = [[None] * w for _ in range(h)]
    grid[0][0] = c1
    grid[0][h - 1] = c2
    grid[w - 1][0] = c3
    print(grid)
    # for c in range(1, width - 1):
    #     pass


def main():
    def parse_tile(lines):
        lines = lines.split('\n')
        tile_id = int(lines[0].split()[1][:-1])
        rows = lines[1:]
        return tile_id, rows

    tiles_by_id = dict(parse_tile(lines)
                       for lines in ''.join(fileinput.input()).split('\n\n'))

    # print(tiles_by_id)
    tiles = list(tiles_by_id.values())
    print('\n'.join(tiles[0]))
    # for border in borders(tiles[0]):
    #     print('b ', border)
    # for rows in flips(['abc', 'def', 'ghi']):
    #     print('flipped:')
    #     print(rows)
    t = ['ab', 'cd']
    print(t)
    # for r in range(4):
    #     t = rotate(t)
    #     print('rotated')
    #     print('\n'.join(t))
    for o in orientations(t):
        print('ori')
        print('\n'.join(o))


    print(part1(tiles_by_id))
    # print(part2(tiles_by_id))


if __name__ == '__main__':
    main()
