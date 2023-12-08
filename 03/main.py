# Author: Donato Quartuccia
# Last Modified: 2023-12-07
import functools
import itertools
import operator
from collections.abc import Generator, Iterable


def adjacent(i: int, j: int, rows: int, cols: int) -> Generator[tuple[int, int]]:
    """Yield all valid adjacent positions to i, j for i < rows and j < cols"""
    values = itertools.product(
        (i - 1, i, i + 1),
        (j - 1, j, j + 1),
    )
    yield from (
        (n, m)
        for n, m in values
        if (n != i or m != j) and -1 < n < rows and -1 < m < cols
    )


def part_numbers(file: str) -> tuple[int, int]:
    """Return the sums of all part numbers and of all gear ratios in the schematic. A part number
    is defined as any number adjacent to a symbol, excluding periods. A gear ratio is defined
    as any number adjacent to an asterisk, when that asterisk is adjacent to another number.

    Precondition: Mo symbol but an asterisk is adjacent to more than one number
    """
    digits = set("0123456789")
    not_symbol = digits.union(".\n")

    with open(file) as schematic:
        grid = [line for line in schematic]
        rows, cols = len(grid), len(grid[0])

        symbols = {
            (i, j): []
            for i, row in enumerate(grid)
            for j, char in enumerate(row)
            if char not in not_symbol
        }
        targets = {
            pair: (i, j) for i, j in symbols for pair in adjacent(i, j, rows, cols)
        }

        for i, row in enumerate(grid):
            curr, key = "", None
            for j, char in enumerate(row):
                if char in digits:
                    curr += char
                    key = key or targets.get((i, j), None)
                elif key is not None:
                    symbols[key].append(int(curr))
                    curr, key = "", None
                else:
                    curr, key = "", None
        part_sum = sum(itertools.chain.from_iterable(symbols.values()))
        gear_sum = sum(
            functools.reduce(operator.mul, numbers)
            for numbers in symbols.values()
            if len(numbers) > 1
        )
        return part_sum, gear_sum


if __name__ == "__main__":
    parts, gears = part_numbers("./input.txt")
    print(f"Day 3: {parts}, {gears}")
