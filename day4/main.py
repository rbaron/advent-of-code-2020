import fileinput


def part1(arg):
    valid = 0
    current_pass_keys = set()
    for line in arg:
        if line == "":
            valid += 1 if (len(current_pass_keys) == 8 or (len(current_pass_keys)
                                                           == 7 and 'cid' not in current_pass_keys)) else 0
            current_pass_keys = set()
        kvs = line.split()
        for kv in kvs:
            k, v = kv.split(':')
            current_pass_keys.add(k)
    valid += 1 if (len(current_pass_keys) == 8 or (len(current_pass_keys)
                                                   == 7 and 'cid' not in current_pass_keys)) else 0
    return valid


def part2(arg):
    def valid_height(value):
        if value[-2:] == 'cm':
            return 150 <= int(value[:-2]) <= 193
        elif value[-2:] == 'in':
            return 59 <= int(value[:-2]) <= 76
        else:
            return False

    def valid_hair(value):
        if value[0] != '#':
            return False
        try:
            int(value[1:], 16)
            return True
        except ValueError:
            return False

    def is_valid(kvs):
        if not(len(kvs) == 8 or (len(kvs) == 7 and 'cid' not in kvs)):
            return False

        validations = (
            (1920 <= int(kvs['byr']) <= 2002),
            (2010 <= int(kvs['iyr']) <= 2020),
            (2020 <= int(kvs['eyr']) <= 2030),
            valid_height(kvs['hgt']),
            valid_hair(kvs['hcl']),
            kvs['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth', },
            len(kvs['pid']) == 9  # only numbers?
        )
        return all(validations)

    valid = 0
    current_pass_keys = {}
    for line in arg:
        if line == "":
            valid += 1 if is_valid(current_pass_keys) else 0
            current_pass_keys = {}
        kvs = line.split()
        for kv in kvs:
            k, v = kv.split(':')
            current_pass_keys[k] = v
    valid += 1 if is_valid(current_pass_keys) else 0
    return valid


def main():
    arg = [line.strip() for line in fileinput.input()]

    # 7m46s
    print(part1(arg))
    # 22m56s
    print(part2(arg))


if __name__ == '__main__':
    main()
