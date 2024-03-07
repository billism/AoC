

def preprocess(fn):
    data = []
    with open(fn) as f:
        for line in f:
            data.append(list(line.strip()))
    return data

def find_free_space(data):
    rows = []
    cols = []
    for i, row in enumerate(data):
        if "#" in row:
            continue
        else:
            rows.append(i)
            
    dataT = list(zip(*data))
    for i, col in enumerate(dataT):
        if "#" in col:
            continue
        else:
            cols.append(i)
    return rows, cols

def shortest_path(a, b, rows, cols, n=10):
    x1, y1 = a
    x2, y2 = b
    result = abs(x2-x1)+abs(y2-y1)
    for r in rows:
        if x1 < r < x2 or x2 < r < x1:
            result += (n-1)
    for c in cols:
        if y1 < c < y2 or y2 < c < y1:
            result += (n-1)
    return result

def solution(fn):
    data = preprocess(fn)
    rows, cols = find_free_space(data)
    galaxies = []
    result = 0
    for i, row in enumerate(data):
        for j, ele in enumerate(row):
            if ele == "#":
                for g in galaxies:
                    result += shortest_path((i,j), g, rows, cols, n=1000000)
                galaxies.append((i,j))
    return result

from pathlib import Path
data = preprocess(Path(__file__).parent / 'test1.txt')
print(find_free_space(data))
print(solution(Path(__file__).parent / 'input.txt'))
