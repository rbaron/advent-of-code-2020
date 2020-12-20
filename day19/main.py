import fileinput


def matches(string, rules):
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
                    # Problem: with loops, we might match in more than one ways!
                    # Idea: do a dfs here.

                    new_j, matched = inner(sub_rule_n, j)
                    # if rule_n in [0, 11]:
                    #     print(f'rule n: {rule_n} from {j}:{new_j}: {string[j:new_j]}. sub rule: {sub_rule_n}, matched: {matched}')
                    j = new_j
                    if not matched:
                        matched_all = False
                        break
                if matched_all and (True if rule_n != 0 else j == len(string)):
                    return j, True
            return i, False
    i, matched = inner(0, 0)
    return matched and i == len(string)


def part1(rules, strings):
    return sum(matches(string, rules) for string in strings)


def part2(rules, strings):
    # 8: matches 42 one of more times
    # rules[8] = ('conj', [[42], [42, 8]])
    # 11: matches (42*k + 31*k), for k >= 1
    # rules[11] = ('conj', [[42, 31], [42, 11, 31]])


    string = 'aab'
    print(matches(string, rules))

    # k = 10
    # rules[8] = ('conj', [[42] * i for i in range(1, k)])
    # rules[11] = ('conj', [[42] * i + [31] * i for i in range(1, k)])
    # print('should be false: ', matches('aaaaabbaabaaaaababaa', rules))
    # print('should be true: ', matches('babbbbaabbbbbabbbbbbaabaaabaaa', rules))
    # return sum(matches(string, rules) for string in strings)


# 246 too high
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
    # print(part1(rules, strings))
    print(part2(rules, strings))


if __name__ == '__main__':
    main()
