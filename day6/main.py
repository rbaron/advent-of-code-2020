import fileinput


def part1(arg):
    pass


def part2(arg):
    pass


def main():
    arg = [line.strip() for line in fileinput.input()]

    # 5m57s
    # Part 1
    total = 0
    s = set()
    for line in arg:
        if line == '':
            total += len(s)
            s = set()
        for c in line:
            s.add(c)
    total += len(s)
    s = set()
    print(total)

    # 5m34s
    # Part 2
    total = 0
    begin = True
    s = set()
    for line in arg:
        if begin:
            s = set(line)
            begin = False
            continue
        if line == '':
            total += len(s)
            begin = True
        s = s & set(line)
    total += len(s)
    print(total)

    print(part1(arg))
    print(part2(arg))


if __name__ == '__main__':
    main()
