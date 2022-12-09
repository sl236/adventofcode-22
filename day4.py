#!/usr/bin/python
import fileinput

contains = 0
overlaps = 0
for line in fileinput.input():
    line = line.strip()

    a, b = (tuple(int(x) for x in p.split('-')) for p in line.split(','))

    if( (a[0] >= b[0]) and (a[1] <= b[1]) ) or ( (b[0] >= a[0]) and (b[1] <= a[1]) ):
        contains += 1

    if(a[0] <= b[1]) and (a[1] >= b[0]):
        overlaps += 1

print(contains)
print(overlaps)