

def preprocess(fn):
    data = []
    with open(fn) as f:
        for line in f:
            line = list(line.strip())
            data.append(line)
    return data

def move_row(row):
    # move to the left
    row_copy = [ele for ele in row]
    last = -1
    for i, ele in enumerate(row):
        if ele == ".":
            continue
        elif ele == "#":
            last = i
        else:
            row_copy[last+1], row_copy[i] = row_copy[i], row_copy[last+1]
            last = last + 1
    return row_copy
        
def solution1(fn):
    data = preprocess(fn)
    dataT = list(zip(*data))
    print(*dataT, sep="\n")
    res = [move_row(row) for row in dataT]
    res = list(zip(*res))
    n = 0
    for i, row in enumerate(reversed(res)):
        n += (i+1) * sum([ele == "O" for ele in row])
    return n

def solution2(fn):
    data = preprocess(fn)
    # print(*data, sep="\n")
    record = {}
    for i in range(300):
        # north
        data = list(zip(*data))
        data = [move_row(row) for row in data]
        data = list(zip(*data))
        # west
        data = data
        data = [move_row(row) for row in data]
        # south
        data = [list(reversed(row)) for row in list(zip(*(data)))]
        data = [move_row(row) for row in data]
        data = list(zip(*[list(reversed(row)) for row in data]))
        # east
        data = [list(reversed(row)) for row in data]
        data = [move_row(row) for row in data]
        data = [list(reversed(row)) for row in data]

        # print(*data, sep="\n")
        n = 0
        for j, row in enumerate(reversed(data)):
            n += (j+1) * sum([ele == "O" for ele in row])
        # if i < 123:
        #     print(i, n, end=",")
        # else:
        #     print(i, n, end="\n")

        if n in record:
            record[n].append(i)
        else:
            record[n] = [i]
    print(*[(k, v) for k, v in sorted(record.items(), key=lambda item: item[1])], sep='\n')

if __name__ == "__main__":
    from pathlib import Path
    fn = Path(__file__).parent /  'test1.txt'
    fn = Path(__file__).parent /  'input.txt'
    # data = preprocess(fn)
    # print(*data, sep="\n")
    
    res = solution2(fn)
    # print("answer:", res)

    # print( (1000000000 - 123) % 26 + 122)