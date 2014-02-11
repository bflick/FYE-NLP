from nltk.stem.porter import *
from nltk.corpus.reader.wordnet import ADJ, ADJ_SAT, ADV, NOUN, VERB

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
    def getStem( taggedWord ):
        pStem = PorterStemmer()
        stem = pStem.stem( taggedWord[0] )
        return stem
