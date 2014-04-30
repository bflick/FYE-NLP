import nltk.metrics.distance as diff
from nltk.stem.wordnet import WordNetLemmatizer
import nlp_utils
from paragraph import paragraph
from word import word

class paper(object):
    """
        properties accessible in the form 'assignmentObject.property'
    """
    @property
    def paras(self):
        return self.paraList

    @property
    def rawText(self):
        rawText = ''
        for p in self.paraList:
            rawText += p.rawText + '\n'
        return rawText

    @property
    def size(self):
        return self.numParas

    """
        Constructor:
        @param 'pList' - a list of lists of lists of strings
    """
    def __init__(self, pList):
        self.numParas = len(pList)
        self.paraList = []
        for p in pList:
            self.paraList.append(paragraph(self, p))

    """
        getWords
        @return the listing of words/tokens in the paper
    """
    def getWords(self):
        words = []
        for p in self.paras:
            for s in p.sentences:
                for w in s.words:
                        words.append(w)
        return words


    """
        doDiff
        @param 'other' - another paper object
        @return the number of character edits
        #TODO there is an issue with this because sentence.rawText is accumulated
              for self.rawText and there is some dependency on accurate tagging
    """
    def doDiff(self, other):
        editDistance = diff.edit_distance(self.rawText, other.rawText)
        return editDistance

    """
        findCliches - checks for cliches in sententences excluding those containing quotes
        @return list of sentence locations which contain cliches as tuple;
                 i.e. (para, sent, word, cliche) first 3 are positions, and the last is
                      the cliche that seems to have been found.
    """
    def findCliches(self):
        sentLocs = []
        cliches = nlp_utils.openFileReturnTokens('../assets/cliches.txt', delim='/')
        for i, p in enumerate(self.paras):
            for j, s in enumerate(p.sentences):
                clicheAt = s.containsCliche(cliches)
                if clicheAt != None:
                    sentLocs.append((i, j, clicheAt[0], clicheAt[1]))
        return sentLocs

    """
       findPassives - finds a list of locations of sentences containing passive voice
       @return list of sentence locations which use passive voice as tuple;
                 i.e. (paragraph, sentence)
    """
    def findPassives(self):
        sentLocs = []
        for i, p in enumerate(self.paras):
            for j, s in enumerate(p.sentences):
                if s.isPassive():
                    sentLocs.append((i, j))
        return sentLocs

    """
        findNewSents
        @param 'other' - another paper object
        @return integer list of new sentences
    """
    def findNewSents( self, other ):
        newSentenceIndices = [] # list of tuples containing paragraph and sentence index
        for p1 in self.paras:
            for i, p2 in enumerate(other.paras):
                for j, s2 in enumerate(p2.sentences):
                    if not p1.contains(s2):
                        newSentenceIndices.append((i, j))

        return newSentenceIndices

    """
        findNominalizations
        This depends somewhat on accurate tagging of sentences by NLTK.
        The function looks through each word in the paper returns a list of
        nominalizations that are surrounded by a determiner and a preposition,
        along with the corresponding positions in the paper.
        @param nomList - list of non-derivational nominalizations
        @param nomBlacklist - list of NOT nominalizations with endings that are usually nominalizations
        @return list of the form - [(para, sent, word, nominal phrase),...]
                where the word is the position in the (para, sent) that the nominalization occurs
    """
    def findNominalizations(self, nomList, nomBlacklist):
        nomList = []
        lemm = WordNetLemmatizer()
        for i, p in enumerate(self.paras):
            for j, s in enumerate(p.sentences):
                for k, (tkn, pos) in enumerate(s.taggedWords):
                    singular = lemm.lemmatize( tkn )
                    if len(s.taggedWords) > k + 1 and k - 1 > 0 and word.isNominal( singular, nomList, nomBlacklist ):
                        if pos.startswith( 'N' ) and s.taggedWords[k - 1][1] == 'DT':
                            if s.taggedWords[k + 1][1] == 'IN':
                                nomList.append( (i, j, k, s.taggedWords[k - 1][0] + ' ' + tkn + ' ' + s.taggedWords[k + 1][0]) )
        return nomList

    """
        sentDiff
        a edit distance by sentence measure. Sentence objects have and "__eq__"
        function which returns True if the difference is above a threshold, and False otherwise.
        This is intended to be a more robust "findNewSents" function, that only
        returns the number of new sentences.
    """
    def sentDiff(self, other):
        cols = self.size + 1
        rows = other.size + 1
        matrix = [[0 for j in range(cols)] for i in range(rows)]
        selfSent = [s for p in self.paras for s in p]
        othSent = [s for p in other.paras for s in p]
        for i in range(rows):
            matrix[i][0] = i
        for j in range(cols):
            matrix[0][j] = j
        for i in range(1, rows):
            for j in range(1, cols):
                if selfSent[i] == othSent[j]:
                    matrix[i][j] = matrix[i-1][j-1]
                else:
                    deletion = matrix[i-1][j] + 1
                    insertion = matrix[i][j-1] + 1
                    substitution = matrix[i-1][j-1] + 2
                    matrix[i][j] = min(insertion, deletion, substitution)

        return matrix[-1][-1]


    """
        getAvgComplexity
        accumulates the comlplexity measure for each sentence in a paper, and divides
        total by the number of sentences.
    """
    def getAvgComplexity( self ):
        totalComplexity = 0.0
        avgComplexity = 0.0
        numSents = 0.0
        for p in self.paras:
            for s in p.sentences:
                totalComplexity += float(s.complexity)
                numSents += 1.0
        avgComplexity = totalComplexity / numSents
        return avgComplexity
