from pathlib import Path
#######################################################################
############################## Part I #################################
#######################################################################
def preprocess(fn):
    # 预处理
    games = []
    with open(fn) as f:
        for line in f:
            # single game
            game_play = []
            records = line.split(":")[1].split(";")
            for record in records:
                # single round
                record = record.split(",")
                record_dict = [0, 0, 0]
                for marbles in record:
                    marbles = marbles.strip()
                    if 'red' in marbles:
                        record_dict[0] = int(marbles.split()[0])
                    if 'green' in marbles:
                        record_dict[1] = int(marbles.split()[0])
                    if 'blue' in marbles:
                        record_dict[2] = int(marbles.split()[0])
                game_play.append(record_dict)
            games.append(game_play)
    # print(*games, sep='\n')
    return games

def solve_part1(fn, bag):
    games = preprocess(fn)
    result = 0
    for i, game_play in enumerate(games):
        # 是否每种颜色都满足
        allok = True
        for record in game_play:
            thistime = all([a <= b for a, b in zip(record, bag)])
            allok = allok and thistime
        if allok:
            result += (i+1)   # i+1 是 game index
        # print(i+1, allok)
    return result

print(solve_part1(Path(__file__).parent / 'test1.txt', [12, 13, 14]))
# print(solve_part1(Path(__file__).parent / 'input.txt', [12, 13, 14]))

#######################################################################
############################## Part II ################################
#######################################################################
def solve_part2(fn):
    games = preprocess(fn)
    ## Part II
    result = 0
    for game_play in games:
        numr, numg, numb = list(zip(*game_play))
        a, b, c = max(numr), max(numg), max(numb)
        result += a*b*c
    return result

print(solve_part2(Path(__file__).parent / 'test2.txt'))
# print(solve_part2(Path(__file__).parent / 'input.txt'))