
import heapq
from pathlib import Path

fn = Path(__file__).parent / 'test1.txt'
fn = Path(__file__).parent / 'input.txt'

# 读取数据
data = []
with open(fn) as f:
    for line in f:
        data.append(list(map(int, line.strip())))
# 长宽
H = len(data)
W = len(data[0])

s2i = {s:i for i, s in enumerate(["", "^",">","v","<", "^^",">>","vv","<<", "^^^",">>>","vvv","<<<"])}

def get_neighbors(pos, H, W):
    row, col, s = pos     # 当前的位置, s 指的是当前已经直行的方向和步数
    neighbors = []
    if row > 0     and s[-1:] != "v" and s != "^^^":  # 向上一格
        neighbors.append((row - 1, col, s+"^" if "^" in s else "^"))
    if row < H - 1 and s[-1:] != "^" and s != "vvv":  # 向下一格
        neighbors.append((row + 1, col, s+"v" if "v" in s else "v"))
    if col > 0     and s[-1:] != ">" and s != "<<<":  # 向左一格
        neighbors.append((row, col - 1, s+"<" if "<" in s else "<"))
    if col < W - 1 and s[-1:] != "<" and s != ">>>":  # 向右一格
        neighbors.append((row, col + 1, s+">" if ">" in s else ">"))
    return neighbors

# 最大可能的 Loss, 代替 inf
maxloss = sum([sum(row) for row in data])
loss = [[[maxloss]*13 for _ in range(W)] for _ in range(H)]  # 是个三维的 array, 最后一个维度表示之前连续直行了几步到达这里
parents = [[[None]*13  for _ in range(W)] for _ in range(H)] # 也是个三维的
visited = set()

start_node = (0, 0, '')
stop_nodes  = set([(H-1, W-1, s) for s in s2i])

loss[0][0][s2i[""]] = 0 # data[0][0]

queue = []
heapq.heappush(queue, (loss[0][0][s2i[""]], (0, 0, "")))

while queue:
    current_loss, current_node = heapq.heappop(queue)   # 从队列中取出一个
    if current_node in stop_nodes:
        break
    if current_node in visited:
        continue
    visited.add(current_node)
    
    neighbors = get_neighbors(current_node, H, W)
    for neighbor in neighbors:
        row, col, s = neighbor
        if neighbor in visited:
            continue
        
        weight = data[row][col]
        new_loss = current_loss + weight
        if new_loss < loss[row][col][s2i[s]]:
            loss[row][col][s2i[s]] = new_loss
            parents[row][col][s2i[s]] = current_node
            heapq.heappush(queue, (new_loss, (row, col, s)))

path = []
while current_node != start_node:
    path.append(current_node)
    row, col, s = current_node
    current_node = parents[row][col][s2i[s]]
path.append(start_node)
path = list(reversed(path))

print(min(loss[H-1][W-1]))

# print(*data, sep="\n")
# res = 0
# for node in path:
#     row, col, s = node
#     res += data[row][col]
#     print(row, col, data[row][col], loss[row][col][s2i[s]], res)

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.imshow(data)
for node in path:
    row, col, s = node
    ax.text(col, row, s[-1:], horizontalalignment='center', verticalalignment='center')
plt.show()
