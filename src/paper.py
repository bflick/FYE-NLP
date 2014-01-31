import nltk.metrics.distance.edit_distance as diff

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

	def __init__( self, pList ):
		for p in pList:
			self.paraList.append( paragraph( self, p ))

	def doDiff( self, other ):
		editDistance = diff( self.rawText, other.rawText )
		return editDistance

	def findNewSents( self, other ):
		newSentenceIndices = [] # list of tuples containing paragraphm and sentence index
		if len(self.paras) < len(other.paras):
			return other.findNewSents( self )

		for i, p1, p2 in enumerate(zip( self.paras, other.paras )):
			for j, s2 in enumerate( p2 ):
				if not p1.contains( s2 ):
					newSentenceIndices.append( (i, j) )

		return newSentenceIndices
