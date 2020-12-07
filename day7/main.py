import fileinput
import re
from collections import defaultdict


# 18m43s
def part1(arg):
    container_pat = r'^(.+) bags contain'
    contents_pat = r'(\d+) (.+?) bag'
    containers_by_content = defaultdict(list)
    for line in arg:
        container = re.findall(container_pat, line)[0]
        contents = re.findall(contents_pat, line)
        for (n, content) in contents:
            containers_by_content[content].append(container)

    def traverse(key):
        total = set(containers_by_content[key])
        for container in containers_by_content[key]:
            total |= traverse(container)
        return total

    return len(traverse('shiny gold'))


# 7m11s
def part2(arg):
    container_pat = r'^(.+) bags contain'
    contents_pat = r'(\d+) (.+?) bag'
    contents_by_container = defaultdict(list)
    for line in arg:
        container = re.findall(container_pat, line)[0]
        contents = re.findall(contents_pat, line)
        for (n, content) in contents:
            contents_by_container[container].append((int(n), content))

    def traverse(key):
        total = 1
        for (n, content) in contents_by_container[key]:
            total = total + (n * traverse(content))
        return total

    # Discount the outmost bag itself.
    return traverse('shiny gold') - 1


def main():
    arg = [line.strip() for line in fileinput.input()]

    print(part1(arg))
    print(part2(arg))


if __name__ == '__main__':
    main()
