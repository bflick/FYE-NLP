from nltk.tag import pos_tag
from word import word
import string
import logging
import nlp_utils
from nltk.util import ngrams

class sentence(object):

    """
        properties accessible in the form 'sentenceObject.property'
    """
    @property
    def complexity(self):
        return self._complexity

    @property
    def rawText( self ):
        specialPunct = ["``",'(']
        lastChar = ' '
        lastPos = ' '
        rawText = ''
        for i, (tkn, pos) in enumerate(self.taggedWords):
            if pos in specialPunct:
                rawText += ' ' + tkn
            else:
                if lastChar[-1] in ["'", '-'] and len(tkn) <= 2:
                    rawText = rawText[:-1]
                rawText += tkn
                if i + 1 < len(self.words) and not nlp_utils.isPunct(self.words[i + 1]):
                    if pos not in specialPunct:
                        rawText += ' '

            lastChar = tkn.strip()

        rawText += ' '
        return rawText

    @property
    def size(self):
        return self._size

    @property
    def taggedWords(self):
        return self._taggedWords

    @property
    def words(self):
        return self.wordList

    """
        Constructor:
        @param 'listOfTokens' - a list of strings i.e. ['Rub','my','back','.']
    """
    def __init__(self, listOfTokens):
        self.wordList = listOfTokens
        self.index = 0
        self._size = 0
        self._complexity = 0.0
        self._taggedWords = []
        tgdWords = pos_tag( listOfTokens )
        for tkn, pos in tgdWords:
            self._taggedWords.append((tkn, pos))
            self._size += 1
            self._complexity += word.getWeight((tkn, pos))


    # sent == other is only meant to be used in 'paper.sentDiff()' function
    def __eq__(self, other):
        diff = self.wordDiff(other)
        if 2 * diff / (other.size + self.size) <= 1 - nlp_utils.similarityTolerance:
            return True
        return False

    """
        Iterator:
        Allows for the objects use in a for each loop
    """
    def __iter__(self):
        return self

    """
        next
        Necessary to access rawText in a for each loop
        implied call with in a for each loop
    """
    def next(self):
        ret = ''
        if self.index == len(self.words):
            raise StopIteration

        ret = self.wordList[self.index]
        self.index += 1
        return ret


    """
        containsCliche - windowed editDist allows for a replacement of a word
        @param clicheList - list to search the sentence for
        @return True if the cliche is contained; False otherwise
    """
    def containsCliche(self, clicheList):
        wordList = nlp_utils.removeList(self.words, list(string.punctuation)+['s','t'])
        for c in clicheList:
            cList = c.split()
            clicheKeywords = nlp_utils.removeList(cList, nlp_utils.clicheBlacklist)
            nGramList = ngrams(wordList, len(cList) + 1)

            for n, ngram in enumerate(nGramList):
                intersect = nlp_utils.clicheIntersection(ngram, clicheKeywords)

                if len(cList) == 0:
                    continue
                # if the cliche has 2 or fewer keywords
                # both must be present in the ngram
                if len(clicheKeywords) <= 2 and len(clicheKeywords) != len(intersect):
                    continue
                # otherwise the ngram may be missing one of the keywords
                elif len(clicheKeywords) - 1 > len(intersect):
                     continue

                cols = len(ngram) + 1
                rows = len(cList) + 1
                mat = [[0 for j in range(cols)] for i in range(rows)]
                for i in range(rows):
                    mat[i][0] = i
                for j in range(cols):
                    mat[0][j] = j

                for i in range(1, rows):
                    for j in range(1, cols):
                        if word.getStem(ngram[j-1]) == word.getStem(cList[i-1]):
                            mat[i][j] = mat[i-1][j-1]
                        else:
                            mat[i][j] = min(mat[i-1][j]+1, mat[i][j-1]+1, mat[i-1][j-1]+1)

                if mat[-1][-1] <= 2:
                    return n, c

        return None

    """
        wordDiff !!! I have kept this here for reference, Levenshtein Algorithm
                 !!! is in the nlp_utils.py file
        @param 'other' - another sentence object
        @return the number of words removed and added
    """
    def wordDiff(self, other):
        selfWords = nlp_utils.removeListPunct(self.words)
        othWords = nlp_utils.removeListPunct(other.words)
        cols = len(selfWords) + 1
        rows = len(othWords) + 1
        matrix = [[0 for j in range(cols)] for i in range(rows)]
        for i in range(rows):
            matrix[i][0] = i
        for j in range(cols):
            matrix[0][j] = j
        for i in range(1, rows):
            for j in range(1, cols):
                thisWord = word.getStem( selfWords[j-1] )
                otherWord = word.getStem( othWords[i-1] )
                if thisWord == otherWord:
                    matrix[i][j] = matrix[i-1][j-1]
                else:
                    deletion = matrix[i-1][j] + 1
                    insertion = matrix[i][j-1] + 1
                    substitution = matrix[i-1][j-1] + 2
                    matrix[i][j] = min(insertion, deletion, substitution)

        return matrix[-1][-1]

    """
        isPassive
        @return True 
    """
    def isPassive(self):
        ret = False
        count = 0
        conjugates = ["be", "was", "were", "been", "is", "being", "are", "got", "gotten", "had gotten"]
        pastPart = "VBN"
        det = "DT"

        for token, pos in self.taggedWords:
            if pos == pastPart and self.taggedWords[self.taggedWords.index((token,pos))-1] != det:
                index = self.taggedWords.index((token, pos))
                for word in self.words:
                    if word in conjugates:
                        if self.words.index(word) >= index - 2:
                            count += 1
                            break

                count += 1
                break
        if count >= 2:
            ret = True

        return ret
