from pathlib import Path

def preprocess(fn):
    """read data and preprocess
    """
    with open(fn) as f:
        data = {}
        # first line: seeds
        seeds = f.readline()
        data["seeds"] = list(map(int, seeds.strip().split(":")[1].strip().split()))
        # second line: blank
        f.readline()
        ## layer names
        keys = ['s2s', 's2f', 'f2w', 'w2l', 'l2t', 't2h', 'h2l']
        ## each layer represents a mapping
        for key in keys:
            data[key] = []
        ## # the rest lines
        i = 0
        for line in f:
            # if blank line
            if line == "\n":
                # note: sorted by source values
                data[keys[i]] = sorted(data[keys[i]], key=lambda x: x[1])
                i+=1
            else:
                if line[0].isdigit():
                    data[keys[i]].append(list(map(int, line.strip().split())))
                else:
                    pass
        # don't forget this, don't ask why
        data[keys[i]] = sorted(data[keys[i]], key=lambda x: x[1])
        return data

def processor_unit(piece, mapping, bucket):
    """break a biscuit into pieces, transform them, and put them into a bucket
    """
    # piece is a closed interval [a, b]
    # mapping is a set (list) of ordered redirection rules
    # bucket is a set (list) of (transformed) piece
    # break the piece into more pieces and put them into the bucket
    for transporter in mapping:
        if piece == []:
            break
        a, b = piece
        d, s, l = transporter  # a transporter
        # from: [s, s+l-1]
        #   to: [d, d+l-1]
        if b < s:                                # 左侧, 无交集
            bucket.append([a, b])
            piece = []
        elif a < s and s <= b <= (s+l-1):        # 左侧, 有交集
            bucket.append([a, s-1])
            bucket.append([s+(d-s), b+(d-s)])
            piece = []
        elif a < s and b > (s+l-1):              # 完全跨越
            bucket.append([a, s-1])
            bucket.append([s+(d-s), s+l-1+(d-s)])
            piece = [s+l, b]
        elif a >= s and b <= (s+l-1):            # 身居其中
            bucket.append([a+(d-s), b+(d-s)])
            piece = []
        elif s <= a <= (s+l-1) and b > (s+l-1):  # 右侧, 有交集
            bucket.append([a+(d-s), s+l-1+(d-s)])
            piece = [s+l, b]
        elif a > (s+l-1):                        # 右侧, 无交集
            piece = [a, b]
        else:
            print("if you see this, there is something wrong", piece)
    if len(piece) > 0:
        bucket.append(piece)
    return bucket

def solve_part2(fn):
    data = preprocess(fn)
    result = []
    keys = ['s2s', 's2f', 'f2w', 'w2l', 'l2t', 't2h', 'h2l']
    ## seed ranges
    for start, length in zip(data['seeds'][::2], data['seeds'][1::2]):
        # print(start, length)
        # initial bucket, only one piece
        bucket = [[start, start+length-1]]
        ## transport layer by layer
        for key in keys:
            # print(key)
            # print(bucket)
            mapping = data[key]
            new_bucket = []
            for piece in bucket:
                new_bucket = processor_unit(piece, mapping, new_bucket)
            bucket = new_bucket
            bucket = sorted(bucket, key=lambda x:x[0])
            # print(key, bucket[:5])
        result.append(bucket[0][0])
        # break
    return min(result)

if __name__ == "__main__":
    # data = preprocess('input.txt')
    # print(*[f"{k}\n{v}" for k, v in data.items()], sep='\n')
    # print(data)
    import timeit
    number_of_runs = 1000
    bench_time = timeit.timeit(
        lambda: solve_part2(Path(__file__).parent / 'input.txt'),
        number=1000
        )
    print(f"{number_of_runs} runs took {bench_time} seconds")
    print(f"On average, each round took {bench_time*1000/number_of_runs} ms")
    
    