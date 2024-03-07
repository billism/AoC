# 读取数据
def preprocess(fn):
    data = []
    with open(fn) as f:
        for line in f:
            line = line.rstrip()
            data.append(list(line))
    return data

from pathlib import Path
data = preprocess(Path(__file__).parent / 'input.txt')
print("height", len(data), "width", len(data[0]))

move = {
    "|": ('|7F', '|LJ', ''   , ''  ),  # 顺序: 上下左右
    "-": (''   , ''   , '-LF', '-J7'),
    "L": ('|7F', ''   , ''   , '-J7'),
    "J": ('|7F', ''   , '-LF', ''  ),
    "7": (''  ,  '|LJ', '-LF', ''  ),
    "F": (''  ,  '|LJ', ''   , '-J7'),
}

import math
visited = [[math.inf for ele in row] for row in data]
start_pos = None
for i, row in enumerate(data):
    for j, ele in enumerate(row):
        # 检查是不是起始位置
        if ele == "S":
            start_pos = (i, j)
            visited[i][j] = 0
            break
    if start_pos is not None:
        break
x, y = start_pos
data[x][y] = '7'
            
def travel(current_pos):
    points = [current_pos]
    while len(points) > 0:
        x, y = points[0]
        points.pop(0)
        for s, step in zip(move[data[x][y]], [(-1, 0), (1, 0), (0, -1), (0, 1)]):  # 上下左右
            # print("?", s)
            a, b = step
            new_pos = x+a, y+b
            # 检查是不是可以通行
            # print(data[x+a][y+b])
            if 0 <= x+a < len(data) and 0 <= y+b < len(data[0]) and data[x+a][y+b] in s:
                # 可以通行就试试看
                if visited[x+a][y+b] > visited[x][y] + 1:
                    visited[x+a][y+b] = visited[x][y] + 1
                    points.append(new_pos)

travel(start_pos)
# print(*data, sep='\n')
# print(*visited, sep='\n')
rst = [[-1 if ele == math.inf else ele for ele in row] for row in visited]
# print(rst)
rst = max([max(row) for row in rst])
print(rst)
    