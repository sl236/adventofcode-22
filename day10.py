#!/usr/bin/python3
import fileinput

X = 1
cycle = 1

strength_sum = 0
row = ''

def tick():
    global cycle, strength_sum, X, row
    sprite = ( (X-1) <= ((cycle+39)%40) and (X+1) >= ((cycle+39)%40) )
    row += '#' if sprite else '.'
    if cycle % 40 == 0:
        print(row)
        row = ''

    if (cycle + 20) % 40 == 0:
        strength_sum += cycle * X
    cycle += 1

for line in fileinput.input():
    line = line.strip()

    if line.startswith('noop'):
        tick()
        continue

    if line.startswith('addx'):
        V = int(line.split(' ')[1])
        tick()
        tick()
        X += V

print(strength_sum)