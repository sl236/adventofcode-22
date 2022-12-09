#!/usr/bin/python
import fileinput

fs = {}
path = [fs]

for line in fileinput.input():
    line = line.strip()

    if line == '$ cd /':
        path = [fs]
        continue

    if line == '$ ls':
        continue

    if line == '$ cd ..':
        path = path[:-1]
        continue

    if line.startswith('$ cd '):
        path.append( path[-1][line[5:]] )
        continue

    if line.startswith('dir '):
        name = line[4:]
        if name not in path[-1]:
            path[-1][name] = {}
        continue

    size, name = line.split(' ')
    path[-1][name] = int(size)

ts = 0
sizes = []
available = 70000000

def dump(f, indent = ''):
    global ts
    size = 0
    for key in sorted(f):
        if isinstance(f[key], dict):
            print("{}{}".format(indent, key))
            ds = dump(f[key], indent + ' ')
            size += ds
            print("{} -- {}".format(indent, ds))
        else:
            print("{}{} {}".format(indent, key, f[key]))
            size += f[key]
    if(size <= 100000):
        ts = ts + size
    sizes.append(size)
    return size

used = dump(fs)

print("part1:", ts)

needed = 30000000 - (available-used)
for s in sorted(sizes):
    if s >= needed:
        print("part2:", s)
        break