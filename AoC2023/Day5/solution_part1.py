import time
from pathlib import Path

def preprocess(fn):
    with open(fn) as f:
        data = {}
        # 读取第一行,
        seeds = f.readline()
        data["seeds"] = list(map(int, seeds.strip().split(":")[1].strip().split()))
        # 读取第二行 (空行)
        f.readline()
        # 读取其余行
        keys = ['s2s', 's2f', 'f2w', 'w2l', 'l2t', 't2h', 'h2l']
        for key in keys:
            data[key] = []
        i = 0
        for line in f:
            if line == "\n":
                # 注意: 这里按照 source 排序了
                data[keys[i]] = sorted(data[keys[i]], key=lambda x: x[1])
                # data[keys[i]] = list(zip(*data[keys[i]]))
                i+=1
            else:
                if line[0].isdigit():
                    data[keys[i]].append(list(map(int, line.strip().split())))
                else:
                    pass
        data[keys[i]] = sorted(data[keys[i]], key=lambda x: x[1])
        return data

data = preprocess(Path(__file__).parent / 'test1.txt')
# print(data)

def get_mapped_value(mapping, value2check):
    result = value2check
    for destination, source, interval in mapping:
        if source <= value2check < source + interval:
            result = value2check + (destination-source)
    return result

def solve_part1(fn):
    data = preprocess(fn)
    keys = ['s2s', 's2f', 'f2w', 'w2l', 'l2t', 't2h', 'h2l']
    nums = []
    for seed in data['seeds']:
        value2check = seed
        for key in keys:
            mapping = data[key]
            mapped_value = get_mapped_value(mapping, value2check)
            value2check = mapped_value
        nums.append(mapped_value)
    return min(nums)


tic = time.time()
print(solve_part1(Path(__file__).parent / 'input.txt'))
print(time.time() - tic)