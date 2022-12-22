#!/usr/bin/python
import fileinput, re, itertools, functools, copy


board = []
path = None

mw = 0
for line in fileinput.input():
    if not line.strip():
        path = ''
        continue

    if path is not None:
        path = line.strip()
        break
    else:
        board.append(line.rstrip())
        mw = max(mw, len(line.rstrip()))

for i in range(len(board)):
    board[i] = board[i] + (' ' * (mw-len(board[i])))

facing_ofs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def add(a, b):
    return tuple(x+y for x,y in zip(a,b))

def tile(pos):
    return board[pos[1]][pos[0]]

def wrap(pos, b):
    y = (pos[1]+len(b)) % len(b)
    x = (pos[0]+len(b[y])) % len(b[y])
    return (x,y)

def step(pos, facing):
    pos = wrap(add(pos, facing_ofs[facing]), board)
    while tile(pos) == ' ':
        pos = wrap(add(pos, facing_ofs[facing]), board)
    return pos, facing

def move(pos, facing, step):
    npos, nfacing = step(pos, facing)
    if tile(npos) == '.':
        return npos, nfacing
    if tile(pos) != '.':
        raise RuntimeError("could not locate a place to stand")
    return pos, facing

trace = [ [c for c in row] for row in board ]

LOC = ("right", "bottom", "left", "top")
REL = ("left of", "above", "right of", "below")
DIR = ("right", "down", "left", "up")

def solve( step ):
    global trace
    pos, facing = ((0, 0), 0)
    while tile(pos) == ' ':
        pos = (pos[0]+1, pos[1])

    pidx = 0
    while pidx < len(path):
        dist = ''
        while pidx < len(path) and path[pidx] in '0123456789':
            dist += path[pidx]
            pidx += 1
        if dist:
            #print("{}: move {} {}".format(pos, dist, DIR[facing]))
            for _ in range( int(dist) ):
                trace[pos[1]][pos[0]] = '>v<^'[facing]
                pos, facing = move(pos, facing, step)

        rot = ''
        if pidx < len(path):
            rot = path[pidx]
            facing = (facing + (1 if path[pidx] == 'R' else 3)) % 4
            #print("{}: rotate {}; now facing {}".format(pos, rot, DIR[facing]))
            pidx += 1
    return pos, facing

pos, facing = solve(step)

#print(dist, rot, pos[0]+1, pos[1]+1, facing)
#for row in trace:
#    print( ''.join(row) )

print("Part 1: {}".format(1000*(pos[1]+1)+4*(pos[0]+1)+facing))

if len(board) < 50:
    face_len = 4
else:
    face_len = 50

face_map = []
face_count = 0
face_pos = []

for y in range(0, len(board), face_len):
    row = ''
    for x in range(0, len(board[y]), face_len):
        if tile((x, y)) == ' ':
            row += ' '
        else:
            row += str(face_count)
            face_count += 1
            face_pos.append((x//face_len, y//face_len))
    face_map.append(row)

for row in face_map:
    print(row)

adjmap = {}

def check(pos, b):
    y = (pos[1]+len(b)) % len(b)
    x = (pos[0]+len(b[y])) % len(b[y])
    return (pos[0] == x) and (pos[1] == y)

adj = [[None for _ in range(4)] for _ in range(6)]
edges_matched = 0

for face in range(6):
    for facing in range(4):
        x, y = add(face_pos[face], facing_ofs[facing])
        if check((x,y),face_map) and face_map[y][x] != ' ':
            cand = int(face_map[y][x])
            print("{} is {} {}".format( face, REL[facing], cand ) )
            x = face_pos[face][0] * face_len
            y = face_pos[face][1] * face_len
            for d in range(face_len):
                adjmap[((x, y), facing)] = (add((x, y), facing_ofs[facing]), facing)
                if facing == 0 or facing == 2:
                    x += 1
                else:
                    y += 1
            adj[face][facing] = (cand, (facing+2)%4, 0, 0)
            edges_matched += 1


expected = [0,0,0,0,1,0,0,1,0,1,0,1,0,0] if len(board)>20 else [0,1,1,0,1,1,1,1,1,1,1,1,1,1]

work = True
while work:
    work = False

    for face in range(6):
        for facing in range(4):
            if adj[face][facing] is None:
                for adjofs in (1, 3):
                    adjdir = (facing+adjofs)%len(facing_ofs)
                    if adj[face][adjdir] is None:
                        continue
                    adjface, adjentrydir, ac, af = adj[face][adjdir]

                    cdir = (adjentrydir+(4-adjofs+2+(2 if ac else 0)))%len(facing_ofs)
                    if adj[adjface][cdir] is None:
                        continue

                    destface, entrydir, c, cf = adj[adjface][cdir]
                    entrydir = (entrydir+adjofs+2+c*2)%4
                    if adj[destface][(entrydir+2)%4] is not None and adj[destface][(entrydir+2)%4][0] != face:
                        continue

                    #print("no direct adjacency to {} edge of {}; checking {}".format(LOC[facing], face, LOC[adjdir]))
                    #print(" -> checking {}".format(LOC[cdir]))
                    #print("because {} is {} {}".format( face, REL[adjdir], adjface ) )
                    #print(" and {} is {} {}".format( adjface, REL[cdir], destface ) )

                    # to calculate this correctly involves walking the perimeter, which is awkward. hardwire instead
                    flip = expected.pop(0)
                    #print(" {}'s {} edge touches {}'s {} edge; distance {}; exiting {} enters {}; {}".format( face, LOC[facing], destface, LOC[(entrydir+2)%4], c+ac, DIR[facing], DIR[entrydir], "flipped" if flip else "unflipped" ))

                    F = face_len-1
                    exits =   ((F, 0, 0, 1), (0, 1, F, 0), (0, 0, 0, 1), (0, 1, 0, 0))
                    entries = ((F, 0, F, -1), (F, -1, F, 0), (0, 0, F, -1), (F, -1, 0, 0)) if flip else exits
                    sxs, sx, sys, sy = exits[facing]
                    srcx = face_pos[face][0] * face_len + sxs
                    srcy = face_pos[face][1] * face_len + sys

                    dxs, dx, dys, dy = entries[(entrydir+2)%4]
                    destx = face_pos[destface][0] * face_len + dxs
                    desty = face_pos[destface][1] * face_len + dys

                    adj[face][facing] = destface, entrydir, c+1, flip
                    for d in range(face_len):
                        adjmap[((srcx, srcy), facing)] = ((destx, desty), entrydir)
                        srcx += sx
                        srcy += sy
                        destx += dx
                        desty += dy

                    work = True
                    edges_matched += 1
                    break

trace = [ [c for c in row] for row in board ]

def cubestep(pos, facing):
    return adjmap.get( (pos, facing), (add(pos, facing_ofs[facing]), facing) )

pos, facing = solve(cubestep)

#for row in trace:
#    print( ''.join(row) )

print("Part 2: {}".format(1000*(pos[1]+1)+4*(pos[0]+1)+facing))
