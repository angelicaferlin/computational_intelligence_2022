import logging
from collections import namedtuple
import random
from typing import Callable
from copy import deepcopy
from itertools import accumulate
from operator import xor
import numpy as np

Nimply = namedtuple("Nimply", "row, num_objects") # move

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    @property
    def k(self) -> int:
        return self._k

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects

# Different help functions
def pure_random(state: Nim) -> Nimply:
    """A strategy that returns a random possible move"""
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

def nim_sum(state: Nim) -> int:
    """Calculates the nim-sum of the board in a given state"""
    *_, result = accumulate(state.rows, xor)
    return result

def active_rows_index(state: Nim) -> list:
  """Returns a list with the index of all the active rows(rows with elem > 0)"""
  active_rows_index = []
  count = 0
  for o in state.rows:
      if o > 0:
        active_rows_index.append(count)
      count += 1
  return active_rows_index


def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k
    ]
    cooked["active_rows_number"] = sum(o > 0 for o in state.rows)

    #list with all active rows
    cooked["active_rows_index"] = active_rows_index(state)

    #list of rows with only 1 elem
    cooked["rows_with_one_element"] = [(index, r) for index, r in enumerate(state.rows) if r == 1]

    #list of rows with multiple elem
    cooked["rows_multiple_elem"] = [(index, r) for index, r in enumerate(state.rows) if r > 1]

    #index of the shortest row
    cooked["shortest_row"] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]

    #index of the longest row
    cooked["longest_row"] = max((x for x in enumerate(state.rows)), key=lambda y: y[1])[0]

    cooked["nim_sum"] = nim_sum(state)
    cooked["pure_random"] = pure_random(state)

    brute_force = list()
    for m in cooked["possible_moves"]:
        tmp = deepcopy(state)
        tmp.nimming(m)
        brute_force.append((m, nim_sum(tmp)))
    cooked["brute_force"] = brute_force

    return cooked