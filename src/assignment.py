from paper import paper
import nlp_utils

class assignment(object) :

    """
        properties accessible in the form 'assignmentObject.property'
    """
    @property
    def draft(self):
        return self.draftPaper

    @property
    def final(self):
        return self.finalPaper

    @property
    def numEdits(self):
        return self.wordDifference()

    @property
    def score(self):
        return self._score

    @property
    def thesis(self):
        return self._thesis

    @score.setter
    def score(self, val):
        self._score = val

    @thesis.setter
    def thesis(self, ths):
        self._thesis = ths

    """
        Constructor:
        @param 'draft' - a list of lists of lists of tokens i.e. a list of paragraphs
        @param 'final' - same as above
    """
    def __init__(self, draft, final):
        self.draftPaper = paper(draft)
        self.finalPaper = paper(final)
        self._score = 'unscored'

    """
        doDiff
        @returns - number of character edits
    """
    def doDiff(self):
        return self.final.doDiff(self.draft)

    """
        customEditDist
        @returns - number of word edits
    """
    def wordDifference(self):
        return nlp_utils.wordDiff(self.final.getWords(), self.draft.getWords())

    """
        draftFinalDist
        @return the text mining distance referred to in Cyril and Dominique Labbe`'s paper
        'Duplicate and Fake Publications in Scientific Literature: How many SCIgen papers in Computer Science?'
    """
    def draftFinalDist(self):
        return nlp_utils.iDist(self.draft.getWords(), self.final.getWords())

    """
        getNewSents
        @return a list of indexes of sentences in the final that do not appear in the draft
    """
    def getNewSents(self):
        return self.draft.findNewSents(self.final)
