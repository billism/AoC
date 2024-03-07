from pathlib import Path

fn = Path(__file__).parent / "test1.txt"
fn = Path(__file__).parent / "input.txt"

ans = set(['A','R'])

workflows = {}
with open(fn) as f:
    for line in f:
        if line.strip() == "":
            break
        else:
            wfname, rules = line.strip().split("{")
            rules = rules[:-1].split(",")
            rules1 = []
            rules2 = []
            for ele in rules:
                if ":" not in ele:
                    rules1.append(True)
                    rules2.append(ele)  # 可能是 pv, 也可能是 A
                else:
                    lhs, rhs = ele.split(":")
                    rules1.append(lhs)
                    rules2.append(rhs)
            workflows[wfname] = [rules1, rules2]

def print_wfs(wfs):
    for k, v in wfs.items():
        print(k, v)

print("+++++++++++++++++++++++++++++++++++++++++++")
# print_wfs(workflows)
# print(len(workflows))

import copy

ans = set(['A','R'])
record = {k:[] for k in workflows}
record['A'] = []
record['R'] = []
record['in'] = [{"s":(1,4000),
                "x": (1,4000),
                "a": (1,4000),
                "m": (1,4000)}] # s, x, a, m 顺序

queue = ['in']
while queue:
    wf = queue.pop(0)
    if wf in ans:
        continue
    while record[wf]:
        seg = record[wf].pop(0)   # 待分割的区间
        lhs, rhs = workflows[wf]  # rules
        # 一步步走
        for i, ele in enumerate(lhs):
            # 条件判断
            if isinstance(lhs[i], str):
                c = lhs[i][0]  # s,x,a,m 中的一个
                op = lhs[i][1] # < or >
                num = int(lhs[i][2:])
                if op == "<":
                    # 把符合条件的部分送走 (把 seg 二分)
                    if seg[c][1] < num:  # 整个区间都符合
                        # 全部送走
                        record[rhs[i]].append(seg)
                        queue.append(rhs[i])  # 并加入到队列
                        # 并中断执行这个 wf
                        break
                    elif seg[c][0] >= num: # 整个区间都不符合
                        # 下一条 rule
                        continue
                    else: # 有重合, 即 seg[c][0] <= num <= seg[c][1]
                        cseg1, cseg2 = (seg[c][0], num-1), (num, seg[c][1])
                        new_seg = copy.deepcopy(seg)
                        new_seg[c] = cseg1 # 符合的
                        seg[c] = cseg2     # 不符合的   -> 继续下一条 rule
                        # 送走这个符合的
                        record[rhs[i]].append(new_seg)
                        queue.append(rhs[i])
                else: # op == ">"
                    # 把符合条件的部分送走 (把 seg 二分)
                    if seg[c][0] > num:  # 整个区间都符合
                        # 全部送走
                        record[rhs[i]].append(seg)
                        queue.append(rhs[i])  # 并加入到队列
                        # 并中断执行这个 wf
                        break
                    elif seg[c][1] <= num: # 整个区间都不符合
                        # 下一条 rule
                        continue
                    else: # 有重合, 即 seg[c][0] <= num <= seg[c][1]
                        cseg1, cseg2 = (seg[c][0], num), (num+1, seg[c][1])
                        new_seg = copy.deepcopy(seg)
                        new_seg[c] = cseg2 # 符合的  -> 继续下一条 rule
                        seg[c] = cseg1     # 不符合的
                        # 送走这个符合的
                        record[rhs[i]].append(new_seg)
                        queue.append(rhs[i])
                
            else:
                assert lhs[i] is True, "应该是 True 才对"
                # 全部送走
                record[rhs[i]].append(seg)
                queue.append(rhs[i])

# print(record['A'])
res = 0
for seg in record['A']:
    tmp = 1
    for k, v in seg.items():
        tmp *= (v[1]+1-v[0])
    res += tmp
print(res)
