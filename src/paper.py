import nltk.metrics.distance as diff
from nltk.stem.wordnet import WordNetLemmatizer
import nlp_utils
from paragraph import paragraph
from word import word

class paper( object ):

    """
        properties accessible in the form 'assignmentObject.property'
    """
    @property
    def paras( self ):
        return self.paraList

    @property
    def rawText( self ):
        rawText = ''
        for p in self.paraList:
            rawText += p.rawText + '\n'
        return rawText

    @property
    def size( self ):
        return self.numParas

    """
        Constructor:
        @param 'pList' - a list of lists of lists of strings
    """
    def __init__( self, pList ):
        self.numParas = len(pList)
        self.paraList = []
        for p in pList:
            self.paraList.append( paragraph( self, p ))

    def getWords( self ):
        words = []
        for p in self.paras:
            for s in p.sentences:
                for w in s.words:
                        words.append( w )
        return words

    def interDiff( self, another ):
        return nlp_utils.iDist( self.getWords(), another.getWords() )

    """
        doDiff
        @param 'other' - another paper object
        @return the number of character edits
    """
    def doDiff( self, other ):
        editDistance = diff.edit_distance( self.rawText, other.rawText )
        return editDistance

    """
        findCliches - checks for cliches in sententences excluding those containing quotes
        @return list of sentence locations which contain cliches as tuple;
                 i.e. (paragraph, sentence)
    """
    def findCliches( self ):
        sentLocs = []
        cliches = nlp_utils.openFileReturnTokens('../assets/cliches.txt', delim='/')
        for i, p in enumerate( self.paras ):
            for j, s in enumerate(p.sentences ):
                if not '"' in s.words:
                    clicheAt = s.containsCliche( cliches )
                    if clicheAt != -1:
                        sentLocs.append( (i, j, clicheAt[0], clicheAt[1]) )
        return sentLocs

    """
       findPassives - finds a list of locations of sentences containing passive voice
       @return list of sentence locations which use passive voice as tuple;
                 i.e. (paragraph, sentence)
    """
    def findPassives( self ):
        sentLocs = []
        for i, p in enumerate( self.paras ):
            for j, s in enumerate(p.sentences ):
                if s.isPassive():
                    sentLocs.append( (i, j) )
        return sentLocs

    """
        findNewSents
        @param 'other' - another paper object
        @return integer list of new sentences
        #TODO
    """
    def findNewSents( self, other ):
        newSentenceIndices = [] # list of tuples containing paragraphm and sentence index
        if len(self.paras) < len(other.paras):
            return other.findNewSents( self )

        # i can't do this because zip will truncate the shorter paragraph
        for i, (p1, p2) in enumerate(zip( self.paras, other.paras )):
            #print 'p1', p1

            for j, s2 in enumerate( p2.sentences ):
             #   print 's2', s2
                if not p1.contains( s2 ):
                    newSentenceIndices.append( (i, j) )
        return newSentenceIndices

    def findNominalizations( self, nomList, nomBlacklist ):
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
