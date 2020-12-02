from collections import Counter


def part1(arg):
    def is_valid(line):
        policy, password = [part.strip() for part in line.split(':')]
        counts, char = policy.split(' ')
        pol_min, pol_max = map(int, counts.split('-'))
        return pol_min <= Counter(password)[char] <= pol_max

    return sum(map(is_valid, arg))


def part2(arg):
    def is_valid(line):
        policy, password = [part.strip() for part in line.split(':')]
        counts, char = policy.split(' ')
        pol_i, pol_j = map(int, counts.split('-'))
        return (password[pol_i - 1] == char) ^ (password[pol_j - 1] == char)

    return sum(map(is_valid, arg))


def main():
    # Test input.
    # arg = [
    #     '1-3 a: abcde',
    #     '1-3 b: cdefg',
    #     '2-9 c: ccccccccc',
    # ]

    with open('input.txt', 'r') as f:
        arg = list(f.read().split('\n'))

    print(part1(arg))
    print(part2(arg))


if __name__ == '__main__':
    main()
