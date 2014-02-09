from nltk.tag import pos_tag
from word import word
import logging
import nlp_utils
from nltk.util import ngrams

class sentence( object ):

    logging.basicConfig(filename='../Sentence.log',level=logging.DEBUG)

    """
        properties accessible in the form 'sentenceObject.property'
    """
    @property
    def rawText( self ):
        rawText = ''
        rt_ind = 0
        punctuation = set('.,?:;"\'`!()')
        for tkn in self.words:
            if any((c in tkn) for c in punctuation) or rt_ind == 0:
                rawText += tkn
            else:
                rawText += ' ' + tkn
            rt_ind += 1
        return rawText + ' '

    @property
    def size( self ):
        return self._size

    @property
    def taggedWords( self ):
        return self._taggedWords

    @property
    def words( self ):
        return self.wordList

    """
        Constructor:
        @param 'listOfTokens' - a list of strings i.e. ['Rub','my','back','.']
    """
    def __init__( self, listOfTokens ):
        self.wordList = listOfTokens
        self.index = 0
        self._size = 0
        self._taggedWords = []
        tgdWords = pos_tag( listOfTokens )
        for w in tgdWords:
            self._taggedWords.append( w )
            self._size += 1
    """
        Iterator:
        Allows for the objects use in a for each loop
    """
    def __iter__( self ):
        return self

    """
        next
        Necessary to access rawText in a for each loop
        implied call with in a for each loop
    """
    def next( self ):
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
    def containsCliche( self, clicheList ):
        #print self.words
        for c in clicheList:
            cList = c.split()
            #print cList
            nGramList = ngrams(nlp_utils.removeListPunct(self.words), len(cList) + 1 )
            for ngram in nGramList:

                cols = len(ngram) + 1
                rows = len(cList) + 1
                mat = [[0 for j in range(cols)] for i in range(rows)]
                for i in range(rows):
                    mat[i][0] = i
                for j in range(cols):
                    mat[0][j] = j

                lastEntry = None
                for i in range(1, rows):
                    for j in range(1, cols):
                        if ngram[j-1] == cList[i-1]:
                            mat[i][j] = mat[i-1][j-1]
                        else:
                            mat[i][j] = min(mat[i-1][j]+1, mat[i][j-1]+1, mat[i-1][j-1]+1)
                        if i == rows - 1 and j == cols - 1:
                            lastEntry = mat[i][j]
                if lastEntry != None and lastEntry <= 1:
                    print ' '.join( ngram )
                    print ' '.join( cList )+'\n'
                    return True
        return False

    """
        wordDiff
        @param 'other' - another sentence object
        @returns the number of words removed and added
    """
    def wordDiff( self, other ):
        cols = self.size + 1
        rows = other.size + 1
        matrix = [[0 for j in range(cols)] for i in range(rows)]

        # not sure whether the range should start at 1 or not
        for i in range(1, rows):
            matrix[i][0] = i
        for j in range(1, cols):
            matrix[0][j] = j
#        self.display( matrix )

        for i in range(1, rows):
            for j in range(1, cols):
                thisWord = word.getStem( self.taggedWords[j-1] )
                otherWord = word.getStem( other.taggedWords[i-1] )
#                logging.info('comparing '+thisWord+' and '+otherWord)
                if thisWord == otherWord:
                    matrix[i][j] = matrix[i-1][j-1]
                else:
#                    logging.debug(thisWord+' is not '+otherWord)
                    deletion = matrix[i-1][j] + 1
                    insertion = matrix[i][j-1] + 1
                    substitution = matrix[i-1][j-1] + 2
                    matrix[i][j] = min(insertion, deletion, substitution)
#            logging.debug('\nAfter row '+str(i))
#            self.display( matrix )
        return matrix[rows - 1][cols - 1]


    def display( self, mat ):
        printString = ''
        for row in range(len(mat)):
                printString += '  ' + ' '.join(str(mat[row])) + '\n'
        logging.debug('\n' + printString + '\n')



