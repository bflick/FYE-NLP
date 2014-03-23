#!/bin/python
from nltk.corpus import *
from nltk.tag import pos_tag
from sentence import sentence
import nlp_utils
from word import word



def tagAndStem( lis ):
    taggedW = pos_tag( lis )
    w = []
    for t, p in taggedW:
        w.append((t.lower(),p))
    return w

t = brown.tagged_sents() #[:10000]
ntagged = []
vtagged = []
nvtagged = []
j = set()
keepers = {}
#for s in j:
#   t.append(tagAndStem(s))

for s in t:
    for p in s:
        if p[1].startswith('N'):
            ntagged.append(p[0])
        if p[1].startswith('V'):
            vtagged.append(p[0])

nvtagged = nlp_utils.setIntersection(ntagged, vtagged)
for s in t:
    for p in s:
        if p[0] in nvtagged:
            try:
                keepers[p[0]].append(p[1])
            except:
                keepers[p[0]] = [p[1]]

tossers = {}
for k in keepers.keys():
    ncount = 0
    vcount = 0
    count = 0
    for tag in keepers[k]:
        count  += 1
        if tag.startswith('N'):
            ncount += 1
        if tag.startswith('V'):
            vcount += 1
    if vcount > ncount / 2 + 1:
        if  float(ncount) >= 0.2*float(count):
            j.add( k.lower() )
        else:
            tossers[k] = keepers[k]
            del keepers[k]
    elif  ncount > vcount / 2 + 1:
        if float(vcount) >= 0.2*float(count):
            j.add( k.lower() )
        else:
            tossers[k] = keepers[k]
            del keepers[k]
    else:
        tossers[k] = keepers[k]
        del keepers[k]

j = sorted(j)
for x in j:
    print x

"""
for k in tossers.keys():
    for x in nvtagged:
        if word.getStem(k) == word.getStem(x):
            for suf in ['ment','ion','ty','ness']:
                if k.endswith(suf):
                    keepers[k] = tossers[k]
                    print 'added stem match', k, x
"""
#print nvtagged
#print '**************************'
#nlp_utils.printDict('Noun-verb tagged', keepers)
