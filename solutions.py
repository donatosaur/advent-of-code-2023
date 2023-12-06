# Author: Donato Quartuccia
# Last Modified: 2023-12-05
import functools
import operator
import re


# ------------------------------------- Day 1 -------------------------------------
def sum_calibration_values(file: str, include_words: bool) -> int:
    """Return the sum of the first and last digits of each line"""
    translate = {str(n): n for n in range(10)}
    translate_words = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }
    translate |= translate_words if include_words else {}
    group = '|'.join(translate.keys())
    first = re.compile(f'(?=({group}))')
    last = re.compile(f'.*({group})')

    with open(file) as calibration_input:
        match_generator = (
            (first.search(line), last.search(line))
            for line in calibration_input
        )
        digits = (
            (translate[match.group(1)] for match in matches)
            for matches in match_generator
        )
        return sum(n * 10 + m for n, m in digits)


# ------------------------------------- Day 2 -------------------------------------
def score_games(file: str, max_red: int, max_green: int, max_blue: int) -> tuple[int, int]:
    """Return the sum of the IDs of all games possible with the passed max numbers of marbles
    and the sum of the products of the minimum number of cubes required to play each game
    """
    pattern = re.compile(r'(\d+) (\w+)')

    def parse_line(line: str) -> dict[str, int]:
        bag = {'red': 0, 'green': 0, 'blue': 0}
        for num, color in pattern.findall(line):
            bag[color] = max(bag[color], int(num))
        return bag

    def is_possible(bag: dict[str, int]) -> bool:
        return all((
            bag["red"] <= max_red,
            bag["green"] <= max_green,
            bag["blue"] <= max_blue,
        ))

    with (open(file) as game_record):
        bags = (parse_line(line) for line in game_record)
        marbles_by_game = {k: v for k, v in enumerate(bags, 1)}
        game_id_sum = sum(
            game_id for game_id, bag in marbles_by_game.items() if is_possible(bag)
        )
        find_power = functools.partial(functools.reduce, operator.mul)
        marble_power = sum(find_power(bag.values()) for bag in marbles_by_game.values())
        return game_id_sum, marble_power


if __name__ == '__main__':
    simple_total = sum_calibration_values('input/day_1.txt', False)
    complete_total = sum_calibration_values('input/day_1.txt', True)
    print(f'Day 1: {simple_total}, {complete_total}')

    game_ids, power = score_games('input/day_2.txt', 12, 13, 14)
    print(f'Day 2: {game_ids}, {power}')
