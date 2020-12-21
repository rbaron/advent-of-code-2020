import fileinput
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


def possible_instantiations(food):
    for ingredients in itertools.permutations(food.ingredients, len(food.alergens)):
        yield dict(zip(ingredients, food.alergens))


def is_valid(instantiations):
    ingredient_by_alergen = {}
    for inst in instantiations:
        for ingredient, alergen in inst.items():
            if ingredient != ingredient_by_alergen.get(alergen, ingredient):
                return False
            ingredient_by_alergen[alergen] = ingredient
    return True


def part1(foods):
    ingredients_in_valid_instantiatins = set()
    for instantiations in itertools.product(
        *map(possible_instantiations, foods)
    ):
        if is_valid(instantiations):
            ingredients_in_valid_instantiatins |= {
                ing for inst in instantiations for ing in inst.keys()
            }

    never_assigned = {ing for f in foods for ing in f.ingredients} - ingredients_in_valid_instantiatins
    return sum(1 for f in foods for ing in f.ingredients if ing in never_assigned)


def part2(foods):
    pass


def main():
    foods = [parse_line(line.strip()) for line in fileinput.input()]

    # Works on the test input, too slow for the real deal.
    print(part1(foods))
    # print(part2(foods))


if __name__ == '__main__':
    main()
