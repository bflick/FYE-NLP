import sys
from collections import defaultdict
from glob import glob
##
sequence = 0

######################################################################
## CHECK ARGUMENTS
def checkargsatleast(number, message):
    if len(sys.argv) < number:
        print message
        sys.exit(1)

######################################################################
##
def display(rec, dtd):
    s = ""
    for tag in dtd:
        if tag in rec:
            if 'creator' == tag:
                s += '%4d: %s\n' % (sequence, rec[tag])
            elif 'title' == tag:
                s += '%4d: %s\n%4d: ' % (sequence, rec[tag], sequence)
            elif 'subject' == tag:
                s += '%4d: %s\n' % (sequence, rec[tag])
            elif 'filelabel' == tag:
                s += '\n%4d: %s\n' % (sequence, rec[tag])
            else:
                s += '( %s )' % (rec[tag])
    return s

######################################################################
##
def filldtd():
    dtd = list()
    dtd.append("creator")
    dtd.append("title")
    dtd.append("chapter")
    dtd.append("booktitle")
    dtd.append("journal")
    dtd.append("series")
    dtd.append("editor")
    dtd.append("institution")
    dtd.append("organization")
    dtd.append("publisher")
    dtd.append("school")
    dtd.append("howpublished")
    dtd.append("address")
    dtd.append("volume")
    dtd.append("number")
    dtd.append("month")
    dtd.append("year")
    dtd.append("pages")
    dtd.append("note")
    dtd.append("dateentered")
    dtd.append("filelabel") #
    dtd.append("subject")

#    dtd.append("dc") #
#    dtd.append("type")
    return dtd

######################################################################
## do a lookup of term in the record (anywhere) to find a match
def isamatch(keywords, record, matchflag):
    matchresultOR = False
    matchresultAND = True
    for term in keywords:
        if 'everything' == term:
            return True

        localterm = term.lower()
        recordlower = ""
        for key, item in record.items():
            if 'subject' == key:
                sorig = ' '.join(item).split()
            else:
                sorig = item.split()
            for s in sorig:
                recordlower += ' ' + s.lower()

        if recordlower.find(localterm) >= 0:
            matchresultOR = True
        else:
            matchresultAND = False

    if 'AND' == matchflag:
        return matchresultAND
    else:
        return matchresultOR

######################################################################
##
def parsexml(filename, dtd):
    record = defaultdict()
    inputlist = list()
    finput = open(filename)
    for line in finput:
        line = line.strip()
        inputlist.append(line)

    subject = []
    for i in range(0, len(inputlist)):
        line = inputlist[i]
        line = line.strip()
        if line.startswith('<?xml'): continue
        if line.startswith('<dc'): continue
        if line.startswith('<type'): continue
        if line.startswith('</'): continue
        if line.startswith('<'):
            line = line[1:]
            if line.startswith('subject'):
                subject.append(inputlist[i+1])
            else:
                pos = line.index('>')
                tag = line[:pos]
                if tag not in dtd:
                    print "ERROR: invalid tag '" + tag + "'"
                    print display(record, dtd)
                    sys.exit(1)
                record[tag] = inputlist[i+1]

    if 0 == len(subject):
        subject.append('NOKEYWORDS')

    if 'dateentered' not in record:
        record['dateentered'] = '700101'

    record['subject'] = subject

#    for subj in subject:
#        print 'SUBJECT %-20s %-10s %s' % (record['filelabel'],record['dateentered'],subj)

    return record
        
######################################################################
## MAIN PROGRAM STARTS HERE
##
checkargsatleast(5, "usage: a.out HOME/WORK/AIR outfilename AND/OR keywords")

######################################################################
##
dtd = filldtd()
##
if sys.argv[1] == 'HOME':
    directory = "/Users/dabuell/Documents/library/xtfExecutable/tomcat/webapps/xtf/data"
elif sys.argv[1] == 'WORK':
    directory = "/Users/buell/Documents/library/xtfExecutable/tomcat/webapps/xtf/data"
elif sys.argv[1] == 'AIR':
    directory = "/Users/duncanbuell/Documents/library/xtfExecutable/tomcat/webapps/xtf/data"
else:
    print 'ERROR: location not HOME, WORK, or AIR'
    sys.exit(1)
##
if (sys.argv[3] != 'AND') and (sys.argv[3] != 'OR'):
    print 'ERROR: must specify AND or OR'
    sys.exit(1)
matchflag = sys.argv[3]
##
if 'stdout' == sys.argv[2]:
    fout = sys.stdout
else:
    fout = open(sys.argv[2], 'w')
##
fout.write("LOCATION: " + sys.argv[1] + '\n')
keywords = ' '.join(sys.argv[4:])
keywords = keywords.split()
fout.write("KEYWORDS: " + str(keywords)+'\n')
filenames = glob(directory + "/*/*/*.xml")
fout.write("DIRECTORY: " + directory + '\n')
for name in filenames:
    rec = parsexml(name, dtd)
    if isamatch(keywords, rec, matchflag):
        sequence += 1
        fout.write(display(rec, dtd) + '\n')

######################################################################
##
