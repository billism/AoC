
import heapq
from pathlib import Path

fn = Path(__file__).parent / 'test1.txt'
fn = Path(__file__).parent / 'test2.txt'
fn = Path(__file__).parent / 'input.txt'

# 读取数据
data = []
with open(fn) as f:
    for line in f:
        data.append(list(map(int, line.strip())))
# 长宽
H = len(data)
W = len(data[0])

# 考虑这个问题: 如果当前选择转向, 至多影响之后 10 步

d2i = {d:i for i, d in enumerate(["", "^", ">", "v", "<"])}

def get_neighbors(pos, H, W):
    row, col, s, d = pos     # 当前的位置, s 指的是当前已经直行的方向和步数
    neighbors = []
    # 初始为 0, 往任意方向移动均可
    if row > 0     and s == 0:  # 向上一格
        neighbors.append((row - 1, col, 1, "^"))
    if row < H - 1 and s == 0:  # 向下一格
        neighbors.append((row + 1, col, 1, "v"))
    if col > 0     and s == 0:  # 向左一格
        neighbors.append((row, col - 1, 1, "<"))
    if col < W - 1 and s == 0:  # 向右一格
        neighbors.append((row, col + 1, 1, ">"))
    # 小于四步, 必须继续原方向
    if row > 0     and 0 < s < 4 and d == "^":  # 向上一格
        neighbors.append((row - 1, col, s+1, "^"))
    if row < H - 1 and 0 < s < 4 and d == "v":  # 向下一格
        neighbors.append((row + 1, col, s+1, "v"))
    if col > 0     and 0 < s < 4 and d == "<":  # 向左一格
        neighbors.append((row, col - 1, s+1, "<"))
    if col < W - 1 and 0 < s < 4 and d == ">":  # 向右一格
        neighbors.append((row, col + 1, s+1, ">"))
    # 大于 4 步, 小于 10 步, 可以任意方向 (除了原方向)
    if row > 0     and 4 <= s < 10 and d != "v":  # 向上一格
        neighbors.append((row - 1, col, s+1 if d == "^" else 1, "^"))
    if row < H - 1 and 4 <= s < 10 and d != "^":  # 向下一格
        neighbors.append((row + 1, col, s+1 if d == "v" else 1, "v"))
    if col > 0     and 4 <= s < 10 and d != ">":  # 向左一格
        neighbors.append((row, col - 1, s+1 if d == "<" else 1, "<"))
    if col < W - 1 and 4 <= s < 10 and d != "<":  # 向右一格
        neighbors.append((row, col + 1, s+1 if d == ">" else 1, ">"))
    # 等于 10 步, 必须转向
    if row > 0     and 10 <= s and d in "<>":  # 向上一格
        neighbors.append((row - 1, col, 1, "^"))
    if row < H - 1 and 10 <= s and d in "<>":  # 向下一格
        neighbors.append((row + 1, col, 1, "v"))
    if col > 0     and 10 <= s and d in "^v":  # 向左一格
        neighbors.append((row, col - 1, 1, "<"))
    if col < W - 1 and 10 <= s and d in "^v":  # 向右一格
        neighbors.append((row, col + 1, 1, ">"))    
    return neighbors

# 最大可能的 Loss, 代替 inf
maxloss = sum([sum(row) for row in data])
loss = [[[[maxloss]*5 for _ in range(11)] for _ in range(W)] for _ in range(H)]
parents = [[[[None]*5 for _ in range(11)]  for _ in range(W)] for _ in range(H)]
visited = set()

start_node = (0, 0, 0, "")
stop_nodes = (H-1, W-1)

loss[0][0][0][0] = 0

queue = []
heapq.heappush(queue, (loss[0][0][0][0], (0, 0, 0, "")))

while queue:
    current_loss, current_node = heapq.heappop(queue)   # 从队列中取出一个
    if current_node[:2] == stop_nodes and current_node[2] >=4:
        print('stop point', current_loss)
        break
    if current_node in visited:
        continue
    visited.add(current_node)
    
    neighbors = get_neighbors(current_node, H, W)
    # print(current_node, len(neighbors))
    for neighbor in neighbors:
        row, col, s, d = neighbor
        if neighbor in visited:
            continue
        
        weight = data[row][col]
        new_loss = current_loss + weight
        if new_loss < loss[row][col][s][d2i[d]]:
            loss[row][col][s][d2i[d]] = new_loss
            parents[row][col][s][d2i[d]] = current_node
            heapq.heappush(queue, (new_loss, (row, col, s, d)))

path = []
while current_node != start_node:
    path.append(current_node)
    row, col, s, d = current_node
    current_node = parents[row][col][s][d2i[d]]
path.append(start_node)
path = list(reversed(path))

print((loss[H-1][W-1]))

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
    row, col, s, d = node
    ax.text(col, row, d, horizontalalignment='center', verticalalignment='center')
plt.show()
