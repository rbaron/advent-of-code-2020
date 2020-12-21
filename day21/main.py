import fileinput
import json
import itertools
import re

from dataclasses import dataclass
from typing import List


FOOD_PATT = re.compile(r'^(.+) \(contains (.+)\)$')


@dataclass
class Food:
    ingredients: List[str]
    alergens: List[str]


def parse_line(line):
    match = re.match(FOOD_PATT, line)
    ingredients = [s.strip() for s in match.group(1).split()]
    alergens = [s.strip() for s in match.group(2).split(',')]
    return Food(ingredients, alergens)


def get_possible_ingrs_by_alerg(foods):
    possible_ingrs_by_alerg = {}
    for food in foods:
        for alerg in food.alergens:
            possible = possible_ingrs_by_alerg.get(
                alerg, set(food.ingredients))
            possible_ingrs_by_alerg[alerg] = possible & set(food.ingredients)
    return possible_ingrs_by_alerg


def part1(foods):
    possible_ingrs_by_alerg = get_possible_ingrs_by_alerg(foods)
    all_ingrs = [ingr for f in foods for ingr in f.ingredients]
    return sum(all(ingr not in possible for possible in possible_ingrs_by_alerg.values())
               for ingr in all_ingrs)


def part2(foods):
    alerg_and_possible_ingrs = sorted(get_possible_ingrs_by_alerg(
        foods).items(), key=lambda kv: len(kv[1]))
    ingr_by_alerg = {}
    while len(ingr_by_alerg) != len(alerg_and_possible_ingrs):
        for alerg, possible in alerg_and_possible_ingrs:
            free = possible - set(ingr_by_alerg.values())
            if len(free) == 1:
                ingr_by_alerg[alerg] = next(iter(free))
                break

    return ','.join(
        ingr
        for alerg, ingr in sorted(ingr_by_alerg.items(), key=lambda ai: ai[0])
    )


def main():
    foods = [parse_line(line.strip()) for line in fileinput.input()]

    print(part1(foods))
    print(part2(foods))


if __name__ == '__main__':
    main()
