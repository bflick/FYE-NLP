from __future__ import print_function
import os
import sys
import utilspackage as util

newDest = '../FYE-TEXT/101/'
fileSrc = '../justTextENGL101/'

def cleanSmartQuotes(text):
    text = text.replace("\x91", ' ')
    text = text.replace("\x92", "'")
    text = text.replace('\x94', '"')
    text = text.replace('\x93', '"')
    text = text.replace('\x85', ' ')
    text = text.replace('\xE3', ' ')
    return text

def cleanUp():
	fileNames = os.listdir( fileSrc )
	for txtHandle in fileNames:
		oldPath = fileSrc + txtHandle
		txt = util.openFileReturnString( oldPath )
		txt = cleanSmartQuotes( txt )
		newPath = newDest + txtHandle
		newFile =  open( newPath, 'w')
		try:
			print( txt, file = newFile )
		finally:
			newFile.close()

cleanUp()

newDest = '../FYE-TEXT/102/'
fileSrc = '../justTextENGL102/'

cleanUp()