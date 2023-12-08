# Author: Donato Quartuccia
# Last Modified: 2023-12-05
import re


def sum_calibration_values(file: str, include_words: bool) -> int:
    """Return the sum of the first and last digits of each line"""
    translate = {str(n): n for n in range(10)}
    translate_words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    translate |= translate_words if include_words else {}
    group = "|".join(translate.keys())
    first = re.compile(f"(?=({group}))")
    last = re.compile(f".*({group})")

    with open(file) as calibration_input:
        match_generator = (
            (first.search(line), last.search(line)) for line in calibration_input
        )
        digits = (
            (translate[match.group(1)] for match in matches)
            for matches in match_generator
        )
        return sum(n * 10 + m for n, m in digits)


if __name__ == "__main__":
    simple_total = sum_calibration_values("./input.txt", False)
    complete_total = sum_calibration_values("./input.txt", True)
    print(f"Day 1: {simple_total}, {complete_total}")
