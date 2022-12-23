#!/usr/bin/python
import fileinput, re, itertools, functools, copy

def _f(a, b, f):
    return tuple(f(x,y) for x,y in zip(a,b))

ADD = lambda a, b: (a[0]+b[0], a[1]+b[1])
MIN = lambda a, b: _f(a, b, min)
MAX = lambda a, b: _f(a, b, max)
MUL = lambda a, b: (a[0]*b[0], a[1]*b[1])

elves = []

y = 0
for line in fileinput.input():
    line = line.strip()
    if not line:
        continue

    for x, c in enumerate(line):
        if c == '#':
            elves.append((x, y))
    y += 1


directions = [
    (( 0, -1), [(-1, 0), (1, 0)]),
    (( 0,  1), [(-1, 0), (1, 0)]),
    ((-1,  0), [( 0,-1), (0, 1)]),
    (( 1,  0), [( 0,-1), (0, 1)]),
]

part1 = set(elves)

def moveround(ridx):
    global part1
    proposals = {}

    ridx = ridx % len(directions)
    order = directions[ridx:] + directions[:ridx]

    for elf in part1:
        popn = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if ADD(elf, (dx, dy)) in part1:
                    popn += 1
        if popn == 1:
            continue

        for move, orthogonal in order:
            empty = True
            dest = ADD(elf, move)
            if dest in part1 or ADD(dest, orthogonal[0]) in part1 or ADD(dest, orthogonal[1]) in part1:
                continue
            proposals[dest] = proposals.get(dest, []) + [elf]
            break

    moved = 0
    for dest in proposals:
        elves = proposals[dest]
        if len(elves) != 1:
            continue
        part1.remove(elves[0])
        part1.add(dest)
        moved += 1
    return moved


def area():
    bmin = None
    bmax = None
    for e in part1:
        if bmin is None:
            bmin = e
            bmax = e
        else:
            bmin = MIN(bmin, e)
            bmax = MAX(bmax, e)

    return (bmax[0]-bmin[0]+1) * (bmax[1]-bmin[1]+1)

r = 0
for _ in range(10):
    if not moveround(r):
        break
    r += 1

print("Part 1: {}".format(area() - len(part1)))

while moveround(r):
    r += 1

print("Part 2: {}".format(r+1))
