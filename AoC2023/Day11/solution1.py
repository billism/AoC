

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

def correct_space(data):
    rows, cols = find_free_space(data)
    for i, x in enumerate(rows):
        data = data[:x+i+1] + data[x+i:]
    dataT = list(zip(*data))
    for j, y in enumerate(cols):
        dataT = dataT[:y+j+1] + dataT[y+j:]
    data = list(zip(*dataT))
    return data

def shortest_path(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x2-x1)+abs(y2-y1)

def solution(fn):
    data = preprocess(fn)
    data = correct_space(data)
    galaxies = []
    result = 0
    for i, row in enumerate(data):
        for j, ele in enumerate(row):
            if ele == "#":
                for g in galaxies:
                    result += shortest_path((i,j), g)
                galaxies.append((i,j))
    return result

from pathlib import Path
data = preprocess(Path(__file__).parent / 'test1.txt')
print(*data, sep='\n')
print(find_free_space(data))
data = correct_space(data)
print(*data, sep='\n')
print(shortest_path((2,0), (7, 12)))
print(solution(Path(__file__).parent / 'input.txt'))
