
def preprocess(fn):
    data = []
    with open(fn) as f:
        for line in f:
            data.append(line.strip())
    return data

move = {
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

class Node:
    def __init__(self, i, j, v):
        self.i = i
        self.j = j
        self.v = v
        self.beam = []
        self.beams = set()
    
def energize(grid, node, queue):
    while node.beam:
        current_beam = node.beam.pop(0)
        if current_beam not in node.beams:
            node.beams.add(current_beam)
            next_beams = propagate[(node.v, current_beam)]
            for next_beam in next_beams:
                step_i, step_j = move[next_beam]
                next_i, next_j = node.i + step_i, node.j + step_j
                if 0 <= next_i < len(grid) and 0 <= next_j < len(grid[0]):
                    next_node = grid[next_i][next_j]
                    next_node.beam.append(next_beam)
                    queue.append(next_node)
        
import matplotlib.pyplot as plt
import numpy as np

def solution1(fn):
    data = preprocess(fn)
    grid = [[Node(i, j, ele) for j, ele in enumerate(row)] for i, row in enumerate(data)]
    start_node = grid[0][0]
    start_node.beam.append(">")
    queue = [start_node]
    
    mat = [[0 for _ in row] for row in data]
    mat = np.array(mat)
    # fig, ax = plt.subplots()
    # ax.set_xlim([0, 110])
    # ax.set_ylim([0, 110])
    # img = ax.imshow(mat)
    # img.set_clim(vmin=0, vmax=1)
    # for i, row in enumerate(data):
    #     for j, ele in enumerate(row):
    #         ax.text(j, i, ele,
    #                 horizontalalignment='center',
    #                 verticalalignment='center',)
    
    while queue:
        node = queue.pop(0)
        # ax.scatter(node.j, node.i, color='y', marker='s')
        # plt.draw()
        # plt.pause(1e-2)
        energize(grid, node, queue)

    res = 0
    for i, row in enumerate(grid):
        for j, ele in enumerate(row):
            if len(ele.beams)>0:
                res += 1
    
    plt.show()
    return res

# def solution2(fn):
#     data = preprocess(fn)
#     ress = []
#     for ii in [0, len(data)-1]:
#         for jj in range(len(data[0])-1):
#             grid = [[Node(i, j, ele) for j, ele in enumerate(row)] for i, row in enumerate(data)]
#             start_node = grid[ii][jj]
#             if ii == 0:
#                 start_node.beam.append("v")
#             else:
#                 start_node.beam.append("^")
#             queue = [start_node]
            
#             while queue:
#                 node = queue.pop(0)
#                 energize(grid, node, queue)

#             res = 0
#             for i, row in enumerate(grid):
#                 for j, ele in enumerate(row):
#                     if len(ele.beams)>0:
#                         res += 1
#             ress.append(res)

#     for ii in range(len(data)-1):
#         for jj in [0, len(data[0])-1]:
#             grid = [[Node(i, j, ele) for j, ele in enumerate(row)] for i, row in enumerate(data)]
#             start_node = grid[ii][jj]
#             if jj == 0:
#                 start_node.beam.append(">")
#             else:
#                 start_node.beam.append("<")
#             queue = [start_node]
            
#             while queue:
#                 node = queue.pop(0)
#                 energize(grid, node, queue)

#             res = 0
#             for i, row in enumerate(grid):
#                 for j, ele in enumerate(row):
#                     if len(ele.beams)>0:
#                         res += 1
#             ress.append(res) 

#     return max(ress)

if __name__ == "__main__":
    from pathlib import Path
    fn = Path(__file__).parent /  'test1.txt'
    fn = Path(__file__).parent /  'input.txt'
    # data=preprocess(fn)
    # print(*data, sep='\n')
    import time
    tic = time.time()
    res = solution1(fn)
    toc = time.time()
    print(res)
    print("time used:", toc - tic)
    # import cProfile
    # cProfile.run('solution1(fn)')
        