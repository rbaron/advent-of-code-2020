import fileinput
import copy


def neighbors(y, x, table):
    return [
        (y + ny, x + nx)
        for ny, nx in [
            (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        ]
        if 0 <= y + ny < len(table) and 0 <= x + nx < len(table[0])
    ]


def deep_eq(t1, t2):
    return all(
        t1[y][x] == t2[y][x]
        for y in range(len(t1))
        for x in range(len(t1[0]))
    )


def part1(arg):
    def run_one(current_table):
        new_table = copy.deepcopy(current_table)
        for y in range(len(table)):
            for x in range(len(table[0])):
                occ_neighbors = sum(
                    table[ny][nx] == '#' for ny, nx in neighbors(y, x, table))
                if table[y][x] == 'L' and occ_neighbors == 0:
                    new_table[y][x] = '#'
                elif table[y][x] == '#' and occ_neighbors >= 4:
                    new_table[y][x] = 'L'
        return new_table

    table = copy.deepcopy(arg)
    while True:
        new_table = run_one(table)
        if deep_eq(table, new_table):
            return sum(
                table[y][x] == '#'
                for y in range(len(table))
                for x in range(len(table[0]))
            )
        table = new_table


def neighbors2(y, x, table):
    directions = [
        (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
    ]
    total = 0
    for direction in directions:
        ny = y + direction[0]
        nx = x + direction[1]
        while 0 <= ny < len(table) and 0 <= nx < len(table[0]):
            if table[ny][nx] == '#':
                total += 1
                break
            elif table[ny][nx] == 'L':
                break
            ny = ny + direction[0]
            nx = nx + direction[1]
    return total


def part2(arg):
    def run_one(current_table):
        new_table = copy.deepcopy(current_table)
        for y in range(len(current_table)):
            for x in range(len(current_table[0])):
                occ_neighbors = neighbors2(y, x, current_table)
                if current_table[y][x] == 'L' and occ_neighbors == 0:
                    new_table[y][x] = '#'
                elif current_table[y][x] == '#' and occ_neighbors >= 5:
                    new_table[y][x] = 'L'
        return new_table

    table = copy.deepcopy(arg)
    while True:
        new_table = run_one(table)
        print('Ran')
        for r in new_table:
            print(''.join(r))
        if deep_eq(table, new_table):
            return sum(
                new_table[y][x] == '#'
                for y in range(len(table))
                for x in range(len(table[0]))
            )
        table = new_table


def main():
    arg = [list(line.strip()) for line in fileinput.input()]

    # print(part1(arg))
    print(part2(arg))


if __name__ == '__main__':
    main()
