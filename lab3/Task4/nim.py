from collections import namedtuple
from typing import Callable
import random
from copy import deepcopy

Nimply = namedtuple("Nimply", "row, num_objects")


# Nim class
class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    # this allow to use the while loop on the object (when all rows are zeroed this returns false)
    def __bool__(self):
        return sum(self._rows) > 0

    # representation "override"
    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    def __hash__(self) -> int:
        return hash(tuple(self.rows))

    @property
    def rows(self) -> tuple:
        return tuple(self._rows) if len(self._rows) > 0 else tuple((0, 0))

    @property
    def k(self) -> int:
        return self._k

    def nimming(self, ply: Nimply):
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects
        self._rows = sorted([x for x in self._rows if x > 0])
        return self

    # The rewards -1 and 1 are given if the state is a final state or not (and so it tells if the last move led to a win)
    def get_reward(self):
        if self.rows == (0, 0):
            return 1
        else:
            return -1

    def possible_moves(self):
        return [(r, o) for r, c in enumerate(self.rows) for o in range(1, c + 1)]


# Strategy class
class Strategy:
    def __init__(self, dna: list) -> None:
        self._dna = dna
        self._step = 0

    def move(self) -> Callable:
        next_move = self._dna[self._step]
        self._step += 1
        if self._step >= len(self._dna):
            self._step = 0
        return next_move


# A random row with a random number of objects is pick
def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)


# Gabriele's strategy
def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))


# Opponent strategy generator (based on the evolution turn)
def opponent_strategy() -> Strategy:
    # return Strategy([gabriele])
     return Strategy([pure_random])
    # return Strategy([optimal_strategy])
    #return new_strategy()


# During the final evaluation it's possible to compare against a different strategy
def opponent_strategy_evaluate() -> Strategy:
    # return Strategy([gabriele])
    # return Strategy([pure_random])
    # return Strategy([optimal_strategy])
    return new_strategy()


# Optimal function
def nim_sum(state: Nim) -> int:
    result = state.rows[0]
    for row in state.rows[1:]:
        result = result ^ row
    return result


# Professor's cook_status to have all the cooked data inside a single dictionary
def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked['possible_moves'] = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if
                                state.k is None or o <= state.k]
    cooked['nim_sum'] = nim_sum(state)

    cooked['even_object_rows'] = [x[0] for x in enumerate(state.rows) if x[1] % 2 == 0 and x[1] != 0]
    cooked['odd_object_rows'] = [x[0] for x in enumerate(state.rows) if x[1] % 2 != 0]
    cooked['shortest_row'] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]

    brute_force = list()
    for m in cooked['possible_moves']:
        tmp = deepcopy(state)
        tmp.nimming(m)
        brute_force.append((m, nim_sum(tmp)))
    cooked['brute_force'] = brute_force

    return cooked


# This rule is the one that exploit the nim sum
def optimal_strategy(state: Nim) -> Nimply:
    data = cook_status(state)
    return next((bf for bf in data['brute_force'] if bf[1] == 0), random.choice(data['brute_force']))[0]


def new_strategy() -> Strategy:
    return make_strategy([5, 4, 6])
    # return make_strategy([5,4])
    # return make_strategy([5])
    # return make_strategy([4])
    # return make_strategy([6])


# Utility function to generate a strategy with an input list of index in the tactics list
def make_strategy(dna: list) -> Strategy:
    used_tactics = list()

    for al, _ in zip(dna, range(len(dna))):
        used_tactics.append(tactics[al])

    return Strategy(used_tactics)


# This rule picks one object from the shortest row
def pick_one_from_min(state: Nim) -> Nimply:
    data = cook_status(state)
    return Nimply(data['shortest_row'], 1)


# This rule picks half (+1) the objects from the even objects row that has the maximum number of objects
def pick_even_max(state: Nim) -> Nimply:
    data = cook_status(state)
    info = data['even_object_rows'] if data['even_object_rows'] != [] else data['odd_object_rows']
    row_ = max(info, key=lambda x: x)
    return Nimply(row_, (state.rows[row_] // 2) + 1)


# This rule picks half the objects from the odd objects row that has the maximum number of objects
def pick_odd_max(state: Nim) -> Nimply:
    data = cook_status(state)
    info = data['odd_object_rows'] if data['odd_object_rows'] != [] else data['even_object_rows']
    row_ = max(info, key=lambda x: x)
    return Nimply(row_, state.rows[row_] // 2)


# Tactics list brought from lab3-task2 (ignore the duplicated gabriele)
tactics = [gabriele, gabriele, gabriele, gabriele, pick_one_from_min, pick_even_max, pick_odd_max]