#!/usr/bin/python
import fileinput


init = []
fi = fileinput.input()
for line in fi:
    if not line.strip():
        break
    init.append(line.rstrip())

stacks = []
for _ in range((len(init[-1])+3) // 4):
    stacks.append('')
init=init[:-1]

for row in init:
    idx = 1
    while idx < len(row):
        if row[idx] != ' ':
            stacks[idx//4] += row[idx]
        idx += 4

print(stacks)

for line in fi:
    line = line.strip()
    if not line.startswith('move '):
        continue

    _, count, _, f, _, t = line.split(' ')
    count=int(count)
    f=int(f)-1
    t=int(t)-1
    print( count, f, t )
    # part 1
    #    for _ in range(count):
    #        c = stacks[f][0]
    #        stacks[f] = stacks[f][1:]
    #        stacks[t] = c+stacks[t]
    c = stacks[f][:count]
    stacks[f] = stacks[f][count:]
    stacks[t] = c + stacks[t]

    for row in stacks:
        print(row)

print("\n")
print(''.join(row[0] for row in stacks))