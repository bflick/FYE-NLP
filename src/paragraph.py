from nltk import tokenize

class paragraph( object ) :

    @property
    def parentPaper( self ):
        return self.parentPaper

    @property
    def rawText( self ):
        rawText = ''
        for s in sentenceList:
            rawText += s
        rawText += '\n'

    @property
    def sentences( self ):
        return self.sentences

    @property
    def topic( self ):
        return self.topic

    @topic.setter
    def topicSetter( self, value ):
        self.topic = value

    def __init__( self, parent, sentenceList ) :
        self.parentPaper = parent
        self.index = 1
        for s in sentenceList:
            sentences.append( sentence(s) )

    def __iter__( self ):
        return self

    def next( self ):
        if self.index == len(sentenceList):
            raise StopIteration
        self.index += 1
        return self.sentences[self.index - 1]

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