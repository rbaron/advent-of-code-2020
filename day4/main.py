import fileinput


def parse_passports(lines):
    passports = []
    current_pass_keys = {}
    for line in lines:
        if line == "":
            passports.append(current_pass_keys)
            current_pass_keys = {}
        kvs = line.split()
        for kv in kvs:
            k, v = kv.split(':')
            current_pass_keys[k] = v

    if current_pass_keys:
        passports.append(current_pass_keys)
    return passports


def part1(arg):
    return sum(
        len(passport) == 8 or (len(passport) == 7 and 'cid' not in passport)
        for passport in parse_passports(arg)
    )


def part2(arg):
    def valid_height(value):
        if value[-2:] == 'cm':
            return 150 <= int(value[:-2]) <= 193
        elif value[-2:] == 'in':
            return 59 <= int(value[:-2]) <= 76
        else:
            return False

    def valid_hair(value):
        try:
            return value[0] == '#' and int(value[1:], 16) >= 0
        except ValueError:
            return False

    def is_valid(kvs):
        if not(len(kvs) == 8 or (len(kvs) == 7 and 'cid' not in kvs)):
            return False

        return all((
            (1920 <= int(kvs['byr']) <= 2002),
            (2010 <= int(kvs['iyr']) <= 2020),
            (2020 <= int(kvs['eyr']) <= 2030),
            valid_height(kvs['hgt']),
            valid_hair(kvs['hcl']),
            kvs['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
            len(kvs['pid']) == 9  # only numbers?
        ))

    return sum(map(is_valid, parse_passports(arg)))


def main():
    arg = [line.strip() for line in fileinput.input()]

    # 7m46s
    print(part1(arg))
    # 22m56s
    print(part2(arg))


if __name__ == '__main__':
    main()
