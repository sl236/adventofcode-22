#!/usr/bin/python
import fileinput

def marker(line, size):
    buf = line[0:size]
    p = 3

    while len(set(buf)) != size:
        p = p+1
        buf = buf[1:] + line[p]

    return p+1 if len(set(buf)) == size else None

for line in fileinput.input():
    line = line.strip()
    print("{} -- {}".format(marker(line, 4), marker(line, 14)))
