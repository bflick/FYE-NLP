#! /usr/bin/python

from nltk import tokenize
import os
import sys
import utilspackage as util

"""
    First Year English - Natural Language Processing
"""

def main() :
    filePath = '../FYE-TEXT/101/'
    parse_folder( filePath )
    filePath = '../FYE-TEXT/102/'
    parse_folder( filePath )

def parse_folder( dirPath ) :
    textFiles = os.listdir( dirPath )
    for assignmentName in textFiles :
        print 'Assignment Filename = ', assignmentName
        assignment = util.openFileReturnString( dirPath + assignmentName )
        print_sentences( assignment )

def print_sentences( assignment ) :
    paragraphs = assignment.split( '\n\n' )
    for newPara in paragraphs :
        sentences = tokenize.sent_tokenize( newPara )
        for completeThought in sentences :
            print completeThought
        print '\n'
    print '\n'
    return

if __name__ == '__main__' :
    main()
