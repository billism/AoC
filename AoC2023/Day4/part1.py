from pathlib import Path

result = 0
with open(Path(__file__).parent / 'input.txt') as f:
    for line in f:
        A, B = line.split(":")[1].split("|")
        A = list(map(int, A.strip().split()))
        B = list(map(int, B.strip().split()))
        common = len(set(A).intersection(set(B)))
        if common == 0:
            continue
        else:
            result += 2**(common-1)
print(result)