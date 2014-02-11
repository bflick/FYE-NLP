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
    for sw in ['as','a','the','is','in','on','at','to','it','of','an']:
        if sw in cliche:
            stopCount += 1

    if len( cList ) <= 3 or '(' in cliche or stopCount >= len(cList)/2:
        countRemoved += 1
    else:
        txt += nlp_utils.removeRawPunct(cliche) + '/'
        countAdded += 1

print(countAdded)
print(countAdded+countRemoved)

newFile =  open( '../Samples/FirstYearEnglishNLP/clichesEdited.txt', 'w')

try:
    print( txt, file = newFile )
finally:
    newFile.close()
