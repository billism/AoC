from pathlib import Path
from itertools import groupby, product

def preprocess(fn):
    with open(fn) as f:
        board = []
        idx = 0
        mapping = {}
        for line in f:
            line = [list(g) for k, g in groupby(line.strip(), lambda x: x.isdigit())]
            for group in line:
                if group[0].isdigit():
                    num = int("".join(group))       # 实际的数字是多少
                    mapping[idx] = num              # 给它分配一个 ID
                    for i, ele in enumerate(group): # 把数字替换成其 ID
                        group[i] = idx
                    idx += 1
            line = sum(line, [])
            board.append(line)
    return board, mapping

board, mapping = preprocess(Path(__file__).parent / 'test1.txt')
# print(*board, sep='\n')

def look_around(board, i, j):
    """给定一个 symbol 的位置, 检查其周围有无数字, 如果有, 就返回其 ID
    """
    Height = len(board)
    Width  = len(board[0])
    hs = [i-1, i, i+1]
    vs = [j-1, j, j+1]
    coords = list(product(hs, vs))
    coords = [(a, b) for a, b in coords if (0<=a<Width) and (0<=b<Height)]
    num_idx = set()
    for a, b in coords:
        if isinstance(board[a][b], int):
            num_idx.add(board[a][b])
    return num_idx

def solve_part1(fn):
    board, mapping = preprocess(fn)
    all_idx = set()
    for i, row in enumerate(board):
        for j, ele in enumerate(row):
            # 检查是不是一个 symbol
            if not (isinstance(ele, int) or ele == "."):
                num_idx = look_around(board, i, j)
                all_idx = all_idx.union(num_idx)
    return sum([mapping[idx] for idx in all_idx])

print(solve_part1(Path(__file__).parent / 'test1.txt'))
print(solve_part1(Path(__file__).parent / 'input.txt'))

def solve_part2(fn):
    board, mapping = preprocess(fn)
    result = 0
    for i, row in enumerate(board):
        for j, ele in enumerate(row):
            # 检查是不是 "*"
            if ele == "*":
                num_idx = look_around(board, i, j)
                if len(num_idx)==2:
                    num_idx = list(num_idx)
                    result += mapping[num_idx[0]] * mapping[num_idx[1]]
    return result

print(solve_part2(Path(__file__).parent / 'test2.txt'))
print(solve_part2(Path(__file__).parent / 'input.txt'))