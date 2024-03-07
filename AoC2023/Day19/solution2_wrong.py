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

# print("+++++++++++++++++++++++++++++++++++++++++++")
# print_wfs(workflows)

def simplify(wfs):
    
    allA = []
    allR = []
    
    found = False
    for wf, rules in workflows.items():
        lhs, rhs = rules
        if all([ele=="A" for ele in rhs]):
            allA.append(wf)
            found = True
            continue
        if all([ele=="R" for ele in rhs]):
            allR.append(wf)
            found = True
            continue

    
    # 先删掉它们
    for k in allA + allR:
        del workflows[k]
        
    # 替换
    for wf, rules in workflows.items():
        lhs, rhs = rules
        for i, ele in enumerate(rhs):
            if ele in allA:
                workflows[wf][1][i] = "A"
            if ele in allR:
                workflows[wf][1][i] = "R"
        
    # 有没有 orphan (没有被任何 wf 引用)
    all_with_ref = set(sum([rules[1] for rules in workflows.values()], [])) # 所有被引用到的
    all_wf_keys = list(workflows.keys())
    for wf in all_wf_keys:
        if wf not in all_with_ref:
            del workflows[wf]

    # 删除重复的 conditions (比如 m<571, m<1063, m<1247)
    for wf, rules in workflows.items():
        lhs, rhs = rules
        while True:
            tests = [ele[:2] for ele in lhs[:-1]]
            if len(set(tests)) == len(tests):  # 没有重复的 conditions
                break
            if len(tests)<2:
                break
            # print(tests)
            found2 = False
            collect_i = []
            for i in range(len(tests)-1):
                if tests[i] == tests[i+1]:
                    found2 = True
                    collect_i.append(i+1)
                    
            if not found2:
                break
            else:
                # print("before", wf, lhs, rhs)
                lhs = [ele for i, ele in enumerate(lhs) if i not in collect_i]
                rhs = [ele for i, ele in enumerate(rhs) if i not in collect_i]
                # print("after", wf, lhs, rhs)
        workflows[wf] = [lhs, rhs]

    
    if not found:
        return
    
    return simplify(workflows)

print("+++++++++++++++++++++++++++++++++++++++++++")
simplify(workflows)
print_wfs(workflows)
print(len(workflows))
print(workflows['lcv'])
print(workflows['rv'])

