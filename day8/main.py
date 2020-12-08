import fileinput


def part1(instrs):
    "returns (halts?, accumulator)"
    acc = 0
    ip = 0
    seen = set()
    while ip != len(instrs):
        seen.add(ip)
        op, arg = instrs[ip]
        ip += 1
        if op == 'acc':
            acc += arg
        elif op == 'jmp':
            ip += arg - 1
            if ip in seen:
                return (False, acc)
    return (True, acc)


def part2(instrs):
    def flip(i):
        instrs[i] = ('nop', arg) if instrs[i][0] == 'jmp' else ('jmp', arg)

    for i, (op, arg) in enumerate(instrs):
        if op == 'nop' or op == 'jmp':
            flip(i)
            halts, acc = part1(instrs)
            if halts:
                return acc
            flip(i)


def main():
    def parse_instr(line):
        op, arg = line.split()
        return op, int(arg)

    instrs = map(parse_instr, fileinput.input())

    # 9m23s
    print(part1(instrs))
    # 10m49s
    print(part2(instrs))


if __name__ == '__main__':
    main()
