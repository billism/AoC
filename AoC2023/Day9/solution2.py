
def preprocess(fn):
    with open(fn) as f:
        data = []
        for line in f:
            row = list(map(int, line.rstrip().split()))
            data.append(row)
    return data

def diff(lst):
    return [b-a for a, b in zip(lst, lst[1:])]

def predict(lst):
    diffs = [lst]
    while any(diffs[-1]):
        new_lst = diff(diffs[-1])
        diffs.append(new_lst)
    v = 0
    for ele in reversed(diffs[:-1]):
        v = ele[0] - v
    return v


def solve_part1(fn):
    data = preprocess(fn)
    rst = 0
    for lst in data:
        rst += predict(lst)
    return rst

# fn = 'test1.txt'
# data = preprocess(fn)
# print(data)
# print(diff(data[0]))
# print(predict(data[0]))
from pathlib import Path
rst = solve_part1(Path(__file__).parent / 'input.txt')
print(rst)