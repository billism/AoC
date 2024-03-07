

class flipflop():
    def __init__(self, name, receivers, queue):
        self.name = name            # string
        self.receivers = receivers  # list of names
        self.queue = queue          # a list
        self.state = False
    ## act = receive and send (to queue)
    def act(self, pulse, sender):
        # 只有收到 low 的时候才会反应
        if pulse == "low":
            self.state = not self.state  # 翻转
            if self.state:
                self.send("high")
            else:
                self.send('low')
    def send(self, pulse):
        for receiver1 in self.receivers:
            self.queue.append([receiver1, pulse, self.name])

class conjunction():
    def __init__(self, name, receivers, queue):
        self.name = name
        self.receivers = receivers
        self.queue = queue
        self.senders = {}  # name:type
    
    def act(self, pulse, sender):
        self.senders[sender] = pulse
        if all([self.senders[s]=='high' for s in self.senders]):
            self.send('low')
        else:
            self.send('high')

    def send(self, pulse):
        for receiver1 in self.receivers:
            self.queue.append([receiver1, pulse, self.name])                

class broadcast():
    def __init__(self, name, receivers, queue):
        self.name = "broadcaster"
        self.receivers = receivers
        self.queue = queue   
    def act(self, pulse, sender):
        self.send('low')
    def send(self, pulse):
        for receiver1 in self.receivers:
            self.queue.append([receiver1, pulse, self.name])

from pathlib import Path
fn = Path(__file__).parent / 'test1.txt'
fn = Path(__file__).parent / 'test2.txt'
fn = Path(__file__).parent / 'input.txt'


mdict = {}
queue = []

with open(fn) as f:
    for line in f:
        lhs, rhs = line.strip().split("->")
        if lhs.startswith("%"):  # flipflop
            name = lhs.strip()[1:]
            receivers = [ ele.strip() for ele in rhs.strip().split(",")]
            mdict[name] = flipflop(name, receivers, queue)
        elif lhs.startswith("&"):  # conjunction
            name = lhs.strip()[1:]
            receivers = [ ele.strip() for ele in rhs.strip().split(",")]
            mdict[name] = conjunction(name, receivers, queue)
        else:
            # broadcaster
            name = lhs.strip()
            assert name == 'broadcaster', "出错了, 预期是 broadcaster"
            receivers = [ ele.strip() for ele in rhs.strip().split(",")]
            mdict[name] = broadcast(name, receivers, queue)

for k, v in mdict.items():
    if isinstance(mdict[k], conjunction):
        for k1, v1 in mdict.items():
            if k1 == k:
                continue
            if k in v1.receivers:
                mdict[k].senders[k1] = 'low'

for k, v in mdict.items():
    if isinstance(v, conjunction):
        print(k, v.senders)

count = []
cycle = {}
for i in range(100000):
    # print(i, "=============")
    queue.append(('broadcaster', 'low', 'button'))
    while queue:
        m, pulse, sender  = queue.pop(0)
        # print(sender, "->", pulse, "->", m)
        if sender != "button" and isinstance(mdict[sender], conjunction) and len(mdict[sender].senders) > 1 and pulse == "low":
            # print(i, sender, m)
            if sender in cycle:
                cycle[sender].append(i)
            else:
                cycle[sender] = [i]
        count.append(pulse=='high')
        if m not in mdict:
            # print(m)
            if pulse == 'low':
                pass
                # print(i)
            continue
        mdict[m].act(pulse, sender)

for k,v in cycle.items():
    print(k, sorted(list(set(v))))

