#!/usr/bin/python
import fileinput, math

dirs = {
    'U': ( 0,-1),
    'D': ( 0, 1),
    'L': (-1, 0),
    'R': ( 1, 0),
}

visited = set()
visited.add((0,0))

rope = []
for knot in range(10):
    rope.append((0,0))

for line in fileinput.input():
    d, a = line.split(' ')
    d = dirs[d]
    for s in range(int(a)):
        H = rope[0]
        H = (H[0] + d[0], H[1] + d[1])
        rope[0] = H
        for knot in range(len(rope)-1):
            H = rope[knot]
            T = rope[knot+1]
            xd = H[0]-T[0]
            yd = H[1]-T[1]
            if( abs(xd) <= 1 ) and ( abs(yd) <= 1 ):
                continue
            xd = math.copysign( 1, xd ) if xd != 0 else 0
            yd = math.copysign( 1, yd ) if yd != 0 else 0
            rope[knot+1] = (T[0]+xd, T[1]+yd)
        visited.add(rope[-1])

print(len(visited))
