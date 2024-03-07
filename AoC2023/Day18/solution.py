from pathlib import Path

fn = Path(__file__).parent / 'test1.txt'
fn = Path(__file__).parent / 'input.txt'

data = []
with open(fn) as f:
    for line in f:
        row = line.strip().split()
        row[0] = row[0].strip()
        row[1] = int(row[1].strip())
        row[2] = row[2][1:-1]
        data.append(row)

# print(*data, sep="\n")
# print(sum([row[1] for row in data]))

def get_next_node(current_node, d, n):
    i, j = current_node
    new_i, new_j = i, j
    if d == "U":
        new_i = i - n
    if d == "R":
        new_j = j + n
    if d == "D":
        new_i = i + n
    if d == "L":
        new_j = j - n
    if new_i > i:
        return [(k, j) for k in range(i, new_i)], (new_i, new_j)
    if new_i < i:
        return [(k, j) for k in range(i, new_i, -1)], (new_i, new_j)
    if new_j > j:
        return [(i, k) for k in range(j, new_j)], (new_i, new_j)
    if new_j < j:
        return [(i, k) for k in range(j, new_j, -1)], (new_i, new_j)

## 获取整条路线上所有的点
nodes = set()
current_node = (0, 0)
for row in data:
    d, n, c = row
    # print(row)
    lst_nodes, current_node = get_next_node(current_node, d, n)
    # print(lst_nodes, current_node)
    for node in lst_nodes:
        nodes.add(node)
nodes.add(current_node)
# print(nodes, len(nodes))

print(len(nodes))

min_i = min([i for i, j in nodes])
max_i = max([i for i, j in nodes])
min_j = min([j for i, j in nodes])
max_j = max([j for i, j in nodes])

print(min_i, max_i, min_j, max_j)

# 划一个足够大的范围
intpoint = [[0 for _ in range(min_j,max_j+2)] for _ in range(min_i, max_i+2)]
num_inpoint = 0
# 这个范围内的点逐个考察
for i in range(min_i, max_i+2):
    for j in range(min_j, max_j+2):
        if (i, j) in nodes:   # 在圈上
            intpoint[i-min_i][j-min_j] = 2
            continue
        # 判断这个点是内点还是外点
        count = 0
        count1 = 0
        count2 = 0
        for k in range(j, max_j+2):
            n1, n2, n3 = (i-1,k), (i, k), (i+1, k)
            if n2 not in nodes:
                continue
            if n1 in nodes and n2 in nodes:
                count += 1
                continue
            if n1 in nodes and n2 not in nodes:
                count1 -= 1
                if count1 == -2:
                    count1 = 0
                if count1 == -1 and count2 == 1:
                    count += 1
                    count1, count2 = 0, 0
                continue
            if n1 not in nodes and n2 in nodes:
                count2 += 1
                if count2 == 2:
                    count2 = 0
                if count1 == -1 and count2 == 1:
                    count += 1
                    count1, count2 = 0, 0
                continue
            
        if count % 2 == 1:
            intpoint[i-min_i][j-min_j] = 1
            num_inpoint += 1

res = 0
for i, row in enumerate(intpoint):
    for j, ele in enumerate(row):
        if ele > 0:
            res+= 1
print(res)

import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()
ax.imshow(np.array(intpoint))
ax.set_aspect('equal')
plt.show()



