from collections import defaultdict


def run_until(arg, nth_number):
    last_spoken = defaultdict(int)
    for i, n in enumerate(arg):
        last_spoken[n] = i
    del last_spoken[n]
    for i in range(i, nth_number - 1):
        if n not in last_spoken:
            last_spoken[n] = i
            n = 0
        else:
            old = last_spoken[n]
            last_spoken[n] = i
            n = i - old
    return n


def part1(arg):
    return run_until(arg, 2020)


def part2(arg):
    return run_until(arg, 30000000)


def main():
    # arg = [0,3,6]
    arg = [1, 2, 16, 19, 18, 0]

    print(part1(arg))
    # Runs in about 15s.
    print(part2(arg))


if __name__ == '__main__':
    main()
