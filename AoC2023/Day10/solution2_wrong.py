
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

## 查找初始时位置, 并确定初始位置的字符
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
        self.id = 0
        self.isoutsider = None

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

# # 可视化
# import matplotlib.pyplot as plt
# mat = [[len(node.nb) for node in row] for row in grid]
# plt.imshow(mat, cmap='jet')
# plt.gca().set_aspect('equal')
# plt.colorbar()
# plt.show()

# 查找 loop
## 顺着一条线走， 如果能回到起点，则是一个 loop
## 如果回不到起点, 则不是 loop
## 注意: 一个 loop 中不可能出现断头路, 即一个 Loop 是一个 closed set
## 注意: 非 loop 也不会出现分叉 (三叉), 必然是一条路线
setid = -1
# # 以每个点做为起点开始检查
for i, row in enumerate(data):
    for j, ele in enumerate(row):
        # 如果是 "." 就跳过 (保持默认的 id=0)
        if ele == ".":
            continue
        # 如果该点不与任何点连通, 也跳过 (保持默认的 id=0)
        if len(grid[i][j].nb) == 0:
            continue
        # 如果有标记过 setid, 也跳过
        if grid[i][j].id != 0:
            continue
        # 剩下的点应该是有连通的点了
        ## 情况一: 是一条单线路径 (到头后要折返, 直到走到另一头)
        ## 情况二: 是一个环形路径
        ## 这次扫描先把所有单线路径找出来
        if len(grid[i][j].nb) == 1:
            start_node = grid[i][j]
            start_node.id = setid
            # 开始追溯
            prev_node = start_node
            current_node = start_node.nb[0]
            current_node.id = setid
            while len(current_node.nb) != 1:
                nb1, nb2 = current_node.nb
                if nb1 == prev_node:
                    prev_node, current_node = current_node, nb2
                else:
                    prev_node, current_node = current_node, nb1
                current_node.id = setid
        # setid -= 1
setid = 1
loops = []
# # 以每个点做为起点开始检查
for i, row in enumerate(data):
    for j, ele in enumerate(row):
        # 如果是 "." 就跳过
        if ele == ".":
            continue
        # 如果该点不与任何点连通, 也跳过
        if len(grid[i][j].nb) == 0:
            continue
        # 如果有标记过 setid, 也跳过
        if grid[i][j].id != 0:
            continue
        # 剩下的点应该是有连通的点了
        ## 情况一: 是一条单线路径 (到头后要折返, 直到走到另一头)
        ## 情况二: 是一个环形路径
        ## 这次扫描专门扫描环形路径
        if len(grid[i][j].nb) == 2:
            loop = []
            start_node = grid[i][j]
            start_node.id = setid
            # 开始追溯
            prev_node = start_node
            current_node = start_node.nb[0]  # 任选一个方向
            current_node.id = setid
            loop.append(start_node.pos)
            loop.append(current_node.pos)
            while True:
                # 当前节点的两个邻居
                nb1, nb2 = current_node.nb
                # 其中一个是 prev_node
                if nb1 == prev_node:
                    prev_node, current_node = current_node, nb2
                else:
                    prev_node, current_node = current_node, nb1
                current_node.id = setid
                loop.append(current_node.pos)
                if current_node == start_node:
                    break
        # setid += 1
        loops.append(loop)

# 如果一条非环形的路线与边缘相接, 则属于 outsider
# # 以每个点做为起点开始检查
line_outsider_id = []
for i, row in enumerate(data):
    for j, ele in enumerate(row):
        # 如果是在边缘, 且不是 loop, 就是 outsider, 然后沿着这个点追溯
        if i == 0 or i == len(data)-1 or j == 0 or j == len(data[0])-1:
            ## 是 Loop 就跳过
            if grid[i][j].id == 1:
                continue
            ## 如果已经标记过了, 也跳过
            if grid[i][j].id == -2:
                continue
            ## 否则就开始上下左右蔓延, 直到触碰到 loop
            wlist = set([(i, j)])
            while wlist: # 不为空
                # 取出队列中的随机一个
                x, y = wlist.pop()
                grid[x][y].id = -2   # 标记为 outsider
                # 检查邻居们
                for stepx, stepy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1,-1), (-1,1), (1,1),(1,-1)]:
                    nx, ny = x+stepx, y+stepy
                    # 检查是不是在 boundary 内
                    if 0 <= nx < len(data) and 0 <= ny < len(data[0]):
                        # 不在 wlist 内, 不是 loop, 也没标记过 outsider
                        if ((nx,ny) in wlist) or (grid[nx][ny].id in [1, -2]):
                            continue
                        else:
                            wlist.add((nx, ny))

# 继续: 注意, 说的是 main loop


rst = sum([sum([node.id in (0,-1) for node in row]) for row in grid])
print(rst)

for i, row in enumerate(grid):
    for j, ele in enumerate(row):
        if ele.id in (1, -2):
            grid[i][j].id = -2
        if ele.id in (0, -1):
            grid[i][j].id = 0
            
# # # 可视化
import matplotlib.pyplot as plt
import numpy as np
mat = [[node.id for node in row] for row in grid]
# imshow: origin: top left, x down, y right
plt.imshow(mat)
ax = plt.gca()
ax.set_aspect('equal')
ax.set_xticks(np.arange(-.5, 140, 1), minor=True)
ax.set_yticks(np.arange(-.5, 140, 1), minor=True)
ax.grid(which='minor', alpha=0.5, linestyle=':')
ax.set_axis_off()
# plt.colorbar()
# for i, row in enumerate(data):
#     for j, ele in enumerate(row):
#         plt.text(j, i, ele, va='center', ha='center', fontsize=8, color='w')
#         # break
for loop in loops:
    xs, ys = list(zip(*loop))
    plt.plot(np.array(ys), np.array(xs), lw=2)
plt.show()        
        
