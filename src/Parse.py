#! /usr/bin/python

from nltk import tokenize
import os
import sys
import utilspackage as util

"""
    First Year English - Natural Language Processing
"""

def main() :
    filePath = '../justTextENGL101/'
    textFiles = os.listdir( filePath )
    for assignmentName in textFiles :
        print 'Assignment Filename = ', assignmentName
        assignment = util.openFileReturnString( filePath + assignmentName )
        parse( assignment )

def parse( text ) :
    paragraphs = text.split( '\n\n' )
    for newPara in paragraphs :
        sentences = tokenize.sent_tokenize( newPara )
        for completeThought in sentences :
            print completeThought
        print '\n'
    print '\n\n'
    return

if __name__ == '__main__' :
    main()
