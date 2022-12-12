#!/usr/bin/python
import fileinput

elevations = []
x = -1
y = -1

S = None
E = None

def c2e(c):
    global x, y, S, E
    x+=1
    if c == 'S':
        S = (x, y)
        return 0
    if c == 'E':
        E = (x, y)
        return 25
    return ord(c)-ord('a')

for line in fileinput.input():
    y+=1
    x=-1
    elevations.append([c2e(c) for c in line.strip()])

visitmap = [ [None for _ in row ] for row in elevations ]
height = len(visitmap)
width = len(visitmap[0])

def visit(node):
    global elevations, visitmap

    x, y, distance = node
    elevation = elevations[y][x]
    visitmap[y][x] = distance;
    distance+=1

    for nx, ny in [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]:
        if ny >= 0 and ny < height and nx >= 0 and nx < width:
            v = visitmap[ny][nx]
            if (v is None or v > distance) and (elevation - elevations[ny][nx] <= 1):
                    yield (nx, ny, distance)

stack = [(E[0], E[1], 0)]
while stack:
    s = stack[-1]
    stack = stack[:-1]
    stack.extend( visit(s) )

print("Part 1: {}".format(visitmap[S[1]][S[0]]))

best = None
y = -1
for row in elevations:
    y+=1
    x=-1
    for e in row:
        x+=1
        if e == 0:
            if best is None or (visitmap[y][x] is not None and best > visitmap[y][x]):
                best = visitmap[y][x]

print("Part 2: {}".format(best))