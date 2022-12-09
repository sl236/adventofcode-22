#!/usr/bin/python
import fileinput

t = 0
badge = 0

gidx=0
group = None

for line in fileinput.input():
    line = line.strip()

    if gidx == 0:
        group = set(line)
    else:
        group = set(i for i in line if i in group)
    gidx += 1
    if gidx == 3:
        c = tuple(group)[0]
        badge += (ord(c)-ord('A')+27) if c < 'a' else (ord(c)-ord('a')+1)
        gidx = 0

    L = len(line)//2
    s = set(line[:L])
    c = tuple(set(i for i in line[L:] if i in s))[0]

    t += (ord(c)-ord('A')+27) if c < 'a' else (ord(c)-ord('a')+1)

print(t, badge)

