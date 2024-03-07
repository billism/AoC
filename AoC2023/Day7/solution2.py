from collections import Counter

cards = {label:i+1 for i, label in enumerate(reversed('AKQT98765432J'))}

def preprocess(fn):
    with open(fn) as f:
        data = {}
        for line in f:
            hand, bid = line.strip().split()
            bid = int(bid)
            data[hand] = bid
        return data

def get_type(hand):
    counts_dict = Counter(hand)
    counts_sort = sorted(list(counts_dict.values()))
    if len(counts_sort)== 1:
        return 7
    if counts_sort == [1, 4]:
        if "J" in counts_dict:
            return 7
        else:
            return 6
    if counts_sort == [2, 3]:
        if "J" in counts_dict:
            return 7
        else:
            return 5
    if counts_sort == [1, 1, 3]:
        if "J" in counts_dict:
            return 6
        else:
            return 4
    if counts_sort == [1, 2, 2]:
        if "J" in counts_dict:
            if counts_dict["J"] == 1:
                return 5
            else:
                return 6
        else:
            return 3
    if counts_sort == [1, 1, 1, 2]:
        if "J" in counts_dict:
            return 4
        else:
            return 2
    if len(counts_sort)== 5:
        if "J" in counts_dict:
            return 2
        else:
            return 1

def map2value(hand):
    hand_type = get_type(hand)
    hand_map = list(map(lambda x: cards[x], hand))
    result = hand_type * 1000
    for ele in hand_map:
        result = result * 16 + ele
    return result

def solution_part2(fn):
    data = preprocess(fn)
    hands = list(data.keys())
    rank = sorted(hands, key=map2value)
    result = 0
    for i, v in enumerate(rank):
        result += (i+1) * data[v]
    return result

if __name__ == "__main__":
    from pathlib import Path
    print("========== cards ==================")
    print(cards)
    print("========== data  ==================")
    data = preprocess(Path(__file__).parent / 'test1.txt')
    print(data)
    print("========== strength  ==============")
    for h, b in data.items():
        print(h, map2value(h), b)
    print("========== solution ===============")
    print(solution_part2(Path(__file__).parent / 'input.txt'))

