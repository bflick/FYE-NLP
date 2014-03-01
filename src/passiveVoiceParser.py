from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

conjugates = ["be","was", "were", "been", "is", "being", "are", "got", "gotten", "had gotten"]
pastPart = "VBN"
det = "DT"
inFile = open("testpassivepaper.txt")
temp = ""
for line in inFile:
        temp += line
temp = temp.replace("!", ".")
temp = temp.replace("?", ".")
sents = temp.split(".")
#for line in inFile:
#	x = line.strip()
#	sents.append(x)


for sent in sents:
        tokens = []
        splitt = sent.split(" ")
        count = 0
        index = 0
        for i, j in pos_tag(word_tokenize(sent)):
            tokens.append(j)
	for token in tokens:
		if token == pastPart and tokens[tokens.index(token)-1] != det:
			index = tokens.index(token)
			for word in splitt:
				for conjugate in conjugates:
					if word == conjugate:
						if splitt.index(word) >= index - 2:
							count += 1
							break

			count += 1
			break



	if count >= 2:
		print sent
		print tokens
	else:
		print "FAILURE!"
