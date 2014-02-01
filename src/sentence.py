from nltk.tag import pos_tag

class sentence( object ):

	@property
	def words( self ):
		return self.wordList

	@property
	def taggedWords( self ):
		return self._taggedWords

	@property
	def rawText( self ):
		rawText = ''
		rt_ind = 0
		punctuation = set('.,?:;"\'`!')
		for tkn in self.words:
			if any((c in tkn) for c in punctuation) or rt_ind == 0:
				rawText += tkn
			else:
				rawText += ' ' + tkn
			rt_ind += 1
		return rawText

	def __init__( self, listOfTokens ):
		self.wordList = listOfTokens
		self.index = 0
		self._taggedWords = []
		tgdWords = pos_tag( listOfTokens )
		for w in tgdWords:
			self._taggedWords.append( w )

	def __iter__( self ):
		return self

	def next( self ):
		ret = ''
		if self.index == len(self.words):
			raise StopIteration

		ret = self.wordList[self.index]
		self.index += 1
		return ret
