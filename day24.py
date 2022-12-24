#!/usr/bin/python
import fileinput, re, itertools, functools, copy
from collections import deque

def _f(a, b, f):
    return tuple(f(x,y) for x,y in zip(a,b))

ADD = lambda a, b: (a[0]+b[0], a[1]+b[1])
MIN = lambda a, b: _f(a, b, min)
MAX = lambda a, b: _f(a, b, max)
MUL = lambda a, b: (a[0]*b[0], a[1]*b[1])

DIRS = [ ( 0,  1), ( 1,  0), ( 0, -1), (-1,  0), ( 0,  0), ]
BOARD = []
for line in fileinput.input():
    line = line.strip()
    if not line:
        continue

    line = line[1:-1]
    if '#' in line:
        continue
    BOARD.append(line)

H, W = len(BOARD), len(BOARD[0])
BL = frozenset((x, y) for y in range(H) for x in range(W) if BOARD[y][x] == '<')
BR = frozenset((x, y) for y in range(H) for x in range(W) if BOARD[y][x] == '>')
BU = frozenset((x, y) for y in range(H) for x in range(W) if BOARD[y][x] == '^')
BD = frozenset((x, y) for y in range(H) for x in range(W) if BOARD[y][x] == 'v')

START = (0, 0)
GOAL = (W-1, H-1)

def is_free(pos, t):
    return not any((
        (pos[0], (pos[1] - t) % H) in BD,
        (pos[0], (pos[1] + t) % H) in BU,
        ((pos[0] - t) % W, pos[1]) in BR,
        ((pos[0] + t) % W, pos[1]) in BL
    ))

def bfs(start, goal, st):
    Q = deque()
    seen = set()

    while True:
        while not Q:
            st += 1
            if is_free( start, st ):
                Q.append((start, st))

        while Q:
            key = Q.popleft()
            if key in seen:
                continue
            seen.add(key)
            pos, time = key

            if pos == goal:
                return time

            time += 1
            for d in DIRS:
                cand = ADD(pos, d)
                if 0 <= cand[0] < W and 0 <= cand[1] < H and is_free(cand, time):
                    Q.append((cand, time))

st = bfs(START, GOAL, 0)
print("Part 1: {}".format(st))

st = bfs(GOAL, START, st)
st = bfs(START, GOAL, st)
print("Part 2: {}".format(st))