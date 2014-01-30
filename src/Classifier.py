from __future__ import print_function
from nltk import tokenize
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import os
import sys
import re
import utilspackage as util

textDirPath = '../FYE-TEXT/101/'
stopListPath = '../Samples/FirstYearEnglishNLP/stopListNLTK.txt'

def removeStopList( paper ):
	paperNoStopWords = []
	blacklist = util.openFileReturnList( stopListPath )
	newPara = []
	for para in paper:
		newSentence = []
		for sentence in para:
			for word in blacklist:
				sentence = [mt for mt in sentence if mt is not word]
			newSentence = sentence
			newPara.append( newSentence )
		paperNoStopWords.append( newPara )
return paperNoStopWords

def getFilesAsParagraphs( path ):
	papersAsParagraphs = []
	fileNames = os.listdir( path )
	for txtHandle in fileNames:
		fullPath = path + txtHandle
		txt = util.openFileReturnString( fullPath )

		listOfSentences = []
		raw_paragraphs = assignment.split( '\n\n' )
	    for newPara in raw_paragraphs:
	    	sentences = tokenize.sent_tokenize( newPara )
	        listOfSentences.append( sentences )

	    papersAsParagraphs.append( listOfSentences )

    return papersAsParagraphs


def classifyThesis( paper ):
	retDict = {}

	keys = createKeys( paper ) # is a dictionary

	for i, para in enumerate( paper ): # i is paragraph number
		for j, sentence in enumerate( para ): # j is sentence number
			for k, word in enumerate( re.split( '\s', sentence, flags=re.I )): # k is word number

				try:
					retDict['occurance( %d )' % keys[word]] += 1
				except KeyError:
					retDict['occurance( %d )' % keys[word]] = 1

				retDict['position( %d )' % keys[word]].append( {para:i, sentence:j, word:k} )

	return retDict

def createKeys( paper ):
	retDict = {}
	counter = 0
	for para in paper:
		for sentence in para:
			for word in re.split( '\s', sentence, flags=re.I ):
				if word not in retDict:
					retDict[word] = counter
					counter += 1
	return retDict

def main():
	#get files as paragraphs
	#remove stopwords
	#NLTK classify
	reader = PlaintextCorpusReader(textDirPath, '.*')
	numFiles = len(os.listdir(textDirPath))

    # print last sentence of first paragrpah for each paper
	for i in range(numFiles):
		doc = reader.paras(reader.fileids()[i])
			print doc[0][-1]











if __name__ == '__main__' :
    main()




	# for each word in a paragraph
	# how many times does it occur in the paper
	# what are locations of occurance in first paragraph