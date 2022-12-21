#!/usr/bin/python
import fileinput, re, itertools, functools, copy

monkeys = {}

def trace(k, l, o, r, result):
    #print("{} = ({} {} {}) : {}".format(k, l, o, r, result))
    return result

ops = {
    '+': lambda a, b: a+b,
    '-': lambda a, b: a-b,
    '*': lambda a, b: a*b,
    '/': lambda a, b: a//b,
}

def make_op(k, l, o, r):
    if k == 'root':
        return (lambda: (trace( k, l, o, r, ops[o](monkeys[l][0](), monkeys[r][0]())),
                         monkeys[l][0](),
                         monkeys[r][0](),
            ))
    return (lambda: trace( k, l, o, r, ops[o](monkeys[l][0](), monkeys[r][0]())))

for line in fileinput.input():
    line = line.strip()
    if not line:
        continue

    k, v = line.split(': ')
    op = v.split(' ')
    if len(op) == 1:
        monkeys[k] = ((lambda c: (lambda: c))(int(op[0])), (int(op[0]),))
    else:
        monkeys[k] = (make_op(k, *op), tuple(op))

result, l, r = monkeys['root'][0]()
print("Part 1: {}".format(result))

def find( curr, target, path ):
    if curr == target:
        return path
    if len(monkeys[curr][1]) == 1:
        return None
    p = find( monkeys[curr][1][0], target, path + [(curr, 0)] )
    if p is None:
        p = find( monkeys[curr][1][2], target, path + [(curr, 1)] )
    return p

path = find('root', 'humn', [])
curr, pidx = path.pop(0)
target = l if pidx else r

inversions = {
    (0, '+'): lambda t, p: t - p,  # x + p == t -> x == t-p
    (0, '-'): lambda t, p: t + p,  # x - p == t -> x == t+p
    (0, '*'): lambda t, p: t / p,  # x * p == t -> x == t/p
    (0, '/'): lambda t, p: t * p,  # x / p == t -> x == t*p

    (1, '+'): lambda t, p: t - p,  # p + x == t -> x == t-p
    (1, '-'): lambda t, p: p - t,  # p - x == t -> x == p-t
    (1, '*'): lambda t, p: t / p,  # p * x == t -> x == t/p
    (1, '/'): lambda t, p: p / t   # p / x == t -> x == p/t
}

while path:
    curr, pidx = path.pop(0)
    l, op, r = monkeys[curr][1]
    other_param = monkeys[l if pidx else r][0]()
    target = inversions[(pidx, op)](target, other_param)


print("Part 2: {}".format(target))

#monkeys['humn'] = ((lambda c: (lambda: c))(target), (target,))
#print("confirm: {}".format(monkeys['root'][0]()))
