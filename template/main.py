import argparse


def part1(arg):
    pass


def part2(arg):
    pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test', action='store_true')
    args = ap.parse_args()

    with open('test-input.txt' if args.test else 'input.txt', 'r') as f:
        arg = f.read().split('\n')

    print(part1(arg))
    print(part2(arg))


if __name__ == '__main__':
    main()
