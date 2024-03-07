import sympy as sp
import multiprocessing

def solve(idx):
    fn = 'input.txt'
    stones = []
    with open(fn) as f:
        for line in f:
            p, v = line.strip().split("@")
            p = list(map(int, p.strip().split(",")))
            v = list(map(int, v.strip().split(",")))
            stones.append((p, v))
    
    p0, v0 = stones[idx]     # p0 的初始位置
    p0 = sp.Matrix(p0)
    v0 = sp.Matrix(v0)
    for t in range(1,10000):
        p0t = p0 + t * v0       # t 时刻的位置
        planes = []
        for p1, v1 in stones[idx+1:idx+5]: # 其余的点
            p1 = sp.Matrix(p1)
            v1 = sp.Matrix(v1)
            p1t = p1 + t * v1      # t 时刻的位置
            # 如果石子与 p0 在 t 时刻相遇: p0t, p1t, p1 共面
            try:
                pl = sp.Plane(p0t, p1t, p1)
            except Exception as e:
                print(idx, p1, v1, flush=True);
                print(e);
                return idx, t
            
            planes.append(pl)
        if planes[0].are_concurrent(*planes[1:]):
            print(idx, t, flush=True)
            return idx, t
    return idx, None

def print_result(result):
    print("计算结果：", result)
        

if __name__ == '__main__':
    # 输入参数列表
    input_values = list(range(10,240,20))
    # 创建进程池
    pool = multiprocessing.Pool(len(input_values))
    # 提交任务并获取结果
    results = pool.map(solve, input_values)
    # 等待所有进程完成
    pool.close()
    pool.join()
