from pathlib import Path

fn = Path(__file__).parent / 'test1.txt'
fn = Path(__file__).parent / 'input.txt'

data = []
with open(fn) as f:
    for line in f:
        data.append(list(line.strip()))

start_pos = None
gplots = set()

# 找到 S 位置, 记录, 并替换
for i, row in enumerate(data):
    # print(row)
    for j, ele in enumerate(row):
        if ele != "#":
            gplots.add((i,j))
        if ele == "S":
            start_pos=(0, 0, i,j)
print("start pos", start_pos)
# data[start_pos[0]][start_pos[1]] = "."

def get_nbs(pos, grid):
    x, y, i, j = pos
    nrow, ncol = len(grid), len(grid[0])
    tmp = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
    nbs = []
    for nbi, nbj in tmp:
        newx, newy = x, y
        nbii, nbjj = nbi, nbj
        if nbi < 0:
            newx -= 1
            nbii += nrow
        # if 0 <= nbi < nrow:
        #     pass
        if nrow <= nbi:
            newx += 1
            nbii -= nrow
        if nbj < 0:
            newy -= 1
            nbjj += ncol
        # if 0 <= nbj < ncol:
        #     pass
        if ncol <= nbj:
            newy += 1
            nbjj -= ncol
        if grid[nbii][nbjj] == "#":
            continue
        nbs.append((newx, newy, nbii,nbjj))
    return nbs

queue = []
subq = set()
subq.add(start_pos)
queue.append(subq)

count_field = []   # 每一步涉足了多了 fields
# k for kth step
for k in range(300):
    subq = queue[k]  # current positions
    new_subq = set() # next positions
    count_field1 = set()
    for x, y, i, j in subq:
        count_field1.add((x,y))
        nbs = get_nbs((x, y, i,j), data)
        for nb in nbs:
            if nb in new_subq:
                continue
            else:
                new_subq.add(nb)
    count_field.append(len(count_field1))
    queue.append(new_subq)
    # print(len(new_subq))
    # print(sorted(new_subq))

import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

# print(count_field)
print(np.diff(count_field))

# from collections import Counter
# allfield = list(allfield)
# allfield = [k for k, x, y in allfield]
# allfield = sorted(Counter(allfield).items())
# print(allfield)
# import matplotlib.pyplot as plt
# plt.plot(count_field)
# plt.show()

## only i, j
# from collections import Counter
# onlyxy = [Counter([(x,y) for x,y,i,j in subq]) for subq in queue]
# for ct in onlyxy:
#     print(ct[(1,0)], end=',')

# subqsizes = list(map(len, queue))
# import numpy as np

# for i, ele in enumerate(subqsizes):
#     if i % 2 == 0:
#         print(ele, end=", ")
#     else:
#         print(ele)
# print("--------------------------------------")
# for i, ele in enumerate(np.diff(subqsizes)):
#     if i % 2 == 0:
#         print(ele, end=", ")
#     else:
#         print(ele)

# from collections import Counter
# ct = Counter(np.diff(subqsizes))
# print(sorted(ct))

# for subq in queue:
#     print(subq)

