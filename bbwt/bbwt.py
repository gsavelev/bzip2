import bbwt.lyndon as lyndon


def cyclic_group_of(w):
    return [w[len(w) - i:] + w[:len(w) - i] for i in range(len(w))]


def bijective_bwt(w):
    """Returns Bijective Bullows-Wheeler Transform of the string w."""
    transformed_w =  bytearray()
    facts = reversed([facts for facts in lyndon.lyndon_factorize(w)])
    facts = sum([cyclic_group_of(fact) for fact in facts], [])
    maxlen = max([len(fact) for fact in facts]) + 1
    repfacts = [(fact, (fact * ((maxlen + len(fact) - 1) // len(fact) + 10))[:maxlen]) for fact in facts]
    repfacts.sort(key=lambda x: x[1])
    for f in repfacts:
        # FIXME bug here
        transformed_w.append(f[0][-1])
    return transformed_w


def bijective_bwt_inv(l):
    """Inverse transform of bijective_bwt()"""
    n = len(l)
    pi = list(range(n))
    f = sorted(l)
    pi = sorted(pi, key=lambda x: l[x])
    used = [False for _ in range(n)]
    lws, origin = [], bytearray()
    start = 0
    while True:
        while start < n and used[start]:
            start += 1
        if start == n:
            break
        w = []
        index = start
        used[index] = True
        while True:
            w.append(f[index])
            index = pi[index]
            used[index] = True
            if index == start:
                break
        lws.append(w)
    lws.sort(reverse=True)
    for lw in lws:
        for w in lw:
            origin.extend(ord(w).to_bytes(1, 'big'))
    return origin


def bijective_bwt_verbose(w):
    facts = list(reversed([facts for facts in lyndon.lyndon_factorize(w)]))
    print(f'Lyndon factorization:')
    print('\n'.join(['  ' + str(f) for f in reversed(facts)]))
    print(f'Reversed lyndon factors:')
    print('\n'.join(['  ' + str(f) for f in facts]))
    facts = sum([cyclic_group_of(fact) for fact in facts], [])
    print(f'Cyclic strings of all factors:')
    print('\n'.join(['  ' + str(f) for f in facts]))
    maxlen = max([len(fact) for fact in facts]) + 1
    repfacts = [(fact, (fact * ((maxlen + len(fact) - 1) // len(fact) + 10))[:maxlen]) for fact in facts]
    print(f'Infinite repitition of all factors:')
    print('\n'.join(['  ' + str(f[1]) + '..' for f in repfacts]))
    print(f'Sort by infinite repitition of all factors:')
    repfacts.sort(key=lambda x: x[1])
    print('\n'.join([f'  {f[0].ljust(maxlen)}({f[1]}..)' for f in repfacts]))
    return ''.join([f[0][-1] for f in repfacts])