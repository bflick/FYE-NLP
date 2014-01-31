import os
import utilspackage as util

class assignment( object ) :

    @property
    def draft( self ):
        return self.draftPaper

    @property
    def final( self ):
        return self.finalPaper

    @property
    def numEdits( self ):
        return self.doDiff()

    @property
    def score( self ):
        return self._score

    @property
    def thesis( self ):
        return self._thesis

    @draft.setter
    def draft( self, draftParas ):
        self.draftPaper = paper( draftParas )

    @final.setter
    def final( self, finalParas ):
        self.finalPaper = paper( finalParas )

    @score.setter
    def score( self, val ):
        self._score = val

    @thesis.setter
    def thesis( self, ths ):
        self._thesis = ths

    def __init__( self, draft, final ):
        self.draftPaper = draft
        self.finalPaper = final
        self._score = 'unscored'

    def doDiff( self ):
        return self.final.diff( self.draft )
