#!/usr/bin/python
import fileinput

Monkeys = []

KTEST = 'Test'
KSTART = 'Starting items'
KTRUE = 'If true'
KFALSE = 'If false'
KOP = 'Operation'
KITEMS = 'items'
KCOUNT = 'count'

for line in fileinput.input():
    line = line.strip()

    if not line:
        continue
    if line.startswith('Monkey'):
        Monkeys.append({})
        continue
    key, value = line.split(': ')
    value = value.strip()

    if key == KTEST:
        if not value.startswith('divisible by '):
            raise RuntimeError("couldn't parse {}: {}".format(key, value))
        value = int(value[len('divisible by '):])
    elif key == KTRUE:
        if not value.startswith('throw to monkey '):
            raise RuntimeError("couldn't parse {}: {}".format(key, value))
        value = int(value[len('throw to monkey '):])
    elif key == KFALSE:
        if not value.startswith('throw to monkey '):
            raise RuntimeError("couldn't parse {}: {}".format(key, value))
        value = int(value[len('throw to monkey '):])
    elif key == KSTART:
        value = [int(v) for v in value.split(',')]
    elif key == KOP:
        if not value.startswith('new = '):
            raise RuntimeError("couldn't parse {}: {}".format(key, value))
        value = value[len('new = '):]
        value = 'lambda old: (' + value + ')'
        value = (value, eval(value) )
    else:
        raise RuntimeError("couldn't parse {}: {}".format(key, value))

    Monkeys[-1][key] = value

# ----------------

for idx in range(len(Monkeys)):
    Monkeys[idx][KITEMS] = list(Monkeys[idx][KSTART])
    Monkeys[idx][KCOUNT] = 0


for r in range(20):
    for idx in range(len(Monkeys)):
        while Monkeys[idx][KITEMS]:
            Monkeys[idx][KCOUNT] += 1

            item = Monkeys[idx][KITEMS][0]
            Monkeys[idx][KITEMS] = Monkeys[idx][KITEMS][1:]

            item = Monkeys[idx][KOP][1](item) // 3
            dest = KTRUE if (item % Monkeys[idx][KTEST]) == 0 else KFALSE

            Monkeys[Monkeys[idx][dest]][KITEMS].append(item)

def product( x ):
    print(x)
    r = 1
    for item in x:
        r = r * item
    return r

print("Part 1: {}".format(product(sorted([Monkeys[idx][KCOUNT] for idx in range(len(Monkeys))])[-2:])))

# ----------------

modulus = 1
for idx in range(len(Monkeys)):
    Monkeys[idx][KITEMS] = list(Monkeys[idx][KSTART])
    Monkeys[idx][KCOUNT] = 0
    modulus = modulus * Monkeys[idx][KTEST]


for r in range(10000):
    for idx in range(len(Monkeys)):
        while Monkeys[idx][KITEMS]:
            Monkeys[idx][KCOUNT] += 1

            item = Monkeys[idx][KITEMS][0]
            Monkeys[idx][KITEMS] = Monkeys[idx][KITEMS][1:]

            item = Monkeys[idx][KOP][1](item) % modulus
            dest = KTRUE if (item % Monkeys[idx][KTEST]) == 0 else KFALSE

            Monkeys[Monkeys[idx][dest]][KITEMS].append(item)

print("Part 2: {}".format(product(sorted([Monkeys[idx][KCOUNT] for idx in range(len(Monkeys))])[-2:])))
