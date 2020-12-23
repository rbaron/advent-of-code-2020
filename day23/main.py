import fileinput


def add(idx, i, l):
    return (idx + i) % l


def move(curr_idx, cups):
    print('cups: ', cups, 'current: ', cups[curr_idx])
    curr = cups[curr_idx]
    removed = [
        cups[add(curr_idx, i + 1, 9)]
        for i in range(3)
    ]
    print('picked up', removed)
    cups = [
        c for c in cups
        if c not in removed
    ]
    # print('new cups', cups)

    dest = add(curr, -1, 10)
    print('dest: ', dest)
    # while dest in removed:
    while dest not in cups:
        dest = add(dest, -1, 10)
        print('dest: ', dest)
    print('destination', dest)

    for i, r in enumerate(removed):
        dest_idx = cups.index(dest)
        new_idx = add(dest_idx, i + 1, len(cups))
        print(f'will insert {r} in {new_idx} of {cups}')
        # cups = cups[:i] + [r] + cups[i:]
        cups.insert(new_idx, r)

    old_curr_idx = cups.index(curr)
    new_idx = add(old_curr_idx, 1, 9)
    return new_idx, cups


def part1(cups):
    curr_idx = 0
    for i in range(1, 101):
        print(f'-- move {i} --')
        curr_idx, cups = move(curr_idx, cups)
        print()

    print('final: ', cups, f'({cups[curr_idx]})')
    idx = (cups.index(1) + 1) % 9
    res = ''
    while len(res) != 8:
        res += str(cups[idx])
        idx = (idx + 1) % 9
    return res


def part2(cups):
    pass


def main():
    # cups = list(map(int, ('389125467')))
    cups = list(map(int, ('712643589')))

    print(part1(cups))
    # print(part2(cups))


if __name__ == '__main__':
    main()
