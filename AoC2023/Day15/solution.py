
def preprocess(fn):
    data = []
    with open(fn) as f:
        for line in f:
            data += line.strip().split(",")
    return data

def calc_hash(s):
    res = 0
    for c in s:
        res += ord(c)
        res *= 17
        res = res % 256
    return res

def solution1(fn):
    data = preprocess(fn)
    return sum(map(calc_hash, data))

def do_weired_thing(s):
    if "-" in s:
        boxid = calc_hash(s[:-1])   # for box
    else:
        boxid = calc_hash(s[:-2])
    
def solution2(fn):
    data = preprocess(fn)
    boxes = [[] for i in range(256)]
    for s in data:
        if "-" in s:
            label = s[:-1]
            boxid = calc_hash(label)
            # print(boxid)
            # 检查相应的 box 有没有这个 label
            idx = -1
            for i, slot in enumerate(boxes[boxid]):
                if slot[0] == label:
                    idx = i
                    break
            if idx > -1:
                boxes[boxid].pop(idx)
        else:
            label = s[:-2]
            boxid = calc_hash(label)
            lens_length = int(s[-1])
            # 检查相应的 box 有没有这个 label
            found = False
            for i, slot in enumerate(boxes[boxid]):
                if slot[0] == label:
                    boxes[boxid][i] = (label, lens_length)
                    found = True
            if not found:
                boxes[boxid].append((label, lens_length))
    res = 0
    for i, box in enumerate(boxes):
        for j, slot in enumerate(box):
            res += (i+1) * (j+1) * slot[1]
    return res
            


if __name__ == "__main__":
    from pathlib import Path

    fn = Path(__file__).parent / 'test1.txt'
    fn = Path(__file__).parent / 'input.txt'
    # data = preprocess(fn)
    # print(calc_hash('ot'))
    # print(*data, sep="\n")
    res = solution2(fn)
    print(res)
    