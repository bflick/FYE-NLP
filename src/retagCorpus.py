#!/bin/python
from __future__ import print_function
import sys
import itertools
from nltk.corpus import brown
from nltk.tag import pos_tag
from nltk.util import ngrams
import nlp_utils

#engWords = nlp_utils.openFileReturnTokens('../assets/eng.words')
#engWords = sorted(set([w.lower() for w in engWords]))

nonTags = ['$', '--', 'LS', 'CD', 'FW', 'UH']


tags2Brown ={'SC':['CS'],
             'CC':['CC'],
             'DT':['*', 'AP', 'AP$', 'AP+AP', 'AT',
                   'DT', 'DT$', 'DT+BEZ', 'DT+MD', 'DTI', 'DTS', 'DTS+BEZ', 'DTX'],
             'EX':['EX', 'EX+BEZ', 'EX+HVD', 'EX+HVZ', 'EX+MD'],
             'FW':['FW-*', 'FW+AT', 'FW-AT+NN', 'FW-AT+NP', 'FW-BE', 'FW-BER', 'FW-BEZ',
                   'FW-CC', 'FW-CD', 'FW-CS', 'FW-DT', 'FW-DT+BEZ', 'FW-DTS', 'FW-HV',
                   'FW-CD', 'FW-IN+AT', 'FW-IN+NN', 'FW-IN+NP', 'FW-JJ', 'FW-JJR', 'FW-JJT',
                   'FW-NN', 'FW-NN$', 'FW-NNS', 'FW-NP', 'FW-NPS', 'FW-NR', 'FW-OD', 'FW-PN',
                   'FW-PP$', 'FW-PPL', 'FW-PPL+VBZ', 'FW-PPO', 'FW-PPO+IN', 'FW-PPS', 'FW-PPSS',
                   'FW-PPSS+HV', 'FW-QL', 'FW-RB', 'FW-RB+CC', 'FW-TO+VB', 'FW-UH', 'FW-VB', 'FW-VBD',
                   'FW-VGB', 'FW-VBN', 'FW-VBZ', 'FW-WBT', 'FW-WPO', 'FW-WPS'],
             'IN':['IN', 'IN+IN', 'IN+PPO', 'RP', 'RP+IN'],
             'JJ':['JJ', 'JJ$'],
             'JJR':['JJR', 'JJS+CS' ],
             'JJS':['JJS','JJT'],
             'MD':['MD', 'MD*',  'MD+HV', 'MD+PPSS', 'MD+TO'],
             'NN':['NN', 'NN$', 'NN+BEZ', 'NN+HVD', 'NN+HVZ', 'NN+IN', 'NN+MD', 'NN+NN', 'PN', 'PN$',
                   'PN+BEZ', 'PN+HVD', 'PN+HVZ', 'PN+MD', 'PP$$', 'PPL', 'PPLS', 'PPO', 'PPS', 'PPS+BEZ',
                   'PPS+HVD', 'PPS+HVZ', 'PPS+MD'],
             'NNS':['NNS', 'NNS$', 'NNS+MD'],
             'NNP':['NP', 'NP$', 'NP+BEZ', 'NP+HVZ', 'NP+MD'],
             'NNPS':['NPS', 'NPS$', 'NR', 'NR+MD', 'NR$', 'NRS'],
             'PDT':['ABL', 'ABN', 'ABX'],
             'POS':['S'],
             'PRP':['PPSS', 'PPSS+BEM', 'PPSS+BER', 'PPSS+BER', 'PPSS+BEZ',
                    'PPSS+BEZ*', 'PPSS+HV', 'PPSS+HVD', 'PPSS+MD', 'PPSS+VB'],
             'PRP$':['PP$'],
             'RB':['QL', 'QLP', 'RB', 'RB$', 'RB+BEZ', 'RB+CS'],
             'RBR':['RBR', 'RBR+CS', 'RBT'],
             'RP':['RN'],
             'VB': ['BE', 'BEM', 'BEM*', 'DO', 'DO*', 'HV', 'HV*', 'HV+TO', 'VB', 'VB+AT', 'VB+IN', 'VB+JJ', 'VB+PPO',
                    'VB+RP', 'VB+TO', 'VB+VB'],
             'VBD':['BED', 'BED*', 'DOD', 'DOD*', 'HVD', 'HVD*', 'VBD'],
             'VBG':['BEG', 'HVG', 'VBG', 'VBG+TO'], 
             'VBN':['BEN', 'HVN', 'VBN', 'VBN+TO'],
             'VBP':['BER', 'BER*'],
             'VBZ':['BEZ', 'BEZ*', 'BEDZ', 'BEDZ*', 'DOZ', 'DOZ*', 'HVZ', 'HVZ', 'VBZ'],
             'WDT':['WDT', 'WDT+BER', 'WDT+BER+PP', 'WDT+BEZ', 'WDT+DO+PPS', 'WDT+DOD', 'WDT+HVZ'],
             'WP':['WPO', 'WPS', 'WPS+BEZ', 'WPS+HVD', 'WPS+HVZ', 'WPS+MD'],
             'WP$':['WP$'],
             'WRB':['WRB', 'WRB+BER', 'WRB+BEZ', 'WRB+DO', 'WRB+DOD', 'WRB+DOD*', 'WRB+DOZ', 'WRB+IN','WRB+MD'],
             'SYM':['-None-'],
             'TO':['TO', 'TO+VB'],
             'UH':['UH'],
             'CD':['CD', 'CD$', 'OD'],
             ',': [','],
             "'": ["''"],
             '``':['``'],
             '.': ['.'],
             '(': ['('],
             ')': [')'],
             ':': [':'],
             '--':['--']
             '$':[]
         }


"""tags = ['SYM', ',', "'", '``', '.', '(', ')', ':',
        'SC', 'CC', 'DT', 'EX', 'IN',
        'JJ', 'MD', 'NN', 'PDT', 'POS', 'PRP',
        'RB', 'RP', 'TO', 'VB', 'WDT', 'WP', 'WRB']
"""
#zeroStart = tags[:10] + [tags[18]]

"""SubConj = [
           ['after'], ['how'],
           ['till'], ['\'til'],
           ['although'], ['if'],
           ['unless'], ['as'],
           ['inasmuch'], ['until'],
           ['as','if'], ['in','order'],
           ['that'], ['when'],
           ['as','long','as'],
           ['lest'],['whenever'],
           ['as','much','as'], ['now','that'],
           ['where'], ['as','soon','as'],
           ['provided'], ['wherever'],
           ['as', 'though'],
           ['since'], ['while'],
           ['because'], [['so'],['that']],
           ['before'], ['than'],
           ['even','if'], ['that'],
           ['even','though'],
           ['though']
          ]
"""

tagged_corpus = brown.tagged_sents()

def switchTag(tag):
    for pentag, browntags in tags2Brown.iteritems():
        for btag in browntags:
            if tag == btag:
                return pentag
    tag = tag.split('-')
    singletag = []
    for t in tag:
        singletag += t.split('+')
    for t in singletag:
        if t not in ['TL', 'HL']:
            return t
    print('problem' + tag)
    sys.exit(1)

def retagWithSC(idx, taggedSent):
    ret = taggedSent
    ret[idx] = (ret[idx][0],'SC')
    return ret

def main():
    corpus2 = []
    for i in xrange(len(tagged_corpus)):
        adjustedTaggedSent = []
        for tkn, pos in tagged_corpus[i]:
            if tkn.endswith("'s") and pos.endswith('$'):
                adjustedTaggedSent.append((tkn[:-2], switchTag(pos)))
                adjustedTaggedSent.append(("'s", 'POS'))
            else:
                adjustedTaggedSent.append((tkn, switchTag(pos)))

        corpus2.append(adjustedTaggedSent)

    with open('../assets/retaggedCorpus.txt','w') as f:
        for sent in corpus2:
            for tkn, pos in sent:
                f.write(tkn + '_' + pos + ' ')
            f.write('\n')
        
if __name__ == '__main__' :
    main()


"""
"""
    
""" hohmm = HOHMM(1, engWords, tags, retStartProbs(), retEmisProbs(), retTransProbs(), corpus2)
    hohmm.baumWelch()
    hohmm.write('../assets/modelTest.txt')

def retStartProbs():
    startProbs = []
    for pos in tags:
        if pos in zeroStart:
            startProbs.append(0)
        else:
            startProbs.append(1.0/(float(len(tags))-float(len(zeroStart))))
    return startProbs

def retTransProbs():
    transProbs = []
    for pos1 in tags:
        transProbs.append(list())
        for pos2 in tags:
            transProbs[-1].append(1.0/float(len(tags)))
    return transProbs

def retEmisProbs():
    emisProbs = []
    for pos in tags:
        emisProbs.append(list())
        for word in engWords:
            emisProbs[-1].append(1.0/float(len(tags)))
    return emisProbs


"""

"""            for sc in SubConj:
                if len(sc) == 3 and tkn == sc[0] and i + 2 < len(sent) and sent[i+1] == sc[1] and sent[i+2] == sc[2]:
                    adjustedTaggedSent = retagWithSC(i, adjustedTaggedSent)
                elif len(sc) == 2 and tkn == sc[0] and i + 1 < len(sent) and sent[i+1] == sc[1] and i > 0  and adjustedTaggedSent[i-1][1] != 'SC':
                    adjustedTaggedSent = retagWithSC(i, adjustedTaggedSent)
                elif len(sc) == 1 and tkn == sc[0]  and i > 0  and adjustedTaggedSent[i-1][1] != 'SC'  and i > 1  and adjustedTaggedSent[i-2][1] != 'SC':
                    adjustedTaggedSent = retagWithSC(i, adjustedTaggedSent)
     f.write('1\n')
        f.write(str(len(engWords))+'\n')
        for word in engWords:
            f.write(word + '\n')
        f.write(str(len(tags))+'\n')
        for pos in tags:
            f.write(pos + '\n')
        sprob = retStartProbs()
        for x in sprob:
            f.write(str(x) + '\n')
        tprob = retTransProbs()
        for pos in tags:
            for x in tprob[pos]:
                f.write(str(x) + '\n')
        f.write(str((len(corpus2)))+ '\n')
        for sent in corpus2:
            f.write('[')
            for tkn, pos in sent:
                if not tkn is sent[0][0]:
                    f.write(',')
                f.write('['+tkn+', '+pos+']')
         f.write(']\n')
   
   """
