#!/usr/bin/python
import fileinput

SNDIGITMAP = {
    '0': 0,
    '1': 1,
    '2': 2,
    '-': -1,
    '=': -2,
}

SNDIGITS = '012=-'

def sn_to_dec(x):
    return sum( pow(5, idx) * SNDIGITMAP[d] for idx, d in enumerate(reversed(x)) )

def dec_to_sn(x):
    if x == 0:
        return '0'

    result = ''
    while x > 0:
        result = SNDIGITS[x%5] + result
        x = (x // 5) if (x%5) < 3 else (x+2) // 5
    return result


requirements = []
for line in fileinput.input():
    line = line.strip()
    if not line:
        continue

    requirements.append(line)
    #print("{}: {} {}".format(line, sn_to_dec(line), dec_to_sn(sn_to_dec(line))))

print("Part 1: {}".format(dec_to_sn(sum(sn_to_dec(x) for x in requirements))))

