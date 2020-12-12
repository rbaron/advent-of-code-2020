import fileinput
import re
import math


def next_dir(current, right_amount):
    DIRS = list('NESW')
    steps = right_amount // 90
    idx = DIRS.index(current)
    nxt = DIRS[(idx + steps) % 4]
    return nxt


def part1(cmds):
    east = 0
    north = 0
    direction = 'E'
    for d, amount in cmds:
        if d == 'E':
            east += amount
        if d == 'W':
            east -= amount
        if d == 'N':
            north += amount
        if d == 'S':
            north -= amount
        if d == 'R':
            direction = next_dir(direction, amount)
        if d == 'L':
            direction = next_dir(direction, 360 - amount)
        if d == 'F':
            if direction == 'N':
                north += amount
            if direction == 'S':
                north -= amount
            if direction == 'E':
                east += amount
            if direction == 'W':
                east -= amount
    return abs(east) + abs(north)


def rotate(n, e, cw_amount):
    hyp = math.sqrt(e ** 2 + n ** 2)
    angle = math.atan2(n, e)
    new_angle = angle + math.radians(cw_amount)
    return round(math.sin(new_angle) * hyp), round(math.cos(new_angle) * hyp)


def part2(cmds):
    east = 0
    north = 0
    direction = 'E'
    wp_e = 10
    wp_n = 1
    for d, amount in cmds:
        if d == 'E':
            wp_e += amount
        if d == 'W':
            wp_e -= amount
        if d == 'N':
            wp_n += amount
        if d == 'S':
            wp_n -= amount
        if d == 'R':
            wp_n, wp_e = rotate(wp_n, wp_e, 360 - amount)
        if d == 'L':
            wp_n, wp_e = rotate(wp_n, wp_e, amount)
        if d == 'F':
            north += wp_n * amount
            east += wp_e * amount
    return abs(east) + abs(north)


def main():
    arg = [line.strip() for line in fileinput.input()]
    cmds = [(line[0], int(line[1:])) for line in arg]

    # 11m06s.
    print(part1(cmds))
    # 15m42s.
    print(part2(cmds))


if __name__ == '__main__':
    main()
