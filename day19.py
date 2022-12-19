#!/usr/bin/python
import fileinput, re, itertools, functools, copy

blueprints = []
items = ['geode', 'obsidian', 'clay', 'ore']
maxcosts = [0, 0, 0, 0]
GEODE = items.index('geode')

class Cost(object):
    def __init__(self, k, v):
        self.what = k
        self.count = v

    def __str__(self):
        return "{} {}".format(self.count, items[self.what])

for line in fileinput.input():
    line = line.split(':')[1].strip()
    if not line:
        continue

    curr = []
    for entry in line.split('.'):
        m = re.match(r'Each (\S+) robot costs (.+)', entry.strip())
        if not m:
            continue
        key, costs = m.group(1, 2)
        if key not in items:
            items.append(key)
        key = items.index(key)

        while(len(curr) <= key):
            curr.append([])
        for cost in costs.split(' and '):
            v, k = cost.split(' ')

            if k not in items:
                items.append(k)
            k = items.index(k)

            maxcosts[k] = max(int(v), maxcosts[k])
            curr[key].append(Cost(k, int(v)))

    if curr:
        blueprints.append(curr)

def cost(blueprint, limit):

    seen = {}
    stats = {'visited':0, 'pruned':0 }

    def visit(tick, owned, rates, best):
        left = (limit-tick)
        best = max(best, owned[GEODE] + rates[GEODE] * left)
        if tick >= limit:
            return best

        projected = best + (left *(left+1))//2
        if projected < best:
            return best

        stats['visited'] += 1
        key = tuple(owned[idx]+rates[idx]*left for idx in range(len(owned)))
        prev = seen.get(key, None)
        if prev and prev[0] <= tick:
            stats['pruned'] += 1
            return best
        seen[key] = (tick, best)

        builds = []

        for recipeidx, recipe in enumerate(blueprint):
            if recipeidx and rates[recipeidx] >= maxcosts[recipeidx]:
                continue
            buildtime = 1
            for cost in recipe:
                if owned[cost.what] < cost.count:
                    if rates[cost.what] == 0:
                        buildtime = None
                        break
                    needed = cost.count - owned[cost.what]
                    rate = rates[cost.what]
                    buildtime = max(buildtime, 1 + (needed // rate) + (0 if needed % rate == 0 else 1))

            if not buildtime or (tick+buildtime) >= limit:
                continue

            builds.append((recipeidx, recipe, buildtime))

        for recipeidx, recipe, buildtime in builds:
            rowned = [(count + rates[idx]*buildtime) for idx, count in enumerate(owned)]
            for cost in recipe:
                rowned[cost.what] -= cost.count

            rrates = list(rates)
            rrates[recipeidx] += 1

            best = max( best, visit(tick+buildtime, tuple(rowned), tuple(rrates), best) )

        return best

    owned_ = tuple(0 for _ in range(len(items)))
    rates_ = tuple((1 if items[idx] == 'ore' else 0) for idx in range(len(items)))
    result = visit( 0, owned_, rates_, 0 )
    #print(stats)
    return result

quality = 0
for idx in range(len(blueprints)):
    c = cost(blueprints[idx], 24)
    quality += (idx+1)*c

print("Part 1: {}".format(quality))

quality = 1
for idx in range(3):
    c = cost(blueprints[idx], 32)
    print("{}: {} ({})".format(idx+1, c, ((idx+1)*c)))
    quality *= c
print("Part 2: {}".format(quality))
