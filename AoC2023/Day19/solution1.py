from pathlib import Path

fn = Path(__file__).parent / "test1.txt"
fn = Path(__file__).parent / "input.txt"

workflows = {}
parts = []
with open(fn) as f:
    for line in f:
        if line.strip() == "":
            break
        else:
            wfname, rules = line.strip().split("{")
            rules = rules[:-1].split(",")
            workflows[wfname] = rules
            
    for line in f:
        part = line.strip()[1:-1].split(',')
        part = [item.split("=") for item in part]
        part = {k:int(v) for k, v in part}
        parts.append(part)

# print(workflows)
# print(parts)

ans = set(['A','R'])
parts_ans = []

for part in parts:
    # print("正在进行", part)
    x, m, a, s = part['x'], part['m'], part['a'], part['s']
    wf = 'in'
    offer = None
    while offer is None:
        for branch in workflows[wf]:
            # print("WF", wf)
            # print("Branch", branch)
            # 先判断是不是 A 或 R
            if branch in ans:
                offer = branch
                parts_ans.append([part, branch])
                break
            # 如果不是 A 或 R, 可能需要条件测试或者不需要
            else:
                if ":" in branch: # 需要判断
                    lhs, rhs = branch.strip().split(":")
                    # print("需要条件测试", lhs, rhs)
                    if eval(lhs): # 通过了条件测试
                        # print("测试通过")
                        if rhs in ans:  # 是个结果
                            # print("得到结果")
                            offer = branch
                            parts_ans.append([part, rhs])
                            break
                        else: # 是跳转
                            # print("是个跳转")
                            wf = rhs    # 是个跳转
                            break
                    else:
                        # print("未通过测试, 下一项")
                        continue
                else: # 不需要条件测试, 直接跳转
                    # print("无需测试, 直接跳转", branch)
                    wf = branch
                    break

# print(parts_ans)
res = 0
for item in parts_ans:
    part, ans = item[0], item[1]
    if ans == 'A':
        res += sum(part.values())

print(res)