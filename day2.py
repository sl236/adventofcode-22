#!/usr/bin/python
import fileinput

desc = {
    'X': (1, 3, 0, 6),
    'Y': (2, 6, 3, 0),
    'Z': (3, 0, 6, 3),

    'A': (3+0, 1+3, 2+6),
    'B': (1+0, 2+3, 3+6),
    'C': (2+0, 3+3, 1+6),
}

total1 = 0
total2 = 0

for line in fileinput.input():
    line = line.strip()

    play, response = line.split(' ')

    score = desc[response][0] + desc[response][1+ord(play)-ord('A')]
    total1 += score

    score = desc[play][ord(response)-ord('X')]
    total2 += score

print(total1, total2)