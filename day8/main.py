import fileinput


def part1(instrs):
    "returns (halts?, accumulator)"
    acc = 0
    ip = 0
    seen = set()
    while True:
        if ip == len(instrs):
            return (True, acc)

        seen.add(ip)
        op, arg = instrs[ip]
        if op == 'acc':
            acc += arg
            ip += 1
        elif op == 'jmp':
            next_ip = ip + arg
            if next_ip in seen:
                return (False, acc)
            ip = next_ip
        else:
            ip += 1


def part2(instrs):
    for i, (op, arg) in enumerate(instrs):
        if op == 'nop' or op == 'jmp':
            maybe_instrs = instrs[:]
            maybe_instrs[i] = ('nop', arg) if op == 'jmp' else ('jmp', arg)
            halts, acc = part1(maybe_instrs)
            if halts:
                return acc


def main():
    arg = [line.strip() for line in fileinput.input()]
    instrs = []
    for line in arg:
        op, argument = line.split()
        instrs.append((op, int(argument)))

    # 9m23s
    print(part1(instrs))
    # 10m49s
    print(part2(instrs))


if __name__ == '__main__':
    main()
