
# O(n) time, O(n) space.
def part1(numbers_lst):
    numbers = set(numbers_lst)
    for number in numbers:
        diff = 2020 - number
        if diff in numbers:
            return number * diff


# O(n^2) time, O(n) space.
def part2(numbers_lst):
    numbers = set(numbers_lst)
    for first in numbers:
        for second in numbers:
            if second == first:
                continue
            third = 2020 - first - second
            if third in numbers:
                return first * second * third


# O(nlogn) time, O(1) space (we could do in-place sorting).
def part1_solution2(numbers_lst):
    numbers = sorted(numbers_lst)
    p1 = 0
    p2 = len(numbers) - 1
    while p1 != p2:
        s = numbers[p1] + numbers[p2]
        if s == 2020:
            return numbers[p1] * numbers[p2]
        elif s > 2020:
            p2 -= 1
        else:
            p1 += 1


# O(n^2) time, O(1) space (we could do in-place sorting).
def part2_solution2(numbers_lst):
    numbers = sorted(numbers_lst)

    # p2 is the pivot.
    for p2 in range(1, len(numbers) - 1):
        p1 = 0
        p3 = len(numbers) - 1
        while p1 != p2 and p3 != p2:
            s = numbers[p1] + numbers[p2] + numbers[p3]
            if s == 2020:
                return numbers[p1] * numbers[p2] * numbers[p3]
            elif s > 2020:
                p3 -= 1
            else:
                p1 += 1


def main():
    # Test input.
    # numbers = [1721, 979, 366, 299, 675, 1456]

    with open('input.txt', 'r') as f:
        numbers = list(map(int, f.read().split('\n')))

    print(part1(numbers))
    print(part2(numbers))

    print(part1_solution2(numbers))
    print(part2_solution2(numbers))


if __name__ == '__main__':
    main()
