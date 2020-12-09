import fileinput


def part1(arg):
    def valid(target, prev):
        for n in prev:
            if (target - n) in prev and (target - n) != target:
                return True
        return False

    # preamble_len = 5
    preamble_len = 25
    for i in range(preamble_len, len(arg)):
        prev = set(arg[(i-preamble_len):i])
        target = arg[i]
        if not valid(target, prev):
            return target


def part2(arg):
    # target = 127
    target = 530627549
    for i in range(len(arg) - 1):
        s = arg[i]
        for j in range(i + 1, len(arg)):
            s += arg[j]
            if s == target:
                return max(arg[i:j]) + min(arg[i:j])
            elif s > target:
                break


def main():
    arg = [int(line.strip()) for line in fileinput.input()]
    # 12m33s
    print(part1(arg))
    # 12m33s
    print(part2(arg))


if __name__ == '__main__':
    main()
