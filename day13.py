#!/usr/bin/python
import fileinput, functools

packets = [eval(line.strip()) for line in fileinput.input() if line.strip()]

def cmp(left, right):
    if isinstance(left, int):
        if isinstance(right, int):
            return 1 if left > right else (-1 if left < right else 0)
        left = [left]
    elif isinstance(right, int):
        right = [right]

    for idx in range(min(len(left), len(right))):
        r = cmp(left[idx], right[idx])
        if r != 0:
            return r

    return -1 if len(left) < len(right) else (1 if len(left) > len(right) else 0)

print( "Part 1: {}".format( sum(
        idx+1 for idx in range(len(packets)//2)
            if cmp(packets[idx*2],packets[idx*2+1]) <= 0 ) ) )

packets.extend([[[2]],[[6]]])
k = 1

for idx, packet in enumerate(sorted(packets, key = functools.cmp_to_key(cmp))):
    if cmp(packet, [[2]]) == 0 or cmp(packet, [[6]]) == 0:
        k *= idx+1

print( "Part 2: {}".format(k) )


