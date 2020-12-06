import fileinput
from functools import reduce
import operator


def main():
    groups = [group.split('\n')
              for group in ''.join(fileinput.input()).split('\n\n')]

    # Part 1
    print(sum(len(reduce(operator.or_, map(set, group)))
              for group in groups))

    # Part 2
    print(sum(len(reduce(operator.and_, map(set, group)))
              for group in groups))


if __name__ == '__main__':
    main()
