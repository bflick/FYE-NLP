import os
import utilspackage as util
from paper import paper

class assignment( object ) :

    """
        properties accessible in the form 'assignmentObject.property'
    """
    @property
    def draft( self ):
        return self.draftPaper

    @property
    def final( self ):
        return self.finalPaper

    @property
    def numEdits( self ):
        return self.customEditDist()

    @property
    def score( self ):
        return self._score

    @property
    def thesis( self ):
        return self._thesis

    @score.setter
    def score( self, val ):
        self._score = val

    @thesis.setter
    def thesis( self, ths ):
        self._thesis = ths

    """
        Constructor:
        @param 'draft' - a list of lists of lists of tokens i.e. a list of paragraphs
        @param 'final' - same as above
    """
    def __init__( self, draft, final ):
        self.draftPaper = paper( final )
        self.finalPaper = paper( draft )
        self._score = 'unscored'

    """
        doDiff
        @returns - number of character edits
    """
    def doDiff( self ):
        return self.final.doDiff( self.draft )

    """
        customEditDist
        @returns - number of word edits
    """
    def customEditDist( self ):
        newWords = 0

        if len(self.final.paras) != len(self.draft.paras):
            print 'paragraph numbers differ\n'

        for paraFin, paraDft in zip(self.final.paras, self.draft.paras):
            newWords += paraFin.wordDiff( paraDft )
        return newWords










