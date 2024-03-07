
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
            start_pos=(i,j)
# print(start_pos)
# data[start_pos[0]][start_pos[1]] = "."

def get_nbs(pos, grid):
    i, j = pos
    nrow, ncol = len(grid), len(grid[0])
    tmp = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
    nbs = []
    for nbi, nbj in tmp:
        if not (0<=nbi<nrow):
            continue
        if not (0<=nbj<ncol):
            continue
        if grid[nbi][nbj] == "#":
            continue
        nbs.append((nbi,nbj))
    return nbs

visited = set()
queue = []
subq = set()
subq.add(start_pos)
queue.append(subq)

for k in range(64):
    subq = queue[k]
    new_subq = set()
    for i, j in subq:
        nbs = get_nbs((i,j), data)
        for nb in nbs:
            if nb in new_subq:
                continue
            else:
                new_subq.add(nb)
    queue.append(new_subq)

# for subq in queue:
#     print(subq)
print(len(queue[-1]))
# print(len(visited))

# for i, row in enumerate(data):
#     newrow = ["O" if (i,j) in visited else ele for j, ele in enumerate(row) ]
#     print(newrow)