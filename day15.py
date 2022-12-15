#!/usr/bin/python
import fileinput, re, heapq

entries = []

for line in fileinput.input():
    m = re.search('Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)', line)
    if not m:
        continue
    sx, sy, bx, by = tuple(int(c) for c in m.group(1,2,3,4))
    diameter = (abs(bx-sx) + abs(by-sy))
    entries.append((sx, sy, bx, by, diameter))

def count_beacons(entries, y):
    beacons = set()
    for entry in entries:
        if entry[3] == y:
            beacons.add((entry[2], entry[3]))
    return len(beacons)

def scan_row(entries, y):
    row = []
    for entry in entries:
        width = entry[4] - abs(entry[1]-y)
        if width > 0:
            row.append((entry[0]-width, entry[0]+width))

    simplified = []
    if len(row) > 1:
        row = sorted(row)
        ls, le = row[0]
        for item in row[1:]:
            s, e = item
            if s>le:
                simplified.append((ls, le))
                ls, le = s, e
                continue
            ls = min(ls, s)
            le = max(le, e)
        simplified.append((ls, le))

    return simplified

def count_no_beacon(beacons, row):
    if not row:
        return 0
    last_end = row[0][0]
    no_beacon = -beacons
    for entry in row:
        start = max(entry[0], last_end)
        last_end = max(last_end, entry[1]+1)
        no_beacon += max(last_end-start,0)
    return no_beacon

print("Part 1: {}".format(count_no_beacon(count_beacons(entries, 2000000), scan_row(entries, 2000000))))

results = []
for y in range(4000000):
    r = scan_row(entries, y)
    if len(r) > 1:
        x = r[0][1]+1
        frequency = x*4000000+y
        print("Part 2: ({}, {}) frequency {}".format(x, y, frequency))
        break