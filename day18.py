#!/usr/bin/python
import fileinput, re, itertools, functools

raw = []

minc = (0,0,0)
maxc = (0,0,0)

for line in fileinput.input():
    voxel = tuple(int(x) for x in line.strip().split(','))
    minc = tuple(min(a,b) for a,b in zip(minc, voxel))
    maxc = tuple(max(a,b) for a,b in zip(maxc, voxel))
    raw.append( voxel )

print("bounds: {} {}".format(minc, maxc))

FULL, EXTERNAL, INTERNAL = 1, 2, 3
NEIGHBOURS = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]

cloud = { v: FULL for v in raw }

def addv( a, b ):
    return tuple(a[i]+b[i] for i in range(len(a)))

minc = addv(minc, (-1,-1,-1))
maxc = addv(maxc, (1,1,1))

def classify(v):
    global cloud
    if v in cloud:
        return cloud[v]
    seen = set()
    tovisit = [v]

    def identify():
        while tovisit:
            curr = tovisit.pop()
            for ofs in NEIGHBOURS:
                dest = addv(curr, ofs)
                if dest in seen:
                    continue
                seen.add(dest)

                c = cloud.get(dest, None)
                if c == FULL:
                    continue
                if c is not None:
                    return c
                if ( any(dest[i]<minc[i] for i in range(len(minc)))
                    or any(dest[i]>maxc[i] for i in range(len(maxc))) ):
                        return EXTERNAL
                tovisit.append(dest)

        return INTERNAL

    c = identify()
    cloud[v] = c

    for v in seen:
        if v not in cloud:
            cloud[v] = c

    for v in tovisit:
        if v not in cloud:
            cloud[v] = c

def dump():
    for z in range(minc[0], maxc[0]+1):
        print('Z: {}'.format(z))
        for y in range(minc[1], maxc[1]+1):
            c = '{:<2} '.format(y)
            for x in range(minc[2], maxc[2]+1):
                c += '?#.+'[cloud.get((x, y, z), 0)]
            print(c)

for x in range(minc[0]-1, maxc[0]+2):
    for y in range(minc[1]-1, maxc[1]+2):
        for z in range(minc[2]-1, maxc[2]+2):
            v = (x, y, z)
            if v not in cloud:
                classify(v)

def count_faces(voxel, test):
    total = 0
    for ofs in NEIGHBOURS:
        if test(cloud.get(addv(voxel, ofs), EXTERNAL)):
            total += 1
    return total

print("part 1: {}".format(sum(count_faces(v, lambda x:x != FULL) for v in raw)))
print("part 2: {}".format(sum(count_faces(v, lambda x:x == EXTERNAL) for v in raw)))
