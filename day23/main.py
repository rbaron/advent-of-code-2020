from __future__ import annotations

import fileinput
import itertools

from dataclasses import dataclass


@dataclass
class Node:
    label: int
    nxt: Node


def make_linked_list(labels):
    node_by_label = {}
    labels_iter = iter(labels)
    first = prev = Node(next(labels_iter), nxt=None)
    node_by_label[first.label] = first
    for label in labels_iter:
        prev.nxt = Node(label, nxt=None)
        prev = prev.nxt
        node_by_label[prev.label] = prev
    prev.nxt = first
    return first, node_by_label


def move(node, node_by_label, max_label):
    picked_up_labels = []
    picked_up = node.nxt
    last_picked_up = picked_up
    for i in range(2):
        picked_up_labels.append(last_picked_up.label)
        last_picked_up = last_picked_up.nxt
    picked_up_labels.append(last_picked_up.label)
    node.nxt = last_picked_up.nxt

    dest_label = node.label - 1
    dest = None
    while True:
        l = dest_label % (max_label + 1)
        if l not in picked_up_labels and l in node_by_label:
            dest = node_by_label[l]
            break
        dest_label = dest_label - 1

    last_picked_up.nxt = dest.nxt
    dest.nxt = picked_up
    return node.nxt


def part1(labels):
    node, node_by_label = make_linked_list(labels)
    for i in range(100):
        node = move(node, node_by_label, 9)
    n = node_by_label[1]
    res = []
    for i in range(8):
        n = n.nxt
        res.append(n.label)
    return ''.join(map(str, res))


N_CUPS = 1_000_000
N_ROUNDS = 10_000_000


def part2(labels):
    node, node_by_label = make_linked_list(
        itertools.chain(labels, range(10, N_CUPS + 1)))
    for i in range(N_ROUNDS):
        node = move(node, node_by_label, N_CUPS)
    n = node_by_label[1]
    return n.nxt.label * n.nxt.nxt.label


def main():
    # labels = list(map(int, '389125467'))
    labels = list(map(int, '712643589'))

    print(part1(labels))
    print(part2(labels))


if __name__ == '__main__':
    main()
