import copy
import fileinput
import itertools

from collections import defaultdict
from math import prod, sqrt


def cannonical_border(border):
    '''Yields the "cannonical" representation of a border: the
    lexicographic first one among its possible orientations'''
    return sorted([border, ''.join(reversed(border))])[0]


def top_border(rows):
    return rows[0]


def bottom_border(rows):
    return rows[-1]


def left_border(rows):
    cols = [''.join(c) for c in zip(*rows)]
    return cols[0]


def right_border(rows):
    cols = [''.join(c) for c in zip(*rows)]
    return cols[-1]


def cannonical_borders(rows):
    cols = [''.join(c) for c in zip(*rows)]
    # for border in (rows[0], cols[-1], rows[-1], cols[0]):
    for border in (top_border(rows), bottom_border(rows), left_border(rows), right_border(rows)):
        yield cannonical_border(border)


def get_tiles_by_border(tiles_by_id):
    tiles_by_border = defaultdict(list)
    for tile_id, rows in tiles_by_id.items():
        for border in cannonical_borders(rows):
            tiles_by_border[border].append(tile_id)
    return tiles_by_border


def get_corners(tiles_by_id):
    tiles_by_border = get_tiles_by_border(tiles_by_id)

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


def cannonical_borders(rows):
    cols = [''.join(c) for c in zip(*rows)]
    for border in (rows[0], cols[-1], rows[-1], cols[0]):
        yield cannonical_border(border)


def flips(rows):
    yield rows
    yield list(reversed(rows))


def rotate(rows):
    return [''.join(r) for r in zip(*reversed(rows))]


def orientations(rows):
    rotated = copy.deepcopy(rows)
    for i in range(4):
        yield from flips(rotated)
        rotated = rotate(rotated)


def find_orientation(rows, predicate):
    for possible_rows in orientations(rows):
        if predicate(possible_rows):
            return possible_rows


def pretty_print_grid(grid):
    w = len(grid)
    for row in grid:
        for line_n in range(len(row[0][0])):
            print(' '.join([tile[line_n] for tile in row]))
        print()


def join_grid(grid):
    w = len(grid)
    out = []
    for row in grid:
        for line_n in range(len(row[0][0])):
            out.append(''.join([tile[line_n] for tile in row]))
    return out


def solve(tiles_by_id):
    corner1 = next(get_corners(tiles_by_id))
    tiles_by_border = get_tiles_by_border(tiles_by_id)
    c1 = find_orientation(
        tiles_by_id[corner1], lambda rows: len(tiles_by_border[cannonical_border(top_border(rows))]) == 1 and
        len(tiles_by_border[cannonical_border(left_border(rows))]) == 1)

    w = h = int(sqrt(len(tiles_by_id)))
    grid = [[None] * w for _ in range(h)]
    grid[0][0] = c1
    available = set(tiles_by_id.keys())
    available.remove(corner1)

    for r in range(h):
        for c in range(w):
            # If this is a corner, continue.
            if grid[r][c] is not None:
                continue

            if c == 0:
                edge = bottom_border(grid[r-1][0])
                for tile_id in available:
                    orientation = find_orientation(
                        tiles_by_id[tile_id], lambda rows: top_border(rows) == edge)
                    if orientation:
                        grid[r][c] = orientation
                        available.remove(tile_id)
                        break
            else:
                edge = right_border(grid[r][c - 1])
                for tile_id in available:
                    orientation = find_orientation(
                        tiles_by_id[tile_id], lambda rows: left_border(rows) == edge)
                    if orientation:
                        grid[r][c] = orientation
                        available.remove(tile_id)
                        break
    return grid


MONSTER_PATTERN = \
    '''                  #
#    ##    ##    ###
 #  #  #  #  #  #   '''


def find_patterns(image):
    deltas = [
        (delta_r, delta_c)
        for delta_r, row in enumerate(MONSTER_PATTERN.split('\n'))
        for delta_c, char in enumerate(row)
        if char == '#'
    ]

    def matches_char(coord):
        r, c = coord
        if r >= len(image) or c >= len(image[0]):
            return False
        return image[r][c] == '#'

    counts = 0
    for r in range(len(image)):
        for c in range(len(image[0])):
            if all(
                matches_char((r + delta[0], c + delta[1]))
                for delta in deltas
            ):
                counts += 1
    return counts


def part2(tiles_by_id):
    tiles_by_border = defaultdict(list)
    for tile_id, rows in tiles_by_id.items():
        for border in cannonical_borders(rows):
            tiles_by_border[border].append(tile_id)

    grid = solve(tiles_by_id)

    tile_size = len(grid[0][0])

    def strip_tile(tile):
        return [
            row[1:tile_size-1]
            for row in tile[1:tile_size-1]
        ]

    stripped = [
        [strip_tile(tile) for tile in row]
        for row in grid
    ]

    image = join_grid(stripped)

    for orientation in orientations(image):
        if n := find_patterns(orientation):
            monster = n * sum(c == '#' for c in MONSTER_PATTERN)
            nonmonster = sum(
                c == '#' for row in orientation for c in row) - monster
            return nonmonster


def main():
    def parse_tile(lines):
        lines = lines.split('\n')
        tile_id = int(lines[0].split()[1][:-1])
        rows = lines[1:]
        return tile_id, rows

    tiles_by_id = dict(parse_tile(lines)
                       for lines in ''.join(fileinput.input()).split('\n\n'))

    print(part1(tiles_by_id))
    print(part2(tiles_by_id))


if __name__ == '__main__':
    main()
