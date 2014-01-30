import os
import utilspackage as util

class assignment( object ) :

    @property
    def draft( self ):
        return self.draft

    @property
    def final( self ):
        return self.final

    @property
    def numEdits( self ):
        return self.numEdits

    @property
    def score( self ):
        return self.score

    @property
    def thesis( self ):
        return self.thesis

    @draft.setter
    def setDraft( self, draftParas ):
        self.draft = paper( draftParas )

    @final.setter
    def setFinal( self, finalParas ):
        self.final = paper( finalParas )

    @numEdits.setter
    def setNumEdits( self, edits ):
        self.numEdits = edits

    @score.setter
    def setScore( self, val ):
        self.score = val

    @thesis.setter
    def thesisSetter( self, ths ):
        self.thesis = ths

    def __init__( self, draft, final ):
        self.draftParas = draft
        self.finalParas = final

    def doDiff( self ):
        self.numEdits = self.final.diff( self.draft )