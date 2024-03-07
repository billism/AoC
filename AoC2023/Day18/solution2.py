from pathlib import Path
fn = Path(__file__).parent / 'test1.txt'
fn = Path(__file__).parent / 'input.txt'

i2d = {
    '0':"R",
    '1':"D",
    '2':"L",
    '3':"U"
}

data = []
with open(fn) as f:
    for line in f:
        row = line.strip().split()
        distance = int('0x'+row[2][2:-2], base=16)
        direction = i2d[row[2][-2]]
        data.append((direction, distance))
        # print(row[2], direction, distance)
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
    
    return (new_i, new_j), max(abs(new_i-i), abs(new_j-j))

## 获取整条路线上所有的顶点
nodes = []
current_node = (0, 0)
nodes.append(current_node)
perimeter = 0
for row in data:
    d, n = row
    current_node, length = get_next_node(current_node, d, n)
    perimeter += length
    nodes.append(current_node)
print(nodes[0], nodes[-1])  # 确认开头和结尾是同一个点
print(perimeter)
res = 0
for p1, p2 in zip(nodes[:-1], nodes[1:]):
    p1y, p1x = p1
    p2y, p2x = p2
    a = (p1x*p2y-p1y*p2x)
    res += a
    
print(res/2 + perimeter/2 + 1)
