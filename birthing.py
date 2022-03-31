from numpy.random import choice
from random import choice as rchoice, randint
import pandas as pd
from numpy.random import choice
from random import choice as rchoice
import json
import numpy as np
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# print out during development
# verbose = True
verbose = False

# set some important global parameters
NO_NATIONS = 100
NAME_MAX = 25
pfx_P = 0.8
sfx_P = 0.8
raritymap = dict(zip(
    ['common', 'uncommon', 'rare', 'legendary'],
    [0.55, 0.25, 0.15, 0.5]))
unionInit = ['Strattia', 'Cumullia', 'Nimbia', 'Cirria', 'Altia']
unionP = [0.2, 0.2, 0.2, 0.2, 0.2]

# names
namesFilename = 'birthing/names.txt'
pfxFilename = 'birthing/prefix.txt'
sfxFilename = 'birthing/suffix.txt'
currencyFilename = 'birthing/currencies.json'
exportsFilename = 'birthing/exports.json'

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
    if len(temp) <= NAME_MAX:
        if temp not in namesPool:
            namesPool.append(temp)

if verbose:
    # print(namesPool)
    print(len(namesPool), 'nations in list')

# load currency raw
f = open(currencyFilename)
curRaw = json.load(f)

curList = []
curPtemp = []
for cR in curRaw:
    curList.append(cR['currency'])
    curPtemp.append(raritymap[cR['rarity']])

curP = [x / sum(curPtemp) for x in curPtemp]
curPool = choice(curList, NO_NATIONS, p=curP)

if verbose:
    blk = ""
    for cc in curList:
        if cc not in curPool:
            blk += cc + " "
    if len(blk) > 0:
        print(len(curPool), 'currenies in list:', blk, 'are not present')
    else:
        print(len(curPool), 'currenies in list, all present')

# load export raw
f = open(exportsFilename)
expRaw = json.load(f)

expList = []
expPtemp = []
for exR in expRaw:
    expList.append(exR['export'])
    expPtemp.append(raritymap[exR['rarity']])

expP = [x / sum(expPtemp) for x in expPtemp]
expPool = choice(expList, NO_NATIONS, p=expP)

if verbose:
    blk = ""
    for ex in expList:
        if ex not in expPool:
            blk += ex + " "
    if len(blk) > 0:
        print(len(expPool), 'exports in list:', blk, 'are not present')
    else:
        print(len(expPool), 'exports in list, all present')

# random Unions - change for the production
unionList = choice(unionInit, NO_NATIONS, p=unionP)
# unionList = list(unionList)

if verbose:
    print(len(unionList), 'unions in list')

nationDicts = {}
for idx in range(NO_NATIONS):
    print(namesPool[idx])
    nationDicts[idx] = {'name': namesPool[idx], 'union': unionList[idx],
                        'currency': curPool[idx], 'primary_export': expPool[idx]}

print(nationDicts)


@app.get("/")
def index():
    return {'name': 'api data set for the Nations of One project'}


@app.get("/{tokenID}")
def get_nation(tokenID: int = Path(None, description="The tokenID of the nation")):
    return nationDicts[tokenID]
