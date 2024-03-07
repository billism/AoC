def preprocess(fn):
    with open(fn) as f:
        LRInstruction = f.readline().strip()
        f.readline()
        
        Network = dict()
        for line in f:
            node_value, node_ref = line.strip().split(" = ")
            node_value = node_value.strip()
            node_ref = tuple(node_ref.strip()[1:-1].split(", "))
            Network[node_value] = node_ref
    return LRInstruction, Network

def solve_part1(fn):
    instructions, chain = preprocess(fn)
    current_node = "AAA"
    step_count = 0
    while True:
        for i, instruction in enumerate(instructions):
            if current_node == "ZZZ":
                return step_count
            else:
                select = 0 if instruction == "L" else 1
                current_node = chain[current_node][select]
                step_count += 1

def solve_part2(fn):
    instructions, chain = preprocess(fn)
    # make a map from start to end
    start_nodes  = list(chain)
    current_nodes = start_nodes
    for i, instruction in enumerate(instructions):
        select = 0 if instruction == "L" else 1
        current_nodes = [chain[node][select] for node in current_nodes]
    data = dict(list(zip(start_nodes, current_nodes)))
    
    # 超级加速数数
    anodes = [node for node in data if node.endswith('A')]
    znodes = [node for node in data if node.endswith('Z')]
    result = 1
    for anode in anodes:
        count=0
        cnode = anode
        while True:
            count += 1
            cnode = data[cnode]
            if cnode in znodes:
                print(anode, count)
                result = result*count
                break
    return result * len(instructions)
                
if __name__ == "__main__":
    from pathlib import Path
    data = preprocess(Path(__file__).parent / 'test1.txt')
    # print(data)
    # result = solve_part1(Path(__file__).parent / 'input.txt')
    result = solve_part2(Path(__file__).parent / 'input.txt')
    print(result)
