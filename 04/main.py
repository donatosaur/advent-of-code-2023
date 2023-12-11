# Author: Donato Quartuccia
# Last Modified: 2023-12-08
import itertools
from collections.abc import Generator, Iterable


def parse(s: str) -> set[int]:
    """Return a set of all integers from s, assuming s is a string beginning
    with whitespace and whose digits are space-delimited and always exactly
    two characters wide"""
    return {int(s[i : i + 2]) for i in range(1, len(s), 3)}


def score_cards(file: str) -> tuple[int, int]:
    """Return the score of all original scratch cards and the total number of additional
    scratch cards won. Scores are calculated as 1 for one match, doubled for each additional
    match. Matching scratch cards reward additional scratch cards equal to the number of
    matches"""
    with open(file) as card_record:
        parsed_record = (line.split(":")[1].split("|") for line in card_record)
        matches = [len(parse(left) & parse(right)) for left, right in parsed_record]
        scratch_cards = [1 for _ in matches]
        for i, num_matches in enumerate(matches):
            for j in range(i + 1, min(i + 1 + num_matches, len(scratch_cards))):
                scratch_cards[j] += scratch_cards[i]
        score = sum(2 ** (m - 1) if m > 0 else 0 for m in matches)
        cards = sum(scratch_cards)
        return score, cards


if __name__ == "__main__":
    total_score, total_cards = score_cards("./input.txt")
    print(f"Day 4: {total_score}, {total_cards}")
