#!/usr/bin/python
import fileinput, re, itertools, functools, copy

test = [[1, 2, -3, 3, -2, 0, 4],
        [2, 1, -3, 3, -2, 0, 4],
        [1, -3, 2, 3, -2, 0, 4],
        [1, 2, 3, -2, -3, 0, 4],
        [1, 2, -2, -3, 0, 3, 4],
        [1, 2, -3, 0, 3, 4, -2],
        [1, 2, -3, 0, 3, 4, -2],
        [1, 2, -3, 4, 0, 3, -2]]

vals = []
neg_offset = 0
zero_idx = None

for line in fileinput.input():
    line = line.strip()
    if line:
        if int(line) == 0:
            zero_idx = len(vals)
        vals.append(int(line))
        neg_offset = min(neg_offset, int(line))

neg_offset = ((-neg_offset + len(vals) - 1) // len(vals)) * (len(vals)-1)

if(len(vals) < len(test)):
    print(test[0])

curr = [(i, v) for i,v in enumerate(vals)]
def mix(dkey):
    global curr
    for idx, ofs in enumerate(vals):
        if ofs == 0:
            continue

        ofs = ofs*dkey
        srcidx = curr.index((idx, ofs))
        curr.remove((idx, ofs))
        dest = (srcidx+ofs+neg_offset)%len(curr)
        if dest == 0:
            curr.append((idx, ofs))
        else:
            curr.insert(dest, (idx, ofs))

        if(len(vals) < len(test)) and (dkey == 1):
            print("\n{}: {} expected".format( test[0][idx], test[idx+1]) )
            print("{}: {} actual".format(ofs, [c[1] for c in curr]))

mix(1)
new_zero_idx = curr.index((zero_idx, 0))

print("Part 1: {}".format(sum(curr[(new_zero_idx + i)%len(curr)][1] for i in (1000, 2000, 3000))))

dkey = 811589153
curr = [(i, v*dkey) for i,v in enumerate(vals)]
for _ in range(10):
    mix(dkey)

new_zero_idx = curr.index((zero_idx, 0))
print("Part 2: {}".format(sum(curr[(new_zero_idx + i)%len(curr)][1] for i in (1000, 2000, 3000))))

