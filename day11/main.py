import fileinput
import copy

DIRECTIONS = (
    (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
)


def cells(table):
    return (cell for row in table for cell in row)


def get_neighbors_part1(table, y, x):
    return (
        (y + dy, x + dx)
        for dy, dx in DIRECTIONS
        if 0 <= y + dy < len(table) and 0 <= x + dx < len(table[0]) and table[y][x] != '.'
    )


def get_neighbors_part2(table, y, x):
    for direction in DIRECTIONS:
        step = 1
        ny = y + step * direction[0]
        nx = x + step * direction[1]
        while 0 <= ny < len(table) and 0 <= nx < len(table[0]):
            if table[ny][nx] != '.':
                yield (ny, nx)
                break
            step += 1
            ny = y + step * direction[0]
            nx = x + step * direction[1]


def run(table, get_neighbors_fn, min_occupied_neighbors):
    def evolve(cell, y, x):
        occ_neighbors = sum(
            table[ny][nx] == '#' for ny, nx in get_neighbors_part1(table, y, x))
        if table[y][x] == 'L' and occ_neighbors == 0:
            return '#'
        elif table[y][x] == '#' and occ_neighbors >= min_occupied_neighbors:
            return 'L'
        else:
            return cell

    def run_one(current_table):
        new_table = copy.deepcopy(current_table)
        for y in range(len(table)):
            for x in range(len(table[0])):
                new_table[y][x] = evolve(current_table[y][x], y, x)
        return new_table

    n_occ = sum(cell == '#' for cell in cells(table))
    while True:
        table = run_one(table)
        new_occ = sum(cell == '#' for cell in cells(table))
        if new_occ == n_occ:
            return new_occ
        n_occ = new_occ


def part1(table):
    return run(table, get_neighbors_part1, 4)


def part2(table):
    return run(table, get_neighbors_part2, 5)


def main():
    arg = [list(line.strip()) for line in fileinput.input()]

    print(part1(arg))
    print(part2(arg))


if __name__ == '__main__':
    main()
