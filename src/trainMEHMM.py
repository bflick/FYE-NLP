#!/bin/python
import nltk.classify.maxent as mehmm
import itertools
from nltk.corpus import brown
import nlp_utils
import math
import pickle
import string
import sys

tags = ['SYM', ',', "'", '``', '.', '(', ')', ':',
        'SC', 'CC', 'DT', 'EX', 'IN',
        'JJ', 'MD', 'NN', 'PDT', 'POS', 'PRP',
        'RB', 'RP', 'TO', 'VB', 'WDT', 'WP', 'WRB',
        '$', '--', 'LS', 'CD', 'FW', 'UH', '-NONE-']

"""
ment-ed, ment-ion, ment-ion-ing, ment-ion-ed
"""
derivational_endings = ['ing', 'ment', 'ion', 'ness', 'ify', 'ly', 'ate', 'ize']
#'er', 'en', 'ens', 'est', 'ested',
"""'ed', 'ings', 'ied', 'ments', 'edness', 'ation', 'al', #'alism',
'cian', 'er', 'ism', 'ist', 'sion', 'y', 'able', 'ies'
'ary', 'ful', 'fy', 'fied', 'ify', 'ly', 'ate', 'ize', #'ability',
'ions', 'ness','nesses','nance','nances','ity','ities']"""

INF = float('inf')    # infinity !!!
NEG_INF = float('-inf')
M_LN2 = 0.69314718055994530942
letters = [chr(x) for x in xrange(ord('a'), ord('z') + 1)]

def ln(value):
    if (value == 0.0):
        return NEG_INF
    else:
        return math.log(value)
    
# calculate log(exp(left) + exp(right)) more accurately
# based on http://www.cs.cmu.edu/~roni/11761-s12/assignments/__log_add.c
def log_add(left, right):
    if (right < left):
        return left + math.log1p(math.exp(right - left))
    elif (right > left):
        return right + math.log1p(math.exp(left - right))
    else:
        return left + M_LN2

def createEncoding():
    encoding_labels = tags
    """['capitol',
    #'starting',
    'contains_punct',
    'ptbtag+',
    'before',
    'after',
    'ending']"""

    encoding_size = 0
    encoding_mapping = {}
    for i in xrange(0, len(tags)):
        encoding_mapping[(tags[i], tags[i], tags[i])] = i
#        encoding_mapping[('preceded_by_'+tags[i], tags[i], 'bi-tag')] = i + 1
#        encoding_mapping[('preceded_by2x_'+tags[i], tags[i], 'tri-tag')] = i + 2

#    encoding_size = len(encoding_mapping)
#    for i, ending in enumerate(derivational_endings):
#        encoding_mapping[('ends_with_'+ending), ending, 'ending'] = encoding_size + i

    encoding_size = len(encoding_mapping)
#    encoding_mapping[('cap', True, 'capitol')] = encoding_size
#    encoding_mapping[('starts', True, 'starting')] = encoding_size + 1
#    encoding_mapping[('punct', True, 'contains_punct')] = encoding_size + 2
#    encoding_size = len(encoding_mapping)

    mehmmEncoding = mehmm.GISEncoding(encoding_labels, encoding_mapping, unseen_features=True)
    train_toks = []
    sentCount = 0
    with open('../assets/retaggedCorpus.txt') as f:
        for ln in f:
            ln = ln.replace('\n', '')
            splitted = ln.strip().split()
            for i, tAndP in enumerate(splitted):
                (tkn, pos) = tuple(tAndP.split('_'))
                features = {pos: pos}
                """'capitol': lambda x: True if tkn[0] in string.ascii_uppercase else False,
                #'starting': lambda x: True if i==0  else False,
                #'contains_punct': lambda x: True if any((c in tkn) for c in string.punctuation) else False,"""

                """if i > 0:
                    features['bi-tag'] = splitted[i-1].split('_')[1]
                else:
                    features['bi-tag'] = '-NONE-'

                if i > 1:
                    features['tri-tag'] = splitted[i-2].split('_')[1]
                else:
                    features['tri-tag'] = '-NONE-'

                for end in derivational_endings:
                    features['ending'] = ''
                    if tkn.endswith(end):
                        features['ending'] = end
                """
                train_toks.append((features, tkn.lower()))
                sentCount += 1
                if sentCount == 2500:
                    break

    mehmmClassifier = mehmm.MaxentClassifier.train(train_toks, algorithm='GIS', encoding=mehmmEncoding, labels=encoding_labels)
    weights = mehmmClassifier.weights()
    pickle.dump((mehmmEncoding, weights), open('../assets/MEHMModel.pickle', 'wb'))

if __name__ == '__main__' :
    createEncoding()
