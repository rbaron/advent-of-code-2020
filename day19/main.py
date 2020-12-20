import fileinput
from functools import lru_cache


def matches_part1(string, rules):
    def inner(rule_n, i):
        rule_type, clauses = rules[rule_n]
        if rule_type == 'leaf':
            if string[i] == clauses:
                return i + 1, True
            else:
                return i + 1, False
        else:
            for clause in clauses:
                j = i
                matched_all = True
                for sub_rule_n in clause:
                    if j >= len(string):
                        matched_all = False
                        break
                    j, matched = inner(sub_rule_n, j)
                    if not matched:
                        matched_all = False
                        break
                if matched_all:
                    return j, True
            return i, False
    i, matched = inner(0, 0)
    return matched and i == len(string)


def matches_part2(string, rules):
    @lru_cache
    def inner(rule_n, substr):
        if not substr:
            return False
        rule_type, clauses = rules[rule_n]
        if rule_type == 'leaf':
            return substr == clauses
        else:
            if rule_n == 8:
                return all(inner(42, substr[i:i+8]) for i in range(0, len(substr), 8))
            elif rule_n == 11:
                middle = len(substr) // 2
                return (
                    all(inner(42, substr[i:i+8]) for i in range(0, middle, 8)) and
                    all(inner(31, substr[i:i+8]) for i in range(middle, len(substr), 8)))

            # Regular rules
            for clause in clauses:
                if len(clause) == 1:
                    if inner(clause[0], substr):
                        return True
                elif len(clause) == 2:
                    # Return True if there is a split that matches both halves.
                    for i in range(0, len(substr)):
                        r1, r2 = clause
                        if inner(r1, substr[:i]) and inner(r2, substr[i:]):
                            return True
                else:
                    raise RuntimeError(
                        f'Invalid number of rules: {len(clause)}')
            return False

    return inner(0, string)


def part1(rules, strings):
    return sum(matches_part1(string, rules) for string in strings)


def part2(rules, strings):
    return sum(matches_part2(string, rules) for string in strings)


def main():
    rules, strings = ''.join(fileinput.input()).split('\n\n')

    def parse_rule(rule_line):
        n, clauses = rule_line.split(':')
        clauses = clauses.strip()
        if clauses.startswith('"'):
            return int(n), ('leaf', clauses[1])
        else:
            clauses = clauses.split('|')
            return int(n), ('conj', [list(map(int, clause.split())) for clause in clauses])

    rules = dict(map(parse_rule, rules.split('\n')))
    strings = strings.split('\n')
    print(part1(rules, strings))
    print(part2(rules, strings))


if __name__ == '__main__':
    main()
