import fileinput
import itertools

from collections import deque
from copy import deepcopy
from math import prod


def update_decks(winner, p1, p2):
    if winner == 'p1':
        p1.extend([p1[0], p2[0]])
    else:
        p2.extend([p2[0], p1[0]])
    p2.popleft()
    p1.popleft()


def score(deck):
    return sum(card * i for card, i in zip(reversed(deck), itertools.count(1)))


def part1(p1, p2):
    while p1 and p2:
        update_decks('p1' if p1[0] > p2[0] else 'p2', p1, p2)
    return score(p1) if p1 else score(p2)


def subgame_deque(current_deque):
    return deque(itertools.islice(current_deque, 1, 1 + current_deque[0]))


def cache_key(p1, p2):
    return f'{tuple(p1)}:{tuple(p2)}'


def part2(p1, p2):
    def game(p1, p2):
        '''Returns (winner, winner's deck).'''
        cache = set()
        while p1 and p2:
            winner, win_type, deck = round(p1, p2, cache)
            if win_type == 'game':
                return 'p1', deck
            update_decks(winner, p1, p2)
        if p1:
            return 'p1', p1
        else:
            return 'p2', p2

    def round(p1, p2, cache):
        '''Returns (winner, win_type, winner's deck).'''
        cache_key = f'{p1}:{p2}'
        if cache_key in cache:
            return 'p1', 'game', p1
        cache.add(cache_key)

        top1, top2 = p1[0], p2[0]
        if len(p1) - 1 >= top1 and len(p2) - 1 >= top2:
            sub_game_winner, _ = game(subgame_deque(p1), subgame_deque(p2))
            return sub_game_winner, 'round', None
        else:
            return 'p1' if top1 > top2 else 'p2', 'round', None

    _, deck = game(p1, p2)
    return score(deck)


def main():
    blocks = ''.join(fileinput.input()).split('\n\n')

    def parse_deck(block):
        return list(map(int, block.split('\n')[1:]))

    p1, p2 = map(parse_deck, blocks)
    print(part1(deque(p1), deque(p2)))
    print(part2(deque(p1), deque(p2)))


if __name__ == '__main__':
    main()
