################# Part I ###################
def preprocess(fn):
    data1 = []
    data2 = []
    with open(fn) as f:
        for line in f:
            part1, part2 = line.strip().split()
            # 把连续的多个 "." 合并成一个
            count_p = sum([c == "." for c in part1])
            if count_p > 1:
                for i in range(count_p, 1, -1):
                    part1 = part1.replace("." * i, ".")
            # 结尾加上一个 "."
            part1 = part1 + "."
            data1.append(part1)
            data2.append(list(map(int, part2.split(","))))
    return data1, data2

def count(ss, nn):
    if len(nn) == 0:
        return int("#" not in ss)
    n = nn[0]
    if len(ss) < n:
        return 0
    if ss.startswith("."):
        return count(ss[1:], nn)
    if ss.startswith("?"):
        c1 = count("."+ss[1:], nn)
        c2 = count("#"+ss[1:], nn)
        return c1+c2
    if ss.startswith("#"):
        # 必须把第一个数消耗完
        if "." not in ss[:n]:
            return int("#" not in ss[n:n+1]) * count(ss[n+1:], nn[1:])
        else:
            return 0


def solution1(fn):
    data1, data2 = preprocess(fn)
    res = 0
    for s1, s2 in zip(data1, data2):
        m = count(s1, s2)
        res +=m
    return res

################# Part II ###################
def preprocess2(fn):
    data1 = []
    data2 = []
    with open(fn) as f:
        for line in f:
            part1, part2 = line.strip().split()
            part1 = "?".join([part1] * 5)
            # 把连续的多个 "." 合并成一个
            count_p = sum([c == "." for c in part1])
            if count_p > 1:
                for i in range(count_p, 1, -1):
                    part1 = part1.replace("." * i, ".")
            # 结尾加上一个 "."
            part1 = part1 + "."
            data1.append(part1)
            part2 = ",".join([part2] * 5)
            data2.append(tuple(list(map(int, part2.split(",")))))
    return data1, data2

from functools import cache

@cache
def count2(ss, nn):
    if len(nn) == 0:
        return int("#" not in ss)
    n = nn[0]
    if len(ss) < n:
        return 0
    if ss.startswith("."):
        return count2(ss[1:], nn)
    if ss.startswith("?"):
        c1 = count2("."+ss[1:], nn)
        c2 = count2("#"+ss[1:], nn)
        return c1+c2
    if ss.startswith("#"):
        # 必须把第一个数消耗完
        if "." not in ss[:n]:
            return int("#" not in ss[n:n+1]) * count2(ss[n+1:], nn[1:])
        else:
            return 0


def solution2(fn):
    data1, data2 = preprocess2(fn)
    # for a, b in zip(data1, data2):
    #     print(a, b)
    res = 0
    for s1, s2 in zip(data1, data2):
        m = count2(s1, s2)
        # print(m)
        res +=m
    return res

from pathlib import Path
# data1, data2 = preprocess("test1.txt")
# print(*data1, sep='\n')
# print(*data2, sep='\n')
print(solution2(Path(__file__).parent / 'input.txt'))

