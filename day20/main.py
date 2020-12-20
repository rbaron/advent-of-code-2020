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


# def flips(rows):
#     yield rows
#     yield list(reversed(rows))
#     # yield [''.join(reversed(r)) for r in rows]


def rotate(rows):
    return [''.join(r) for r in zip(*reversed(rows))]


def orientations(rows):
    rotated = copy.deepcopy(rows)
    for i in range(4):
        yield rotated
        yield list(reversed(rotated))
        rotated = rotate(rotated)
        # yield from flips(rotated)


def find_orientation(rows, predicate):
    for possible_rows in orientations(rows):
        if predicate(possible_rows):
            return possible_rows
    raise RuntimeError('Unable to find orientation matching predicate')


def try_to_solve_for_corners(tiles_by_id, c1r, c2r, c3r, c4r, used):
    # print('used', used)
    w = h = int(sqrt(len(tiles_by_id)))
    tiles_by_border = get_tiles_by_border(tiles_by_id)

    grid = [[None] * w for _ in range(h)]
    grid[0][0] = c1r
    grid[0][w-1] = c2r
    grid[h-1][0] = c3r
    grid[h-1][w-1] = c4r

    for r in range(h):
        for c in range(w):
            # If this is a corner, continue.
            if grid[r][c] is not None:
                continue

            # Find the edge we need to match.
            if c == 0:
                edge = bottom_border(grid[r-1][0])
                # Find the node whose top row matches the bottom row of the upper node.
                # Careful not to reuse!
                candidate_ids = tiles_by_border[cannonical_border(edge)]
                chosen = None
                for candidate_id in candidate_ids:
                    if candidate_id in used:
                        continue
                    try:
                        chosen = find_orientation(
                            tiles_by_id[candidate_id], lambda rows: top_border(rows) == edge)
                    except RuntimeError:
                        continue
                    grid[r][c] = chosen
                    used.add(candidate_id)
                if chosen is None:
                    raise RuntimeError(
                        'None of the unused candidates had suitable orientations!')
            elif r == 0:
                edge = right_border(grid[r][c - 1])
                # Find the node whose top row matches the bottom row of the upper node.
                # Careful not to reuse!
                candidate_ids = tiles_by_border[cannonical_border(edge)]
                chosen = None
                for candidate_id in candidate_ids:
                    if candidate_id in used:
                        continue
                    try:
                        chosen = find_orientation(
                            tiles_by_id[candidate_id], lambda rows: left_border(rows) == edge)
                    except RuntimeError as e:
                        continue
                    grid[r][c] = chosen
                    used.add(candidate_id)
                if chosen is None:
                    raise RuntimeError(
                        'None of the unused candidates had suitable orientations!')
            else:
                l_edge = right_border(grid[r][c - 1])
                t_edge = bottom_border(grid[r - 1][c])
                # Find the node whose top row matches the bottom row of the upper node.
                # Careful not to reuse!
                candidate_ids = tiles_by_border[cannonical_border(l_edge)]
                chosen = None
                for candidate_id in candidate_ids:
                    if candidate_id in used:
                        continue
                    try:
                        chosen = find_orientation(
                            tiles_by_id[candidate_id], lambda rows: left_border(rows) == l_edge and top_border(rows) == t_edge)
                    except RuntimeError as e:
                        continue
                    grid[r][c] = chosen
                    used.add(candidate_id)
                if chosen is None:
                    raise RuntimeError(
                        'None of the unused candidates had suitable orientations!')

    # Missing checks
    if left_border(c2r) != right_border(grid[0][1]):
        raise RuntimeError
    if top_border(c3r) != bottom_border(grid[1][0]):
        raise RuntimeError
    if top_border(c4r) != bottom_border(grid[h-2][w-1]):
        raise RuntimeError
    if left_border(c4r) != right_border(grid[h-1][w-2]):
        raise RuntimeError

    assert(len(used) == len(tiles_by_id))
    return grid


def pretty_print_grid(grid):
    w = len(grid)
    for row in grid:
        for line_n in range(len(row[0][0])):
                print(' '.join([tile[line_n] for tile in row]))
        print()


def solve(tiles_by_id):
    unordered_corners = get_corners(tiles_by_id)
    grid = None
    tiles_by_border = get_tiles_by_border(tiles_by_id)
    for c1, c2, c3, c4 in itertools.permutations(unordered_corners):
        # Each corner can also have different orientations
        for c1r, c2r, c3r, c4r in itertools.product(
            [o for o in orientations(tiles_by_id[c1]) if len(tiles_by_border[cannonical_border(
                top_border(o))]) == 1 and len(tiles_by_border[cannonical_border(left_border(o))]) == 1],
            [o for o in orientations(tiles_by_id[c2]) if len(tiles_by_border[cannonical_border(
                top_border(o))]) == 1 and len(tiles_by_border[cannonical_border(right_border(o))]) == 1],
            [o for o in orientations(tiles_by_id[c3]) if len(tiles_by_border[cannonical_border(
                left_border(o))]) == 1 and len(tiles_by_border[cannonical_border(bottom_border(o))]) == 1],
            [o for o in orientations(tiles_by_id[c4]) if len(tiles_by_border[cannonical_border(
                right_border(o))]) == 1 and len(tiles_by_border[cannonical_border(bottom_border(o))]) == 1],
        ):
            used = {c1, c2, c3, c4}
            try:
                grid = try_to_solve_for_corners(
                    tiles_by_id, c1r, c2r, c3r, c4r, used)
                print('found grid: ')
                print('using c1', c1)
                # print('\n'.join(grid[0][0]))
                pretty_print_grid(grid)

            except RuntimeError as e:
                # print('oh no!')
                continue

    # if grid is not None:
    #     print('Found a grid!!')
    # else:
    #     print('Unable to find grid')

    # return grid


def part2(tiles_by_id):
    tiles_by_border = defaultdict(list)
    for tile_id, rows in tiles_by_id.items():
        for border in cannonical_borders(rows):
            tiles_by_border[border].append(tile_id)

    grid = solve(tiles_by_id)

    if not grid:
        print('Unable to find grid')
        return

    print(grid)

    for row in grid:
        for tile in row:
            print('\n'.join(tile))
            print()


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
    # print('\n'.join(tiles[0]))
    # for border in borders(tiles[0]):
    #     print('b ', border)
    # for rows in flips(['abc', 'def', 'ghi']):
    #     print('flipped:')
    #     print(rows)
    # t = ['abc', 'def', 'ghi']
    # for o in orientations(t):
    #     print('\n')
    #     print('\n'.join(o))
    # print(t)
    # for r in range(4):
    #     t = rotate(t)
    #     print('rotated')
    #     print('\n'.join(t))
    # t = tiles_by_id[1951]
    # for o in orientations(t):
    #     print('ori')
    #     print('\n'.join(o))

    # print(part1(tiles_by_id))
    print(part2(tiles_by_id))

    tiles_by_border = get_tiles_by_border(tiles_by_id)
    # b = '#...##.#..'
    # print('cano:', cannonical_border(b))
    # print(tiles_by_border[b])
    # t = tiles_by_id[1951]
    # for o in orientations(t):
    #     print('\n')
    #     print('\n'.join(o))
    # tt = '''#...##.#..
    #     ..#.#..#.#
    #     .###....#.
    #     ###.##.##.
    #     .###.#####
    #     .##.#....#
    #     #...######
    #     .....#..##
    #     #.####...#
    #     #.##...##.'''
    # t = [e.strip() for e in tt.split('\n')]
    # for o in orientations(t):
    #     tb = top_border(t)
    #     lb = left_border(t)
    #     if len(tiles_by_border[cannonical_border(top_border(o))]) == 1 and len(tiles_by_border[cannonical_border(left_border(o))]) == 1:
    #         print('top: ', tiles_by_border[cannonical_border(tb)])
    #         print('left: ', tiles_by_border[cannonical_border(lb)])
    #         print('found')
    #         print('\n'.join(o))
    #         print()


if __name__ == '__main__':
    main()
