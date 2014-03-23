#!/bin/python
import urllib2
from word import word
from bs4 import BeautifulSoup

root = 'http://www.scrabblefinder.com'
sufList = ['ion','ment','ments','ness','nesses','nance','nances','ity','ities']
blackList = set()

for suf in sufList:
    page = 'xxx'
    try:
        page = urllib2.urlopen( root +'/ends-with/' + suf + '/').read()
    except:
        print 'error opening page', root + suf
        continue

    souper = BeautifulSoup( page )

    liTags = souper.findAll('li', {'class' : 'defLink'})
    defLinks = []

    for e in liTags:
        defLinks.append( e.find('a')['href'] )

    for l in defLinks:
        try:
            bsoup = BeautifulSoup( urllib2.urlopen( root + l ))
        except:
            print 'error opening page', root + l
            continue
        defs = bsoup.findAll( 'span', { 'class' : 'definition' })

        # if the definition list doesn't exist, its probably a nominalization
        if( len(defs) == 0 ):
            continue

        ncount = 0
        for d in defs:
            pos = d.find('em')
            #print pos.string
            if pos.string == 'n':
                ncount += 1
                break
        theWord = l.split('/')[-2].lower()
        if ncount == 0 or theWord == word.getStem( theWord ):
            blackList.add( theWord )

print '**********'
#print blackList
for wd in blackList:
   print wd.decode( 'utf-8' )
