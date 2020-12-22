import fileinput
import itertools

from collections import deque
from copy import deepcopy
from math import prod


def part1(p1, p2):
    while p1 and p2:
        if p1[0] > p2[0]:
            p1.extend([p1[0], p2[0]])
        else:
            p2.extend([p2[0], p1[0]])
        p2.popleft()
        p1.popleft()

    if p1:
        return sum(card * i for card, i in zip(reversed(p1), itertools.count(1)))
    else:
        return sum(card * i for card, i in zip(reversed(p2), itertools.count(1)))


def tail(deq, n):
    return deque(itertools.islice(deq, 1, 1 + n))


def cache_key(p1, p2):
    return f'{tuple(p1)}:{tuple(p2)}'


def part2(p1, p2):
    def game(p1, p2, game_n):
        cache = set()
        print(f'=== Game {game_n} ==')
        round_n = 1
        while p1 and p2:
            # print(f'-- Round {round_n} (Game {game_n})')
            winner, win_type, deck = round(p1, p2, game_n, round_n, cache)

            # print(f'Player {winner} wins round {round_n} of game {game_n}!')
            if win_type == 'game':
                print(f'The winner of game {game_n} is player {round_n}')
                return 'p1', deck


            if winner == 'p1':
                p1.extend([p1[0], p2[0]])
            else:
                p2.extend([p2[0], p1[0]])
            p1.popleft()
            p2.popleft()
            round_n += 1

        if p1:
            return 'p1', p1
        else:
            return 'p2', p2

    def round(p1, p2, game_n, round_n, cache):
        cache_key = f'{p1}:{p2}'
        if cache_key in cache:
            return 'p1', 'game', p1
        cache.add(cache_key)

        t1, t2 = p1[0], p2[0]
        print(f'Player 1\'s deck:', ', '.join(map(str, p1)))
        print(f'Player 2\'s deck:', ', '.join(map(str, p2)))
        print(f'Player 1 plays: {t1}')
        print(f'Player 2 plays: {t2}')

        if len(p1) - 1 >= t1 and len(p2) - 1 >= t2:
            sub_game_winner, _ = game(tail(p1, t1), tail(p2, t2), game_n + 1)
            return sub_game_winner, 'round', None
        else:
            return 'p1' if t1 > t2 else 'p2', 'round', None

    winner, deck = game(p1, p2, game_n=1)
    return sum(card * i for card, i in zip(reversed(deck), itertools.count(1)))


def main():
    blocks = ''.join(fileinput.input()).split('\n\n')

    def parse_deck(block):
        return deque(map(int, block.split('\n')[1:]))

    p1, p2 = map(parse_deck, blocks)
    # print(part1(p1, p2))
    print(part2(p1, p2))


if __name__ == '__main__':
    main()
