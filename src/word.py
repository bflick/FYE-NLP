from nltk.stem.porter import *
from nltk.corpus.reader.wordnet import ADJ, ADJ_SAT, ADV, NOUN, VERB
import string
import re
import nlp_utils

"""
        Penn2POS = {
        'FW':NOUN,
        'JJ':ADJ,
        'JJR':ADJ,
        'JJS':ADJ,
        'NN':NOUN,
        'NNS':NOUN,
        'NNP':NOUN,
        'NNPS':NOUN,
        'PDT':NOUN,
        'PRP':NOUN,
        'PRP$':NOUN,
        'RB':ADV,
        'RBR':ADV,
        'RP':NOUN,
        'VB':VERB,
        'VBD':VERB,
        'VBG':VERB,
        'VBN':VERB,
        'VBP':VERB,
        'VBZ':VERB
    }
"""

class word( object ):

    @staticmethod
    def getTaggedStem( taggedWord ):
        pStem = PorterStemmer()
        stem = ''
        if isinstance(taggedWord, tuple):
            stem = pStem.stem( taggedWord[0] )
        stem = stem.replace('\'','')
        return stem.lower()


    @staticmethod
    def getStem( word ):
        pStem = PorterStemmer()
        stem = ''
        if isinstance(word, str):
            stem = pStem.stem( word )
        stem = stem.replace('\'','')
        return stem.lower()

    @staticmethod
    def isNominal( word, nominals, nomBlacklist ):
        sufList = ['ion', 'ment', 'ness', 'ance', 'ity', 'ions', 'ments', 'ances', 'ities']
        if word in nominals:
            return True
        if word not in nomBlacklist:
            for suf in sufList:
                if word.endswith(suf):
                    return True
        return False

    @staticmethod
    def getWeight( taggedWord ):
        weight = 0.0
        pos = taggedWord[1]
        if nlp_utils.weights.has_key(nlp_utils.normPos(pos)):
            weight = nlp_utils.weights[nlp_utils.normPos(pos)]
        return weight