from pathlib import Path

copies = dict()

with open(Path(__file__).parent / 'input.txt') as f:
    for i, line in enumerate(f):
        if i in copies:
            copies[i] += 1
        else:
            copies[i] = 1
        A, B = line.split(":")[1].split("|")
        A = list(map(int, A.strip().split()))
        B = list(map(int, B.strip().split()))
        common = len(set(A).intersection(set(B)))
        for j in range(common):
            if i+j+1 in copies:
                copies[i+j+1] += copies[i]
            else:
                copies[i+j+1] = copies[i]

result = sum([v for k, v in copies.items()])
print(result)
