#!/usr/bin/python
import fileinput, re, itertools, functools

valves = {}

class Valve(object):
    def __init__(self, name, rate, dests):
        self.name = name
        self.rate = rate
        self.dests = dests
        self.distances = {}

    def __str__(self):
        return "{}: {} -- {}".format(self.name, self.rate, self.dests)

maxrate = 0
for line in fileinput.input():
    m = re.search('Valve ([A-Z][A-Z]) has flow rate=(-?[0-9]+); tunnels? leads? to valves? (.+)', line)
    if not m:
        print(line)
        continue

    line = line.strip()
    name, rate, dests = m.group(1,2,3)
    maxrate += int(rate)
    valves[name] = Valve(name, int(rate), dests.strip().split(', '))

def dist( src, dest ):
    curr = set()
    curr.add(src)
    dist = 1
    while dest not in curr:
        dist += 1
        reachable = curr.copy()
        for node in curr:
            for d in valves[node].dests:
                reachable.add(d)
        curr = reachable
    return dist

for valve in valves:
    valves[valve].distances = { dest: dist(valve, dest) for dest in valves if dest != valve }

def solve(actors, unopened, released, rate, tick, limit):
    global seen, global_best

    new_tick = min(actor[1] for actor in actors)
    released += rate * (new_tick - tick)
    tick = new_tick

    if tick >= limit:
        if global_best < released:
            global_best = released
        global_best = max(global_best, released)
        return

    projection = released + maxrate * (limit - tick)
    if projection < global_best:
        return

    k = (tuple(sorted(actors[0] for actor in actors)), tuple(sorted(unopened)))
    if seen.get(k, 0)>projection:
        return
    seen[k] = projection

    for actor in actors:
        if actor[1] == tick:
            unopened = tuple( v for v in unopened if v != actor[0] )
            rate += valves[actor[0]].rate

    if not unopened:
        released += rate * (limit-tick)
        if global_best < released:
            global_best = released
        return

    moveset = []
    for idx, actor in enumerate(actors):
        if actor[1] > tick:
            moveset.append([actor])
            continue

        moves = []
        for cand in unopened:
            new_tick = tick + valves[actor[0]].distances[cand]
            if new_tick <= limit:
                moves.append( (cand, new_tick) )
        moves.append( (idx, limit) )
        moveset.append(moves)

    for combo in itertools.product( *moveset ):
        if len(set(actor[0] for actor in combo)) < len(actors):
            continue
        solve( combo, unopened, released, rate, tick, limit )


useful_valves = tuple(sorted(v for v in valves if valves[v].rate > 0))
seen = {}
global_best = -1
solve([('AA', 0)], useful_valves, 0, 0, 0, 30)
print("Part 1: {}".format(global_best))

seen = {}
global_best = -1
solve([('AA', 0), ('AA', 0)], useful_valves, 0, 0, 0, 26)
print("Part 2: {}".format(global_best))
