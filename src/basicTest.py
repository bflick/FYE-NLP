from nltk.tag import pos_tag
from sentence import sentence
import nlp_utils
from word import word

def tagAndStem( lis ):
    taggedW = pos_tag( lis )
    w = []
    for x in taggedW:
        print x
        w.append(word.getTaggedStem(x))
    return w

listW = tagAndStem('I\'ve got some crazy fishing stories'.split())
print listW
s = word.getStem('haven\'t')
print s


print tagAndStem('don\'t bother me with your tall tales .'.split())

print tagAndStem('all\'s fair in love and war'.split())
print tagAndStem('ask me no questions and I\'ll tell you no lies'.split())
print tagAndStem('everything\'s copasetic'.split())
print tagAndStem('dot the i\'s and cross the t\'s'.split())

cl = 'Have a cow'.split()
s = 'she was having a cow'.split()
print nlp_utils.clicheIntersection(s, cl)

"""
k = ['Yabba','dabba','doo','!']
print nlp_utils.removeListPunct(k)
j = [['i','have', 'a','bad','feeling','about','this','.'],['Let','us','pray','.']]
print nlp_utils.removeListPunct(j)
print j
j.append(k)
print nlp_utils.removeListPunct(j)
print j
"""
"""
s0 = sentence('She is as horny as a three balled balloon .'.split())
c = ['as horny as a three balled balloon', 'what the fook']
print s0.containsCliche(c)
"""
