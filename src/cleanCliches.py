from __future__ import print_function
from nltk.corpus import stopwords
import nlp_utils

cliches = nlp_utils.openFileReturnTokens('../Samples/FirstYearEnglishNLP/cliches.txt', delim='/')

txt = ''
countAdded = 0
countRemoved = 0
for cliche in cliches:
    cList = cliche.split()
    stopCount = 0
#    print(cList)
#    print(cliche)
    for sw in ['as','a','the','is','of','an']:
        if sw in cliche:
            stopCount += 1

    add = 0
    if len(cList) % 2 == 1:
        add = 1

    if len(cList) <= 3 or stopCount >= len(cList)/2:
        countRemoved += 1
    else:
        modCliche = []
        for tkn in cList:
            if tkn.endswith(('.','?','!',',')):
                modCliche.append( nlp_utils.removeRawPunct( tkn ))
            elif tkn.startswith('(') or tkn.endswith(')'):
                pass
            else:
                modCliche.append(tkn)
        print(' '.join( modCliche ))

        txt += ' '.join( modCliche ) + '/'
        countAdded += 1

print(countAdded)
print(countAdded+countRemoved)

newFile =  open('../assets/cliches.txt', 'w')

try:
    print( txt, file = newFile )
finally:
    newFile.close()
