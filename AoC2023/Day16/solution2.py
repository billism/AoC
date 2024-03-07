import time


from pathlib import Path
fn = Path(__file__).parent / 'test1.txt'
fn = Path(__file__).parent / 'input.txt'

data = []
with open(fn) as f:
    for line in f:
        data.append([{"sym":c, "^":None, ">":None, "v":None, "<":None} for c in (line.strip())])

H = len(data)
W = len(data[0])

step = {
    "^": (-1,  0),
    ">": ( 0,  1),
    "v": ( 1,  0),
    "<": ( 0, -1)
}

propagate = {
    (".", "^"): ["^"],
    (".", ">"): [">"],
    (".", "v"): ["v"],
    (".", "<"): ["<"],
    ("/", "^"): [">"],
    ("/", ">"): ["^"],
    ("/", "v"): ["<"],
    ("/", "<"): ["v"],
    ("\\", "^"): ["<"],
    ("\\", ">"): ["v"],
    ("\\", "v"): [">"],
    ("\\", "<"): ["^"],
    ("|", "^"): ["^"],
    ("|", ">"): ["^", "v"],
    ("|", "v"): ["v"],
    ("|", "<"): ["^", "v"],
    ("-", "^"): ["<", ">"],
    ("-", ">"): [">"],
    ("-", "v"): ["<", ">"],
    ("-", "<"): ["<"],
}

tic = time.time()

queue = [(0, 0, ">")]
visited = set()
while queue:
    i, j, b = queue.pop(0)     # 从队列中取出一个
    next_beams = propagate[(data[i][j]['sym'], b)]  #  -> 激发
    visited.add((i, j, b))    # 标记已经激发过了
    for next_beam in next_beams:
        di, dj = step[next_beam]
        new_i, new_j = i+di, j+dj
        if 0 <= new_i < H and 0 <= new_j < W and (new_i, new_j, next_beam) not in visited:
            queue.append((new_i, new_j, next_beam))          # -> 加入到队列

toc = time.time()
print(len(set([(i,j) for i,j,b in visited])))


print((toc - tic)*1000)