#!/usr/bin/python
import fileinput

M = [[int(h) for h in line.strip()] for line in fileinput.input()]
visible = set()

walks = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]

for walk in walks:
    dx, dy = walk
    sx, ex, sy, ey = (0, len(M[0])-1, 0, len(M)-1)

    if dx<0:
        sx, ex = ex, sx
    if dy<0:
        sy, ey = ey, sy

    x = sx
    y = sy

    highest = -1
    while True:
        if M[x][y] > highest:
            highest = M[x][y]
            visible.add((x, y))
        if dy == 0:
            if x == ex:
                if y == ey:
                    break
                x = sx
                y = y+1
                highest = -1
            else:
                x = x+dx
        else:
            if y == ey:
                if x == ex:
                    break
                y = sy
                x = x+1
                highest = -1
            else:
                y = y+dy

print("visible: ", len(visible))

best_score = 0

for x in range(len(M[0])):
    for y in range(len(M)):
        score = 1
        for walk in walks:
            cx = x
            cy = y
            dist = 0
            H = M[x][y]
            while ((cx % (len(M[0])-1)) != 0) and ((cy % (len(M)-1)) != 0):
                cx += walk[0]
                cy += walk[1]
                dist += 1
                if M[cx][cy] >= H:
                    break
            score = score * dist

        best_score = max(best_score, score)

print("best: ", best_score)

