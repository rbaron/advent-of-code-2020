import fileinput
import math

from collections import defaultdict


def matches_rule(value, ranges):
    return any(lo <= value <= hi for (lo, hi) in ranges)


def matches_any_rules(value, rules):
    return any(matches_rule(value, ranges) for _, ranges in rules)


def part1(nearby, rules):
    return sum(value for n in nearby for value in n
               if not matches_any_rules(value, rules))


def part2(nearby, rules, your_ticket):
    valids = [n for n in nearby if all(matches_any_rules(v, rules) for v in n)]

    # zip(*matrix) transposes a matrix.
    columns = zip(*valids)

    possible_rules_by_col = defaultdict(set)
    for j, column in enumerate(columns):
        for rule_name, ranges in rules:
            if all(matches_rule(c, ranges) for c in column):
                possible_rules_by_col[j].add(rule_name)

    rule_by_col = {}
    taken = set()
    for col, possible_rules in sorted(possible_rules_by_col.items(), key=lambda e: len(e[1])):
        rule = next(iter(possible_rules - taken))
        taken.add(rule)
        rule_by_col[col] = rule

    indices = [i for i, name in rule_by_col.items()
               if name.startswith('departure')]

    return math.prod(your_ticket[i] for i in indices)


def main():
    arg = ''.join(fileinput.input())

    rule_lines, your_lines, nearby_lines = arg.split('\n\n')

    # rule: (rule_name, [range1, range2]).
    def parse_rule(rule_line):
        rule_name, ranges_text = rule_line.split(':')
        ranges = []
        for r in ranges_text.strip().split(' or '):
            lo, hi = map(int, r.split('-'))
            ranges.append((lo, hi))
        return rule_name, ranges

    # A ticket is just a list of integers.
    def parse_ticket(line):
        return list(map(int, line.split(',')))

    rules = [parse_rule(line) for line in rule_lines.split('\n')]
    nearby = [parse_ticket(line) for line in nearby_lines.split('\n')[1:]]
    your = parse_ticket(your_lines.split('\n')[1])

    # 15m57s.
    print(part1(nearby, rules))

    # 22m26s.
    print(part2(nearby, rules, your))


if __name__ == '__main__':
    main()
