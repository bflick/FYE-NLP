import nltk.metrics.distance as diff
from paragraph import paragraph

class paper( object ):

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

    def __init__( self, pList ):
        self.numParas = len(pList)
        self.paraList = []
        for p in pList:
            self.paraList.append( paragraph( self, p ))

    def doDiff( self, other ):
        editDistance = diff.edit_distance( self.rawText, other.rawText )
        return editDistance

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
