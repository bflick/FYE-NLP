from nltk.stem.porter import *
from nltk.corpus.reader.wordnet import ADJ, ADJ_SAT, ADV, NOUN, VERB
import string
import re

class word( object ):

    PennTagsToSimplePOS = {
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

    @staticmethod
    def getTaggedStem( taggedWord ):
        pStem = PorterStemmer()
        stem = ''
        if isinstance(taggedWord, tuple):
            stem = pStem.stem( taggedWord[0] )
        if re.match( r'.*\'[a-z]+', stem, re.I ):
            i = stem.index('\'')
            stem = stem[:i]
        stem = stem.replace('\'','')
        return stem.lower()


    @staticmethod
    def getStem( word ):
        pStem = PorterStemmer()
        stem = ''
        if isinstance(word, str):
            stem = pStem.stem( word )
        if re.match( r'.*\'[a-z]+', stem, re.I ):
            i = stem.index('\'')
            stem = stem[:i]
        stem = stem.replace('\'','')
        return stem.lower()
