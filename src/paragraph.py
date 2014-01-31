#from nltk import tokenize
from __future__ import division
from nltk.corpus import stopwords
import utilspackage as util

class paragraph( object ) :

    @property
    def parent( self ):
        return self.parentPaper

    @property
    def rawText( self ):
        rawText = ''
        for s in sentenceList:
            rawText += s.rawText
        rawText += '\n'
        return rawText

    @property
    def sentences( self ):
        return self.sentenceList

    @property
    def topic( self ):
        return self._topic

    @topic.setter
    def topic( self, value ):
        self._topic = value

    def __init__( self, parent, sList ) :
        self.parentPaper = parent
        self._topic = ''
        self.index = 0
        for s in sList:
            self.sentenceList.append( sentence(s) )

    def __iter__( self ):
        return self

    def next( self ):
        ret = ''
        if self.index == len(sentenceList):
            raise StopIteration

        ret = self.sentences[self.index]
        self.index += 1
        return ret

    def contains( self, needle ):
        matches = 0
        goodwords = 0
        haystack = self.sentenceList
        blacklist = stopwords.words("english")
        blacklist.join([',', '.', '!','?', ':', ';'])
        needle = [x for x in needle if not x in blacklist]
        for sentence in haystack:
            for tkn in sentence:
                if tkn in blacklist:
                    sentence.remove(tkn)
                else:
                    goodwords += 1

        for sentence in haystack:
            for i, tkn in enumerate(sentence):
                for j, x in enumerate(needle):
                    if x is tkn and abs(i - j) < 5:
                        matches += 1

        if matches / goodwords > 0.7:
            return True
        return False

"""
    def parse( self ) :
        raw_sentences = tokenize.sent_tokenize( self.rawString )
        for s in raw_sentences :
            nxt_s = sentence_list( s )
            self.sentences.append( nxt_s )
        # find topic sentence
        # score the paragraph (mix of structures & topic contiuity)


    def find_topic( self ) :
        for n in self.sentences :
            subject_current = word( n.getSubject() )
            subject_thesis = word( self.parent_paper.getThesis().getSubject() )
            if n.structure is 'declarative' and subject_current.equals( subject_topic ) :
                self.topic = n.getSubject()
                break

    def similarity( self, other ) :
        counter = 0
        non_match_index_list = []
        sim_score = 0.0
        for s_this, s_other in zip( self.sentences, other.sentences ) :
            if not s_this.equals( s_other ) :
            non_match_index_list.append( counter )
            counter += 1

        sim_score = sim_total / counter
        return sim_score
        # count sentences
        # look for exact matches
        # find non-matches cosine similarity
        # WHAT DO additional sentences add (clarification)????!!!!
"""