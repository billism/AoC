

def preprocess(fn):
    data = []
    pattern = []
    with open(fn) as f:
        for line in f:
            if line.strip() == "":
                data.append(pattern)
                pattern = []
            else:
                pattern.append(list(line.strip()))
    data.append(pattern)
    return data

def count_rows(pattern):
    for i, row in enumerate(pattern[:-1]):
        nrow = pattern[i+1]
        if row == nrow:
            # 说明是一个 reflection line, 向上下延展计数
            if all([a == b for a, b in zip(reversed(pattern[:i+1]), pattern[i+1:])]):
                return i+1
    return 0

def solution1(fn):
    data = preprocess(fn)
    res = 0
    for pattern in data:
        h = count_rows(pattern)
        patternT = list(zip(*pattern))
        v = count_rows(patternT)
        res += h * 100
        res += v
    return res

def find_smudge(pattern):
    # 策略: 折叠, 只有一个点不同
    for i in range(len(pattern)):
        part1 = reversed(pattern[:i+1])
        part2 = pattern[i+1:]
        test = sum([sum([not (x==y) for x, y in zip(a, b)]) for a, b in zip(part1, part2)])
        if test == 1:
            # print(i+1)
            return i+1
    return 0

def solution2(fn):
    data = preprocess(fn)
    res = 0
    for pattern in data:
        h = find_smudge(pattern)
        patternT = list(zip(*pattern))
        v = find_smudge(patternT)
        res += h * 100
        res += v
    return res

if __name__ == "__main__":
    from pathlib import Path
    data = preprocess(Path(__file__).parent / 'test1.txt')
    # print(len(data))
    # for pattern in data:
    #     print(count_rows(pattern))
    # print(solution1('input.txt'))
    print(solution2(Path(__file__).parent / 'input.txt'))
    