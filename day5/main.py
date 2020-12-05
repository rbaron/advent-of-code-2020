import fileinput
from collections import defaultdict


def seat_id(arg):
    row_i = col_i = 0
    row_j = 128
    col_j = 8

    for rh in arg:
        if rh == 'F':
            row_j = (row_i + row_j) / 2
        elif rh == 'B':
            row_i = (row_i + row_j) / 2
        elif rh == 'L':
            col_j = (col_i + col_j) / 2
        elif rh == 'R':
            col_i = (col_i + col_j) / 2

    return row_i * 8 + col_i


def part1(arg):
    return max(map(seat_id, arg))


def part2(args):
    all_ids = set(map(seat_id, args))
    for r in range(128):
        for c in range(8):
            if (r * 8 + c) not in all_ids:
                print(r, c, r * 8 + c)


def main():
    arg = [line.strip() for line in fileinput.input()]

    # 9m12s
    print(part1(arg))
    # 18m03s
    print(part2(arg))


if __name__ == '__main__':
    main()
