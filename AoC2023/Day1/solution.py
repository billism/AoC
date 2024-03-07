from pathlib import Path

########################## Part I #############################
def solve_part1(fn: str) -> int:
    """solution to day1 part1
    """
    result: int = 0
    with open(fn) as f:
        for line in f:
            line = line.strip()
            # search for the first digit
            first_digit = None
            for c in line:
                if c.isdigit():
                    first_digit=c
                    break
            # search for the last digit
            last_digit = None
            for c in reversed(line):
                if c.isdigit():
                    last_digit = c
                    break
            num = int(first_digit+last_digit)
            result += num
    return result


print(solve_part1(Path(__file__).parent / 'test1.txt'))
# print(solve_part1(Path(__file__).parent / 'input.txt'))

########################## Part II ############################
def solve_part2(fn: str) -> int:
    """solution to day1 part2
    """
    result: int = 0
    digits: list[str] = '1 2 3 4 5 6 7 8 9 0'.split()
    digits_words: list[str] = "one two three four five six " \
                              "seven eight nine zero".split()
    with open(fn) as f:
        for line in f:
            line = line.strip()
            # search and replace each digit words
            # e.g.  seven -> seven7seven
            # why? sevenine is actually 79
            # this is not clear from the example
            for i, w in enumerate(digits_words):
                line=line.replace(w, w+digits[i]+w)
            # search for the first digit
            first_digit = None
            for c in line:
                if c.isdigit():
                    first_digit=c
                    break
            # search for the last digit
            last_digit = None
            for c in reversed(line):
                if c.isdigit():
                    last_digit = c
                    break
            num = int(first_digit+last_digit)
            result += num
    return result

print(solve_part2(Path(__file__).parent / 'test2.txt'))
# print(solve_part2(Path(__file__).parent / 'input.txt'))
