from numpy.random import choice
from random import choice as rchoice
import pandas as pd

# set some important global parameters
NO_NATIONS = 1950
NAME_MAX = 25

# set some global functions


def name_fix(s):
    if s[0] == " ":
        return " " + s.strip()
    else:
        return s.strip()


def passer(s):
    return s


def loadItemsAndProbabilities(filename):
    temp = []
    with open(filename, 'r') as f:
        temp = temp + [passer(line).strip() for line in f]
    items = []
    items_probs = []
    for e in temp:
        a, b = e.split(",")
        items.append(a)
        items_probs.append(float(b))
    return [items, items_probs]


def string_split(s, splitindex):
    return s.split(',')[splitindex].strip()


def load_a_big_bang_file(filename):
    dat = pd.read_csv(filename)
    dat['type'] = [s.strip() for s in dat['type']]
    return dat


def loadItems(filename, isNames=False):
    items = ['']
    with open(filename, 'r') as f:
        items = items + [name_fix(line) for line in f]
    return items


def createName(prefixes, prefix_probability,
               base_names, suffixes, suffix_probability, MAXLENGTH):
    name_not_yet_returned = True
    while name_not_yet_returned:
        nation_prefix = choice(prefixes, 1, p=prefix_probability)
        nation_prefix = nation_prefix[0]
        if nation_prefix != "":
            if nation_prefix[-1] != " ":
                nation_prefix += " "
        nation_basename = rchoice(base_names)

        nation_suffix = choice(suffixes, 1, p=suffix_probability)
        nation_name = nation_prefix + nation_basename + nation_suffix[0]
        if len(nation_name) <= MAXLENGTH:
            name_not_yet_returned = False
    return nation_name


def main():

    # NAMES
    base_names = loadItems('birthing/names.txt')
    pfx = loadItems('birthing/prefix.txt')
    sfx = loadItems('birthing/suffix.txt')

    pct_empty = 0.35
    pfx_prob = [pct_empty]
    pfx_prob += [(1-pct_empty) / (len(pfx)-1)] * (len(pfx)-1)

    pct_empty = 0.98
    sfx_prob = [pct_empty]
    sfx_prob += [(1-pct_empty) / (len(sfx)-1)] * (len(sfx)-1)

    exp, exp_probs = loadItemsAndProbabilities('birthing/exports.txt')
    cur, cur_probs = loadItemsAndProbabilities('birthing/currencies.txt')

    namesPool = []
    while len(namesPool) < NO_NATIONS:
        name = createName(pfx, pfx_prob, base_names, sfx, sfx_prob, NAME_MAX)
        if name not in namesPool:
            namesPool.append(name)

    print(len(namesPool), 'names in the pool')

    for n in namesPool:
        if "L'Isula" in n:
            print(n)


if __name__ == '__main__':
    main()
