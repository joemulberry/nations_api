from numpy.random import choice
from random import choice as rchoice, randint
import pandas as pd
from numpy.random import choice
from random import choice as rchoice

# set some important global parameters
NO_NATIONS = 1950
NAME_MAX = 25
pfx_P = 0.8
sfx_P = 0.8
MAX_NAME_LENGTH = 25

# define common functions


def makeName(pfx_P, pfxList, namesList, sfx_P, sfxLists, sfxSpaces):

    nationName = ''

    if randint(0, 1) > pfx_P:
        nationName += rchoice(pfxList) + " "

    nationName += rchoice(namesList)

    if randint(0, 1) > sfx_P:
        sfx = rchoice(sfxLists)
        spacer = sfxSpaces[sfxLists.index(sfx)]
        if spacer == 0:
            nationName += sfx
        else:
            nationName += " " + sfx

    return nationName


def main():

    # names
    namesFilename = 'birthing/names.txt'
    pfxFilename = 'birthing/prefix.txt'
    sfxFilename = 'birthing/suffix.txt'

    # load base names
    namesList = []
    with open(namesFilename, 'r') as f:
        namesList = namesList + [line.strip() for line in f]

    # load pfxes
    pfxList = []
    with open(pfxFilename, 'r') as f:
        pfxList = pfxList + [line.strip() for line in f]

    # load sfxes
    sfxLists = []
    sfxSpaces = []
    with open(sfxFilename, 'r') as f:
        for line in f:
            sfxLists.append(line.strip().split(",")[0])
            sfxSpaces.append(int(line.strip().split(",")[1]))

    namesPool = []
    while len(namesPool) < NO_NATIONS:
        temp = makeName(pfx_P, pfxList, namesList, sfx_P, sfxLists, sfxSpaces)
        if len(temp) <= MAX_NAME_LENGTH:
            if temp not in namesPool:
                namesPool.append(temp)

    print(namesPool)
    print(len(namesPool), 'nations in list')

    for n in namesPool:
        if "Oceanic" in n:
            print(n)

    # load surfixes
    # sfxList = []
    # with open(sfxFilename, 'r') as f:
    #     sfxList = sfxList + [line.strip() for line in f]

    # create probabilities

    # function to generate names


if __name__ == '__main__':
    main()
