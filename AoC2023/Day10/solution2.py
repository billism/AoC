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

move = {
    "|": ('|7F', '|LJ', ''   , ''   ),  # 顺序: 上下左右
    "-": (''   , ''   , '-LF', '-J7'),
    "L": ('|7F', ''   , ''   , '-J7'),
    "J": ('|7F', ''   , '-LF', ''   ),
    "7": (''  ,  '|LJ', '-LF', ''   ),
    "F": (''  ,  '|LJ', ''   , '-J7'),
    ".": (''  ,  ''   , ''   , ''   )
}

## 查找初始位置, 并确定初始位置的字符
start_pos = None
for i, row in enumerate(data):
    for j, ele in enumerate(row):
        # 检查是不是起始位置
        if ele == "S":
            # 初始点的坐标
            start_pos = (i, j)
            print("Start Poisition Coordinates: ", start_pos)
            # 已知必然与两个方向连通, 与另外两个方向无连通
            start_c = set('|-LJ7F')
            # 上
            new_pos = (i-1, j)
            if 0<=(i-1)<len(data) and 0<=j<len(data[0]):
                if move[data[i-1][j]][1] != '':
                    start_c = start_c.intersection(set(move[data[i-1][j]][1]))
            # 下
            new_pos = (i+1, j)
            if 0<=(i+1)<len(data) and 0<=j<len(data[0]):
                if move[data[i+1][j]][0] != '':
                    start_c = start_c.intersection(set(move[data[i+1][j]][0]))
            # 左
            new_pos = (i, j-1)
            if 0<=i<len(data) and 0<=(j-1)<len(data[0]):
                if move[data[i][j-1]][3] != '':
                    start_c = start_c.intersection(set(move[data[i][j-1]][3]))
            # 右
            new_pos = (i, j+1)
            if 0<=i<len(data) and 0<=(j+1)<len(data[0]):
                if move[data[i][j+1]][2] != '':
                    start_c = start_c.intersection(set(move[data[i][j+1]][2]))
            # 应该只有唯一解!
            data[i][j] = start_c.pop()
            print("Start Position Character: ", data[i][j])
            break
    if start_pos is not None:
        break

## 定义一个节点
class node():
    def __init__(self, pos, v):
        self.pos = pos
        self.v = v
        self.nb = []  # 长度可以是 0, 1, 2

# 构建一个 graph
grid = [[node((i, j), ele) for j, ele in enumerate(row)] for i, row in enumerate(data)]
for i, row in enumerate(data):
    for j, ele in enumerate(row):
        # 如果是 "." 就跳过 (nb 就是空 list, 没问题)
        if ele == ".":
            continue
        # 否则, 检查上下左右是否联通 (至多有两个连通)
        ## idx 其实是指代上下左右
        for idx, val, step in zip([0, 1, 2, 3], move[data[i][j]], [(-1, 0), (1, 0), (0, -1), (0, 1)]):
            a, b = step
            x, y = i+a, j+b   # 邻居的坐标
            # 检查跟邻居是否联通 (只管自己)
            if 0 <= x < len(data) and 0 <= y < len(data[0]) and data[x][y] in val:
                grid[i][j].nb.append(grid[x][y])

# 查找 loop
## 顺着一条线走， 如果能回到起点，则是一个 loop
## 如果回不到起点, 则不是 loop
## 注意: 一个 loop 中不可能出现断头路, 即一个 Loop 是一个 closed set
## 注意: 非 loop 也不会出现分叉 (三叉), 必然是一条路线
loops = []
visited = set()
# # 以每个点做为起点开始检查
for i, row in enumerate(data):
    for j, ele in enumerate(row):
        # 检查是否已经访问过了
        if grid[i][j] in visited:
            continue
        else:
            visited.add(grid[i][j])
        # 如果该点不与任何点连通, 跳过
        if len(grid[i][j].nb) == 0:
            continue
        # 如果只有一个 neighbor, 也跳过, 不可能属于一个 loop
        if len(grid[i][j].nb) == 1:
            continue
        ## 检查是不是 loop 中的一个 node
        ## 终止条件: 走到尽头; 回到开头
        if len(grid[i][j].nb) == 2:
            loop = []
            start_node = grid[i][j]
            prev_node, current_node = None, start_node
            # 开始追溯
            while len(current_node.nb) == 2:
                loop.append(current_node)
                # 当前节点的两个邻居
                nb1, nb2 = current_node.nb
                # move: 其中一个是 prev_node, 另外一个就是下一个要追溯的 node
                if nb1 == prev_node:
                    prev_node, current_node = current_node, nb2
                else:
                    prev_node, current_node = current_node, nb1
                # 检查回到起点了吗? 如果是则找到一个 loop
                if current_node == start_node:
                    loop.append(current_node) # 如果想看到loop的开口, 就把这一行注释掉
                    loops.append(loop)
                    break
                # 检查是不是 visited 过了 (肯定不是 loop)
                if current_node in visited:
                    break
                else:
                    visited.add(current_node)
                # 检查是不是 start node

print("Number of Loops: ", len(loops))
loops = sorted(loops, key=len, reverse=True)
print(f"Loop length: {[len(loop) for loop in loops]}")

mainloop = set(loops[0])

check = [[0 for _ in row] for row in data]
## 逐个点探查, 看穿过 loop 几次
for i, row in enumerate(data):
    for j, ele in enumerate(row):
        if grid[i][j] in mainloop:
            continue
        # 边缘的点肯定在 Loop 外或者 Loop 上, 而不会在其内
        if i == 0 or i == len(data)-1 or j== 0 or j == len(data[0])-1:
            continue
        # 持续向下走, 看穿过 Loop 几次
        count = 0
        lhalf, rhalf = False, False
        for k in range(i+1, len(data)):  # 至多不会超过这些步
            if grid[k][j] in mainloop:
                if data[k][j] == "-":
                    count += 1
                elif data[k][j] == "|":
                    continue
                elif data[k][j] == "7" or data[k][j] == "J":
                    lhalf = not lhalf
                    if lhalf and rhalf:
                        count += 1
                        lhalf, rhalf = False, False
                else:
                    rhalf = not rhalf
                    if lhalf and rhalf:
                        count += 1
                        lhalf, rhalf = False, False
        check[i][j] = (count % 2) == 1

rst = sum([sum([ele for ele in row]) for row in check])
print(rst)

import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()
# 首先绘制 mainloop
xs, ys = list(zip(*[node.pos for node in loops[0]]))
ax.plot(ys, xs)
ax.set_axis_off()
# 然后绘制标记的点
ax.imshow(np.array(check))
plt.show()


# # # 可视化
# import matplotlib.pyplot as plt
# import numpy as np
# mat = [[node.id for node in row] for row in grid]
# # imshow: origin: top left, x down, y right
# plt.imshow(mat, cmap='jet')
# ax = plt.gca()
# ax.set_aspect('equal')
# ax.set_xticks(np.arange(-.5, 140, 1), minor=True)
# ax.set_yticks(np.arange(-.5, 140, 1), minor=True)
# ax.grid(which='minor', alpha=0.5, linestyle=':')
# plt.colorbar()
# # for i, row in enumerate(data):
# #     for j, ele in enumerate(row):
# #         plt.text(j, i, ele, va='center', ha='center', fontsize=8, color='w')
# #         # break
# for loop in loops:
#     xs, ys = list(zip(*loop))
#     plt.plot(np.array(ys), np.array(xs), lw=2)
# plt.show()        
        
