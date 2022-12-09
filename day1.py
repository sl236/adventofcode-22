#!/usr/bin/python
import fileinput

cal = 0
elves = []
for line in fileinput.input():
    line = line.strip()

    if line:
        cal += int(line)
    else:
        elves.append(cal)
        cal = 0

elves.append(cal)
elves = sorted(elves)
print(elves[-1], sum(elves[-3:]))