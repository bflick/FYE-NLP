import nltk
import nltk.corpus

taggedWords = nltk.corpus.brown.tagged_sents(categories='fiction')[:500]

filePath = '../FYE-TEXT/102/'
draftReader, finalReader = parse_folder( filePath )
numFiles = len( os.listdir( filePath ))

assert numFiles % 2 == 0

finalIdsSortedList = finalReader.fileids().sort()
draftIdsSortedList = draftReader.fileids().sort()
for i in range( numFiles / 2 ):
    final = finalReader.paras( finalIdsSortedList[i] )