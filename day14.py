#!/usr/bin/python
import fileinput

paths = []

for line in fileinput.input():
    paths.append([ (tuple(int(x) for x in pair.split(','))) for pair in line.split('->') ])


xbounds = (99999, 0)
ybounds = (99999, 0)
for path in paths:
    for c in path:
        xbounds = (min(xbounds[0], c[0]), max(xbounds[1], c[0]))
        ybounds = (min(ybounds[0], c[1]-1), max(ybounds[1], c[1]+2))

xbounds = (xbounds[0]-ybounds[1]-1, xbounds[1]+ybounds[1]+1)

SPACE, SAND, WALL = (0, 1, 2)

def sgn(x): # we keep needing this
    if x == 0:
        return 0
    return -1 if x < 0 else 1

MAP = None
def makemap():
    global MAP
    MAP = [ [SPACE for _ in range(xbounds[1]-xbounds[0])] for _ in range(ybounds[1]) ]
    for path in paths:
        c = path[0]
        MAP[c[1]][c[0]-xbounds[0]] = WALL
        for nc in path[1:]:
            dx = sgn(nc[0]-c[0])
            dy = sgn(nc[1]-c[1])
            while c != nc:
                c = (c[0]+dx, c[1]+dy)
                MAP[c[1]][c[0]-xbounds[0]] = WALL

makemap()
atrest = 0
spawn = (500-xbounds[0], 0)
x, y = spawn

while True:
    y += 1
    if y >= ybounds[1]:
        break
    if MAP[y][x] == SPACE:
        continue
    if MAP[y][x-1] == SPACE:
        x -=1
        continue
    if MAP[y][x+1] == SPACE:
        x +=1
        continue
    MAP[y-1][x] = SAND
    x, y = spawn
    atrest += 1

print("Part 1: {}".format(atrest))

makemap()
atrest = 0
spawn = (500-xbounds[0], 0)
x, y = spawn

try:
    while True:
        y += 1
        if y < ybounds[1]:
            if MAP[y][x] == SPACE:
                continue
            if MAP[y][x-1] == SPACE:
                x -=1
                continue
            if MAP[y][x+1] == SPACE:
                x +=1
                continue
        if y==1:
            atrest += 1
            break
        MAP[y-1][x] = SAND
        x, y = spawn
        atrest += 1
except:
    print x, y, xbounds, ybounds
    for row in MAP:
        print(''.join(" .#"[c] for c in row))
    raise

print("Part 2: {}".format(atrest))
