from nltk.tag import pos_tag

class sentence( object ):

	@property
	def words( self ):
		return self.words

	@property
	def taggedWords( self ):
		return self.taggedWords

	@property
	def rawText( self ):
		rt_ind = 0
		punctuation = set('.,?:;"\'`!')
		for tkn in self.words:
			if any((c in tkn) for c in puntutation) or rt_ind == 0:
				rawText = tkn
			else:
				rawText += ' ' + tkn
		return rawText

	def __init__( self, listOfTokens ):
		self.words = listOfTokens
		self.index = 0
		self.taggedWords = []
		tgdWords = pos_tag( listOfTokens )
		for w in tgdWords:
			self.taggedWords.append( w )

	def __iter__( self ):
		return self

	def next( self ):
