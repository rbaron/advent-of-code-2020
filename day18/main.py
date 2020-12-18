import fileinput


def apply(op, v1, v2):
    if op == '+':
        return v1 + v2
    elif op == '*':
        return v1 * v2
    else:
        raise RuntimeError(f'Unrecognized operator: {op}')


def eval1(i, elements):
    res = op = None
    while i < len(elements):
        el = elements[i]
        if el.isdigit():
            if op is not None:
                res = apply(op, res, int(el))
            else:
                res = int(el)
            i += 1
        elif el in '+*':
            op = el
            i += 1
        elif el == '(':
            i, sub_res = eval1(i + 1, elements)
            if op is not None:
                res = apply(op, res, sub_res)
            else:
                res = sub_res
        elif el == ')':
            return (i + 1, res)

    return (i, res)


def part1(expressions):
    s = 0
    for e in expressions:
        _, res = eval1(0, e)
        s += res
    return s


def term(i, elements):
    el = elements[i]
    if el.isdigit():
        return i + 1, int(el)
    elif el == '(':
        i, res = expr(i + 1, elements)
        assert elements[i] == ')'
        return i + 1, res
    else:
        raise RuntimeError(f'Invalid term: {el}')


def factor_prime(i, elements):
    if i >= len(elements) or elements[i] != '+':
        return i, 0
    if elements[i] == '+':
        i, t = term(i + 1, elements)
        i, fp = factor_prime(i, elements)
        return i, t + fp


def factor(i, elements):
    i, t = term(i, elements)
    i, fp = factor_prime(i, elements)
    return i, t + fp


def expr_prime(i, elements):
    if i >= len(elements) or elements[i] != '*':
        return i, 1
    if elements[i] == '*':
        i, f = factor(i + 1, elements)
        i, ep = expr_prime(i, elements)
        return i, f * ep


def expr(i, elements):
    '''
    For handling operator precedence, I use the following grammar:

    <expr>   := <factor>
             |  <factor> + <factor>
    <factor> := <term>
             |  <term> * <term>
    <term>   := number
             | ( <expr> )

    Intuitively, <factor>s are things that can be multiplied. They are "up" in the
    gramar, so they have low precedence (nodes are more atomic, for instance a number).
    Conversely, <term>s are things can be summed together. In this weird math, + has higher
    precedence than *, so <terms> are closer to the "bottom" of the grammar.

    As it is, though, this grammar is hard to parse, since we wouldn't know which rule to
    expand at any given moment. I transform this grammar into an LL(1) one, so we know
    exactly which branch to take given the next token to be parsed.

    The transformed grammar is a lot less intuitive:

    <expr>    := <factor> <expr'>
    <expr'>   := * <factor> <expr'>
              |  $
    <factor>  := <term> <factor'>
    <factor'> := + <term> <factor'>
              | $
    <term>    := number
              | ( <expr> )

    With this, I implement a recursive descent parsed that parses exactly one rule at a time.
    More details in my blog post:
    https://rbaron.net/blog/2018/10/05/Hand-rolling-a-minimal-interpreted-programming-language-from-scratch.html
    '''
    i, f = factor(i, elements)
    i, ep = expr_prime(i, elements)
    return i, f * ep


def part2(expressions):
    s = 0
    for expression in expressions:
        _, res = expr(0, expression)
        s += res
    return s


def main():
    arg = [list(''.join(line.strip().split())) for line in fileinput.input()]
    # 23m11s.
    print(part1(arg))
    # +Inf.
    print(part2(arg))


if __name__ == '__main__':
    main()
