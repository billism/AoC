def preprocess(fn):
    with open(fn) as f:
        ts = list(map(int, f.readline().strip().split(":")[1].split()))
        ds = list(map(int, f.readline().strip().split(":")[1].split()))
    return ts, ds

def count_ways(t, d):
    count = 0
    for i in range(t):
        speed = i
        d_real = 0 * i + speed * (t - i)
        if d_real > d:
            count += 1
    return count

def solve_part1(fn):
    ts, ds = preprocess(fn)
    result = 1
    for t, d in zip(ts, ds):
        result *= count_ways(t, d)
        print(t, d, count_ways(t, d))
    return result

########################################################################
def preprocess2(fn):
    with open(fn) as f:
        t = int(f.readline().strip().split(":")[1].replace(" ", ""))
        d = int(f.readline().strip().split(":")[1].replace(" ", ""))
    return t, d

def solve_part2(fn):
    t, d = preprocess2(fn)
    result = count_ways(t, d)
    return result

if __name__ == "__main__":
    from pathlib import Path
    # data = preprocess(Path(__file__).parent / 'test1.txt')
    # data = preprocess(Path(__file__).parent / 'input.txt')
    # print(data)
    # print(*data, sep="\n")
    # print(solve_part1(Path(__file__).parent / 'input.txt'))
    # print(preprocess2(Path(__file__).parent / 'test1.txt'))
    print(solve_part2(Path(__file__).parent / 'input.txt'))
    